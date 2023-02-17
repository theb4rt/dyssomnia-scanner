# -*- coding: utf-8 -*-
import os
import random

import boto3
from boto3.exceptions import S3UploadFailedError

from ms import app
from ms.helpers.response import response_error
from ms.helpers.response import response_ok


class AwsManager:
    def __init__(self):
        self.s3 = boto3.client('s3', aws_access_key_id=app.config.get('S3_KEY'),
                               aws_secret_access_key=app.config.get('S3_SECRET'),
                               region_name=app.config.get('S3_REGION', 'us-east-1')
                               )

    def validate_img(self, original_name):
        extension = original_name.split('.')[-1]
        allowed_extensions = ['jpg', 'jpeg', 'png']
        return True if extension in allowed_extensions else False

    def upload_image(self, file, directory=None):
        original_name = file.filename
        content_type = file.content_type
        file_location = f"tmp/{original_name}"
        validate_img = self.validate_img(original_name)
        if validate_img:
            try:
                file.save(file_location)
                s3 = boto3.resource('s3')
                bucket_name = app.config.get('S3_BUCKET_NAME')
                extension = original_name.split('.')[-1]
                if directory is None:
                    key_object = f'{random.getrandbits(128)}.{extension}'
                else:
                    key_object = f'{directory}/{random.getrandbits(128)}.{extension}'

                result = self.s3.upload_file(file_location, bucket_name, key_object,
                                             ExtraArgs={'ACL': 'public-read',
                                                        'ContentType': content_type})
                if os.path.exists(file_location):
                    os.remove(file_location)
                location = self.s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
                url = f"https://{bucket_name}.s3.amazonaws.com/{key_object}"
                return response_ok(data=url, message='Image uploaded successfully')

            except S3UploadFailedError as e:
                print(str(e))
                if os.path.exists(file_location):
                    os.remove(file_location)
                return response_error(message='Error uploading image', code=500)
            except Exception as e:
                print(str(e))
                if os.path.exists(file_location):
                    os.remove(file_location)
                return response_error(message='Error uploading image', code=500)

        return response_error(message='Invalid image extension', code=400)
