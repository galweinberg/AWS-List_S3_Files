from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    RemovalPolicy,
    CustomResource,
)
from constructs import Construct
from pathlib import Path
import aws_cdk.custom_resources as cr


class DevopsAssignmentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # S3 creation
        bucket = s3.Bucket(self, "AssignmentBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
        # SNS part
        topic = sns.Topic(self, "S3NotificationTopic")
        topic.add_subscription(subs.EmailSubscription("galw123@gmail.com"))

        #   main lambda - that lists files in the bucket, creation
        lambda_fn = _lambda.Function(self, "ListS3Lambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="main_lambda.handler",
            code=_lambda.Code.from_asset(str(Path(__file__).parent / "lambdas")),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TOPIC_ARN": topic.topic_arn
            }
        )
        # premissions for lambda on s3 bucket
        bucket.grant_read(lambda_fn)

        #helper lambda to help us upload files, creation
        upload_lambda = _lambda.Function(self, "UploadFilesLambda",
        runtime=_lambda.Runtime.PYTHON_3_9,
        handler="upload_files.handler",
        code=_lambda.Code.from_asset(str(Path(__file__).parent / "lambdas")),
        environment={
        "BUCKET_NAME": bucket.bucket_name,
        "LOCAL_FOLDER": "sample_files"
    }
)       
        #premissions for helper lambda on s3 bucket
        bucket.grant_put(upload_lambda)


        #makes sure to activate while deplyoing
        provider = cr.Provider(self, "UploadFilesProvider", on_event_handler=upload_lambda)
        CustomResource(self, "TriggerUpload", service_token=provider.service_token)

