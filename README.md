# batch-code

## Build Image
``
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
