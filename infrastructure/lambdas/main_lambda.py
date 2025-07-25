import boto3
import os
 # main lambda
def handler(event, context):
    s3 = boto3.client("s3") # connect to s3
    sns = boto3.client("sns") # connect to sns

    bucket_name = os.environ["BUCKET_NAME"]
    topic_arn = os.environ.get("TOPIC_ARN")  

    print(f"Listing objects in bucket: {bucket_name}") 
    response = s3.list_objects_v2(Bucket=bucket_name) # use the AWS method to list from bucket

    object_names = [obj['Key'] for obj in response.get("Contents", [])]

    message = f"Found {len(object_names)} objects:\n" + "\n".join(object_names)
    print(message)

    if topic_arn:
        sns.publish(
            TopicArn=topic_arn,
            Subject="Lambda S3 Object Listing",
            Message=message
        )

    return {
        "statusCode": 200,
        "body": message
    }
