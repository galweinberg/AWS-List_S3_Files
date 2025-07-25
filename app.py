#!/usr/bin/env python3
import aws_cdk as cdk
from infrastructure.infra_stack import InfraStack
import os

app = cdk.App()

InfraStack(
    app,
    "InfraStack",
    env=cdk.Environment(
        account=os.environ["AWS_ACCOUNT_ID"],
        region=os.environ["AWS_REGION"]
    )
)

app.synth()
