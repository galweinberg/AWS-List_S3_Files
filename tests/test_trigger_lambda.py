import boto3

client = boto3.client("lambda")

# Try to find the function that starts with the expected logical name
functions = client.list_functions()["Functions"]
target_prefix = "DevopsAssignmentStack-ListS3Lambda"

function_name = None
for fn in functions:
    if fn["FunctionName"].startswith(target_prefix):
        function_name = fn["FunctionName"]
        break

if not function_name:
    raise Exception(f"No Lambda function found with prefix: {target_prefix}")

# Invoke the found function
response = client.invoke(
    FunctionName=function_name,
    InvocationType="RequestResponse"
)

print(response["Payload"].read().decode())