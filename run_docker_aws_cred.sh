docker run \
-e S3_BUCKET='Your Bucket' \
-e BARCODE_IND_STRING='Place Unique String to Identify Barcodes Here' \
-e S3_DIRECTORY='Directory in your bucket with jpgs' \
-e AWS_ACCESS_KEY_ID='Your Access KEY' \
-e AWS_SECRET_ACCESS_KEY='Your Secret key' \
danaswanstrom/script_vin_reading
