import boto3
from botocore.exceptions import ClientError
import json
import builtins
import sys

class AppContext:
    secret_name = None
    region = None

class SingletonInstane:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

class Parameters(SingletonInstane):

    def __init__(self):
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager', region_name=AppContext.region)

        try:
            response = client.get_secret_value(SecretId=AppContext.secret_name)
        except ClientError as e:
            print(e.response['Error']['Code'])
            sys.exit('Failed to load parameters from SecretManager')
        else:
            self.pipeline_config = json.loads(response['SecretString'])
            self.pipeline_config['secret_arn'] = response['ARN']

    def getParameter(self, key: builtins.str):
        return self.pipeline_config.get(key)