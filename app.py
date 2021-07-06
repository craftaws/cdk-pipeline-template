#!/usr/bin/env python3

import json
from aws_cdk import (
    core
)

from pipeline_stack import CdkPipelineStack as pipeline
from app_context import (
    AppContext,
    Parameters,
)

app = core.App()
secret_name = app.node.try_get_context("secret_name")
region = app.node.try_get_context("region")

AppContext.secret_name = secret_name
AppContext.region = region

param = Parameters.instance()

pipeline(app, param.getParameter('stack_name'))

app.synth()