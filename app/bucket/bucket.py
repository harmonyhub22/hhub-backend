import os
import time
import boto3


AWS_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('S3_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
AWS_BUCKET_URL = str('https://' + AWS_BUCKET_NAME + '.s3.us-east-2.amazonaws.com/')

def getBotoClient():
    s3Session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
    return s3Session.client('s3', region_name='us-east-2')

def uploadBucketFile(file, filename, contentType):
    client = getBotoClient()
    print('got client')
    filename = generateFileName(filename)

    client.put_object(Body=file,
                    Bucket=AWS_BUCKET_NAME,
                    Key=filename,
                    ContentType=contentType)
    
    return AWS_BUCKET_URL + filename

def deleteBucketFile(url):

    client = getBotoClient()
    filename = url[url.rfind('/') + 1:]
    client.delete_object(Bucket=AWS_BUCKET_NAME,
                        Key=filename)


def generateFileName(originalName):
    return str(round(time.time() * 1000)) + "-" + originalName.replace(' ','_')