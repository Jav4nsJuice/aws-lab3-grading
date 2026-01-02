import json, boto3, os
from io import BytesIO
from PIL import Image
s3 = boto3.client('s3')
def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        bucket, key = body['bucket'], body['key']
        metadata_key = f"metadata/{os.path.basename(key)}.json"
        try:
            s3.head_object(Bucket=bucket, Key=metadata_key)
            continue # Idempotency: Skip if already exists
        except: pass
        resp = s3.get_object(Bucket=bucket, Key=key)
        img_data = resp['Body'].read()
        img = Image.open(BytesIO(img_data))
        metadata = {
            "source_bucket": bucket, "source_key": key, "format": img.format,
            "width": img.size[0], "height": img.size[1], "file_size_bytes": len(img_data)
        }
        s3.put_object(Bucket=bucket, Key=metadata_key, Body=json.dumps(metadata))
