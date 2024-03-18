from typing import Tuple, Set
from boto3 import session

from pool_executor import PoolExecutor


AWS = 'AWS'
DO = 'DO'

VIDEO = 'video'
AUDIO = 'audio'
SUBTITLE = 'subtitle'


class S3Utils(object):
    def __init__(self, bucket_name, bucket_region, client=None, access_key=None, secret_key=None, cloud=DO):
        self.client = client
        self.bucket_region = bucket_region
        self.bucket_name = bucket_name
        if not client:
            self.client = self.get_client(access_key, secret_key, bucket_region, cloud)

    @staticmethod
    def get_client(access_key, secret_key, bucket_region, cloud):
        if cloud == DO:
            endpoint_url = f'https://{bucket_region}.digitaloceanspaces.com'
            aws_access_key_id = access_key
            aws_secret_access_key = secret_key
        elif cloud == AWS:
            endpoint_url = None
            aws_access_key_id = access_key
            aws_secret_access_key = secret_key
        else:
            raise NotImplementedError

        sess = session.Session()
        client = sess.client('s3',
                             region_name=bucket_region,
                             endpoint_url=endpoint_url,
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)

        return client

    def get_object(self, key, download_to, is_directory=False):
        self.client.download_file(self.bucket_name, key, download_to)

    def upload_files(self, key, file_path):
        if key.endswith('master.m3u8') or key.endswith('stream.mpd') or key.endswith('prod.mpd'):
            extra_args = {'ACL': 'private'}
        else:
            extra_args = {'ACL': 'public-read'}

        if key.endswith('.m3u8'):
            extra_args.update({'ContentType': 'application/x-mpegurl'})

        if not (key.endswith('ignore.mpd') or key.endswith('ignore.m3u8')):
            self.client.upload_file(file_path, self.bucket_name, key, ExtraArgs=extra_args)

    def bulk_upload_parallel(self, files: Set[Tuple[str, str]], pool_executor: 'PoolExecutor'):
        # TODO: Complete this with files
        # TODO: To handle thousands of files separate them into bulk lists
        pool_executor.multiprocessing_threads(self.upload_files, files)

    def check_if_path_exists(self):
        pass

    def set_acl(self, is_directory=False):
        pass

    def remove_object(self, is_directory=False):
        pass
