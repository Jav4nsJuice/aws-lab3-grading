import json, boto3, os
sqs = boto3.client('sqs')
def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        if key.lower().endswith(('.jpg', '.jpeg', '.png')):
            msg = {'bucket': bucket, 'key': key}
            sqs.send_message(QueueUrl=os.environ['QUEUE_URL'], MessageBody=json.dumps(msg))
