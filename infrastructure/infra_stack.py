from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    RemovalPolicy,
    CustomResource,
    Duration,
    CfnOutput,
)
import os
from constructs import Construct
from pathlib import Path
import aws_cdk.custom_resources as cr
from datetime import datetime

class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # S3 creation
        bucket = s3.Bucket(self, "AppBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True 
            # auto deletes when destroyd
        )
        # SNS part - for email notifications in lambda
        topic = sns.Topic(self, "S3NotificationTopic")
        topic.add_subscription(subs.EmailSubscription(os.environ["NOTIFY_EMAIL"])) 
        # plug in the email as secret



        #IAM part - attached to main lambda
        lambda_role = iam.Role(self, "mainLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        ]
    )
        # gives premissions as needed to s3 and SNS
        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:List*", "s3:GetObject*", "sns:Publish"],
            resources=[
            bucket.bucket_arn,
            f"{bucket.bucket_arn}/*",
            topic.topic_arn
        ]
    ))




        #   main lambda - that lists files and sends SNS
        main_lambda = _lambda.Function(self, "ListS3Lambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="main_lambda.handler",
            code=_lambda.Code.from_asset(str(Path(__file__).parent / "lambdas")),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TOPIC_ARN": topic.topic_arn
            },
            role = lambda_role,
            timeout=Duration.seconds(10)  # to make sure it doesnt timeout

        )
        CfnOutput(self, "ListS3LambdaFunctionName",
        value=main_lambda.function_name,
        export_name="ListS3LambdaFunctionName"
)


        #helper lambda - uploads local files from "upload_files" to to s3 in deploy
        upload_lambda = _lambda.Function(self, "UploadFilesLambda",
        runtime=_lambda.Runtime.PYTHON_3_9,
        handler="upload_files.handler",
        code=_lambda.Code.from_asset(str(Path(__file__).parent / "lambdas")),
        timeout=Duration.seconds(10),
        environment={
        "BUCKET_NAME": bucket.bucket_name,
        "LOCAL_FOLDER": "sample_files"
    }
)       
        #premissions for helper lambda on s3 bucket
        bucket.grant_put(upload_lambda)


        #makes sure to activate while deplyoing
        provider = cr.Provider(self, "UploadFilesProvider", on_event_handler=upload_lambda)
        CustomResource(self, "TriggerUpload", service_token=provider.service_token, 
                          properties={
        "Version": str(datetime.now())  
    })

