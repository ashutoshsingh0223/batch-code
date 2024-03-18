from typing import List, Tuple
import argparse
from pathlib import Path

import os

from S3Utils import S3Utils, VIDEO, AUDIO
from video_transcoder import VideoTranscoder

DATA_VOLUME = '/opt/data'


def check_args(args):
    if args.type == VIDEO:
        if not args.aspect_ratio:
            raise ValueError(f'For type {VIDEO} aspect ratio must be defined')
            
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI parameters for end-to-end batch job')
    parser.add_argument('--access-key', type=str, required=True, help='AWS Access Key for s3 access')
    parser.add_argument('--secret-key', type=str, required=True, help='AWS Secret Key for s3 access')
    parser.add_argument('--key', type=str, required=True, help='path of file video file relative to s3 type bucket')
    parser.add_argument('--language', type=str, required=True, help='language of original audio in the video file')
    parser.add_argument('--bucket-name', type=str, required=True, help='s3 compatible bucket name')
    parser.add_argument('--bucket-region', type=str, required=True, help='s3 compatible bucket region')
    parser.add_argument('--bandwidth', type=int, nargs='+', default=[3500, 2000, 1000], help='bandwidth in kbps')
    # TODO Remove this and enforce that unit be 'k'
    parser.add_argument('--bandwidth-unit', type=str, default='k', help='Unit of bandwidth')
    parser.add_argument('--aspect-ratio', type=str, nargs='+', default=['1920:1080', '1280:720', '768:480'],
                        help='Aspect ratios to encode to')
    parser.add_argument('--type', type=str, default=VIDEO)
 

    args = parser.parse_args()
    bandwidths: List[int] = args.bandwidth
    aspect_ratios: List[str] = args.aspect_ratio

    assert len(aspect_ratios) == len(bandwidths), 'Number of aspect ratios should batch the number of bandwidths'

    s3 = S3Utils(bucket_name=args.bucket_name, bucket_region=args.bucket_region, access_key=args.access_key,
                 secret_key=args.secret_key)
    
    # Make folder structure in data volume corresponding to object storage structure
    # Example:
    # key = "path/to/file.mp4"
    # storage_dir = "path/to"
    storage_dir = '/'.join(args.key.split('/')[:-1])
     
    out_dir = Path(DATA_VOLUME) / storage_dir
    Path(out_dir).mkdir(parents=True, exist_ok=True)
  
    # Location on disk to download the file to.
    download_to = str(Path(DATA_VOLUME) / args.key)
    s3.get_object(args.key, download_to=download_to)
    
    # Prepare out-params for VideoTranscoder
    out_params = []
    output_file_names = []
    output_files = []
    for bandwidth, aspect_ratio in zip(bandwidths, aspect_ratios):
        
        identifier = f"{aspect_ratio.replace(':', '-')}-{bandwidth}"
        output_file_name = f"{identifier}.mp4"
        out_param = {
                        "codec": "H.264",
                        "bandwidth": bandwidth,
                        "aspect_ratio": aspect_ratio,
                        "unit": args.bandwidth_unit
                    }
        out_params.append(out_param)
        output_file_names.append(output_file_name)
        output_files.append(str(out_dir / output_file_name))
    
    # Initialize Transcoder and start the process
    transcoder = VideoTranscoder(input_file=download_to, out_params=out_params, output_files=output_files)
    # We don't want to separate audio track, so keep_audio is set.
    transcoder.transcode(keep_audio=True)
    
    # Upload transcoded video files and delete from disk
    for output_file_name in output_file_names):
        output_file = str(out_dir / output_file_name)
        s3.upload_files(f'{storage_dir}/encoded/{output_file_name}', file_path=output_file)
        os.remove(output_file)
