import boto3

client = boto3.client("lambda")
response = client.invoke(
    FunctionName="ListS3Lambda",
    InvocationType="RequestResponse"
)

print(response['Payload'].read().decode())
