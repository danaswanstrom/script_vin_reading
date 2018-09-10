# If you have configured your machine with aws configure the following
# will allow you to access your credentials
AWS_ACCESS_KEY_ID=$(aws --profile default configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws --profile default configure get aws_secret_access_key)

docker run \
-e BARCODE_IND_STRING='Place Unique String to Identify Barcodes Here' \
-e S3_BUCKET='Your Bucket Name' \
-e S3_DIRECTORY='Your Directory Name' \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
danaswanstrom/script_vin_reading
