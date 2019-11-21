
# def getSizeIfExists(client, bucket, key):
#     """return the key's size if it exist, else None"""
#     response = client.list_objects_v2(
#         Bucket=bucket,
#         Prefix=key,
#     )
#     for obj in response.get('Contents', []):
#         print(obj)
#         if obj['Key'] == key:
#             return obj['Size']
#     return None

# for filename, filesize, fileobj in extract(zip_file):
    #     size = getSizeIfExists(bucket, filename)
    #     if size is None or size != filesize:
    #         filename = 
    #         upload_to_s3(bucket, filename, fileobj)
    #         print('Updated!' if size else 'New!')
    #     else:
    #         print('Ignored')


def lambda_handler(event, context):
    fileObj = event['fileObj']
    # fileName = event['fileName']
    # fileSize = event['fileSize']

    sport = event['sport']
    gameType = event['gameType']

    
    return api_response(200, body)