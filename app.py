#!/usr/bin/env python3
import aws_cdk as cdk
from devops_assignment.devops_assignment_stack import DevopsAssignmentStack
import os

app = cdk.App()

DevopsAssignmentStack(
    app,
    "DevopsAssignmentStack",
    env=cdk.Environment(
        account=os.environ["AWS_ACCOUNT_ID"],
        region=os.environ["AWS_REGION"]
    )
)

app.synth()
