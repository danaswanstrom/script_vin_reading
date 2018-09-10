
# coding: utf-8

# To run this you will need to install the following on your Linux box
# libzbar-dev 
# libzbar0

# Used to read environment variables
import os

# Required to read from S3
from io import BytesIO

# AWS connector
import boto3

# OpenCV python package
import cv2

# Python barcode reader
import pyzbar.pyzbar as pyzbar

# Package to support arrays
import numpy as np

# Pandas to create a storage spot for decoded data
import pandas as pd

# Regex
import re

# Used to upload JSON
import json

# Used for timestamp of JSON file
import datetime

# Used if to get VIN information
import requests

# Parameters hard coded
# Uncomment and comment the section below
# s3_bucket_name = 'sample-vin-number-images'
# director_in_bucket_name = 'SampleImages'

# Parameters pass in from Docker run script
s3_bucket_name = os.environ['S3_BUCKET']
director_in_bucket_name = os.environ['S3_DIRECTORY']
barcode_file_indicator_string = os.environ['BARCODE_IND_STRING']

# Create all our resources and clients we will need to interact with AWS
# AWS credientials must have been provided in the docker startup bash script

# Create a resource connection to s3
s3_resource = boto3.resource('s3')

# Create a client connection to s3
s3_client = boto3.client('s3')

# Create a boto3 bucket instance using bucket name parameter
my_bucket = s3_resource.Bucket(s3_bucket_name)

# Functions necessary to decode

def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
  return decodedObjects

# Get a list of all the files in your directory
files = list(my_bucket.objects.filter(Prefix=director_in_bucket_name))
matches_barcode_inicator = re.compile(barcode_file_indicator_string, re.IGNORECASE)
files = filter(matches_barcode_inicator.search, files)

# The list of objects starts with the directory as the first item in the list
# We remove that first item and keep the rest
# files = files[1:]

# Creates list of numbers from 1 to the length of our photo list
index = list(range(1,len(files)+1))

# Creates the empty dataframe with dtype as object
image_dataframe = pd.DataFrame(index=index, columns=['Photo_SN','Vin','Make','Model','ModelYear'])

for index, file in enumerate(files, start = 0):    
    # Obtain the file from aws and load into memory
    image_object = my_bucket.Object(files[index].key)
    
    # Take the file that is in memory and create an np array
    nparr = np.frombuffer(image_object.get()['Body'].read(), np.uint8)
    
    # Use Open CV to decode the np array so the barcode can be decoded
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Decode the barcode
    decodedObjects = decode(img_np)
    
    # Obtain the serial number for the photo
    photo_sn = re.search(r'(?<=\/).*?(?=_)', file.key).group()
    
    
    # If the OpenCV does not identify a barcode, the decode returns and empty list
    if not decodedObjects:
        # record the photo serial number in dataframe
        image_dataframe['Photo_SN'][index + 1] = photo_sn
        # Put empty text into dataframe
        image_dataframe['Vin'][index + 1] = ""
    
    # With a non-empty list we want to do some format changes before recording the vin
    else:    
        # Decoded object is byte type. Convert it and strip white space
        vin_1 = decodedObjects[0].data.decode("utf-8").strip()
     
        # If a vin has any characaters that are non-alphanumeric, remove those
        pattern = re.compile('[\W_]+')
        vin_1 = pattern.sub('', vin_1)
        
        # Record photo serial number in dataframe
        image_dataframe['Photo_SN'][index + 1] = photo_sn
        
        if len(vin_1) == 18:
            # Get rid of any leading or trailing whitespace in vin
            image_dataframe['Vin'][index + 1] = vin_1[1:]
        else:
            image_dataframe['Vin'][index + 1] = vin_1
        
        
print("Done with Barcodes")


# This sections requests vehicle information from the NHTSA website

row_start = 1
row_end = len(image_dataframe['Vin'])+1

for row in range(row_start, row_end):
    vin = image_dataframe['Vin'][row]
    if vin != "":
        url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/' + vin + '?format=json'
        r = requests.get(url)
        r_json = r.json()
        image_dataframe['Make'][row] = (r_json['Results'][0]['Make'])
        image_dataframe['Model'][row] = (r_json['Results'][0]['Model'])
        image_dataframe['ModelYear'][row] = (r_json['Results'][0]['ModelYear'])
    else:
        image_dataframe['Make'][row] = ''
        image_dataframe['Model'][row] = ''
        image_dataframe['ModelYear'][row] = ''

print("Done with vehicle data")
        
# Upload the data to your S3 bucket as json

# Create the json from the pandas dataframe
dataframe_as_json = image_dataframe.to_json(orient='index')

# Create a new s3 object
json_obj = s3_resource.Object(s3_bucket_name,str(datetime.datetime.now()) + 'Vin Numbers.json')

# Upload the object to s3
json_obj.put(Body=dataframe_as_json)

print("Done with uploading json to the bucket:" + s3_bucket_name)
