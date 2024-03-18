# batch-code

## Build Image
```
cd app
// Build the image named batch with v1 tag
docker build --tag batch:v1 .
```



## Push Image to ECR
```
// Tag the image with the ECR repository path.
// aws-account-id: This is your aws account id.
// ecr-repo-region: Region in which ecr repo exists. For example: `us-east-1`
// ecr-repo-name: Name of the repository.
docker tag batch:v1 {aws-account-id}.dkr.ecr.{ecr-repo-region}.amazonaws.com/{ecr-repo-name}:v1

// Login to aws-ecr
aws ecr get-login-password --region {ecr-repo-region} | docker login --username AWS --password-stdin {aws-account-id}.dkr.ecr.{ecr-repo-region}.amazonaws.com
// Finally push the image to the respository
docker push {aws-account-id}.dkr.ecr.{ecr-repo-region}.amazonaws.com/{ecr-repo-name}:v1
```


## JSON command for bento3 Batch client(or directly submit a job from aws batch console)
```
[
"python", "main.py",
"--access-key", "<aws-access-key-s3>",
"--secret-key", "<aws-secret-key-s3>",
"--key", "path/to/file.mp4",
"--language", "en",
"--bucket-name", "Encoding",
"--bucket-region", "<aws-region>",
"--bandwidth", 4000, 2000,
"--aspect-ratio", "1920:1080", "1280:720"
]
```

## main.py options

```
--access-ke: AWS Access Key for s3 access.
--secret-key: AWS Secret Key for s3 access.
--key: Path of file video file relative to s3 type bucket.
--language: Language code(ISO) of original audio in the video file.
--bucket-name: S3 compatible bucket name.
--bucket-region: S3 compatible bucket region.
--bandwidth: Bandwidth in kbps. default=[3500, 2000, 1000]
--aspect-ratio: Aspect ratios to encode to. default=['1920:1080', '1280:720', '768:480']
```
