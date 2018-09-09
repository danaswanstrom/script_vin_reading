# If you have configured your machine with aws configure the following
# will allow you to access your credentials
AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key)

docker run \
-e S3_BUCKET='sample-vin-number-images' \
-e S3_DIRECTORY='SampleImages' \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
script1
