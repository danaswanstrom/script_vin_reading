docker run \
-e S3_BUCKET='Your Bucket' \
-e S3_DIRECTORY='Directory in your bucket with jpgs' \
-e AWS_ACCESS_KEY_ID='Your Access KEY' \
-e AWS_SECRET_ACCESS_KEY='Your Secret key' \
danaswanstrom/script_vin_reading
#
# Alternative below if you have use AWS configure on the machine 
#
# AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id)
# AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key)
#
#docker run \
#-e S3_BUCKET='sample-vin-number-images' \
#-e S3_DIRECTORY='SampleImages' \
#-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
#-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
#danaswanstrom/script_vin_reading
