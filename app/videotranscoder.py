
from typing import List, Dict, Any
from utils import execute
from pool_executor import PoolExecutor


class VideoTranscoder(object):
    """
    H.264 configs based on http://trac.ffmpeg.org/wiki/Encode/H.264
    Two pass ffmpeg
    # ffmpeg -y -i input -c:v libx264 -b:v 2600k -pass 1 -an -f null /dev/null && \
    # ffmpeg -i input -c:v libx264 -b:v 2600k -pass 2 -c:a aac -b:a 128k output.mp4
    """

    def __init__(self, input_file: str, out_params: List[Dict[str, Any]], output_files: List[str], out_type: str = 'VOD'):
        """
        Args:
            input_file: Input filepath or a URL.
            out_params: Dictionary containing values of output parameters used by ffmpeg.
                        Example- [
                            {
                                "codec": "H.264",
                                "bandwidth": Mandatory,
                                "unit:": Mandatory,
                                "maxrate": [Optional],
                                "bufsize": [Optional],
                                "aspect_ratio": '1280:720',
                             },
                            {
                                "codec": "H.264",
                                "bandwidth": Mandatory,
                                "unit:": Mandatory,
                                "maxrate": [Optional],
                                "bufsize": [Optional],
                                "aspect_ratio": '768:480',
                             }
                        ]
            output_files: Output filepaths.
            out_type: Type of encoding. Defaults to VOD(Video On Demand).
        """
        # TODO: Input File can act as a valid URL as well
        self.input_file = input_file
        self.out_params = out_params
        self.output_type = out_type
        self.output_files = output_files
        self.last_command = None

        self.command_prefix: str = f'ffmpeg -i {self.input_file}'

    def if_file_absent(self):
        pass

    def if_no_write_access(self):
        pass

    @staticmethod
    def generate_command(command_params: Dict[str, Any]):
        """
        Args:
            command_params: Dict of options and values for ffmped commands.
        """
        command = ''
        for key, value in command_params.items():
            if isinstance(value, str):
                command += f'{key} {value} '
            elif isinstance(value, bool):
                if value:
                    command += f'{key} '

        command = command.strip()
        return command

    def generate_command_params_audio(self):
        """
        Create a dict of options and corresponding values for audio transcoding. 
        -i: input file path
        -c:a: Audio codec
        -ac: Number of audio channels
        -ab: Bitrate for audio channel.
        """
        command_params = dict()
        command_params['-i'] = self.input_file
        # codec
        command_params['-c:a'] = 'aac'
        # Audio channels
        command_params['-ac'] = '2'
        # bandwidth
        command_params['-ab'] = '128k'
        return command_params

    def generate_command_params_video(self, out_param: Dict[str, Any]):
        """
        Create a dict of options and corresponding values for video transcoding from one item in self.out_params. 
        -i: input file path
        -c:v: Video codec(defaults to 'libx264').
        -x264opts: Options for codec. Like framerate etc.
        --b:v: Bandwidth(bitrate) for output stream.
        
        Args:
            out_param: One item from the list self.out_params to take the values from.
        """
        command_params = dict()
        codec = out_param.get('codec', 'H.264')
        if codec == 'H.264':
            # TODO: preset and tune are not working. Check later. Error:
            #  Codec AVOption tune (Tune the encoding to a specific scenario) specified for input

            # preset = self.out_params.get('preset', 'fast' if self.output_type == 'VOD' else 'veryfast')
            # command_params['-preset'] = preset
            #
            # tune = self.out_params.get('tune', 'film' if self.output_type == 'VOD' else 'zerolatency')
            # command_params['-tune'] = tune
            bandwidth = out_param['bandwidth']
            bandwidth_value = int(bandwidth)
            bandwidth_unit = out_param.get('unit', 'k')

            maxrate = bandwidth_value + 200
            bufsize = bandwidth_value * 2
            command_params['-c:v'] = 'libx264'
            command_params['-x264opts'] = "'keyint=24:min-keyint=24:no-scenecut'"
            command_params['-b:v'] = out_param['bandwidth']
            command_params['-maxrate'] = out_param.get('maxrate', f'{maxrate}{bandwidth_unit}')
            command_params['-bufsize'] = out_param.get('bufsize', f'{bufsize}{bandwidth_unit}')
            command_params['-vf'] = f"'scale={out_param['aspect_ratio']}'"

        elif codec == 'H.265':
            raise ValueError('Not Supported yet')
        return command_params

    def transcode(self, keep_audio=False):
        """
        Main method for transcoding.
        """
        for out_param, outfile in zip(self.out_params, self.output_files):
            command_params = self.generate_command_params_video(out_param=out_param)
            if keep_audio:
                command_params['-c:a'] = 'copy'
            else:
                # Leave audio out
                command_params['-an'] = True

            command = self.generate_command(command_params)

            command = f'{command} {outfile}'
            complete_command = f'{self.command_prefix} {command}'

        complete_command = complete_command.strip()

        self.last_command = complete_command
        # if out_param.get('two_pass'):
        #     # TODO: The complete command isn't working fix it. Reason: POpen does not use a shell
        #     #  so '&&' doesn't work as a seaparator
        #
        #     # prevents audio in pass 1
        #     # command_params['-an'] = True
        #     pass_1 = command + " -y -pass 1 -an -f null /dev/null"
        #     complete_command = pass_1 + f" && {command} -pass 2 {outfile}"
        #
        # else:
        #     complete_command = f"{command} {outfile}"
        print(complete_command)
        execute([complete_command])

    def transcode_audio(self, outfile):
        """
        Main method for transcoding audio.
        """
        command_params = self.generate_command_params_audio()
        command_params['-vn'] = outfile
        command = self.generate_command(command_params)
        complete_command = f'{self.command_prefix} {command}'

        execute(commands=[complete_command.strip()])
view rawvideo_transcoder.py hosted with ❤ by GitHub
