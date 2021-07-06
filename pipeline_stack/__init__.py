from aws_cdk import (
    core,
    aws_iam,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    pipelines,
)

from scenarios import (
    SampleScenarioStack,
)

from app_context import (
    AppContext,
    Parameters,
)

class DeployStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        SampleScenarioStack(self, 'Sample')


class CdkPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        param = Parameters.instance()
        pipeline_name = param.getParameter('pipeline_name')
        connection_arn = param.getParameter('connection_arn')
        github_owner = param.getParameter('github_owner')
        github_repo = param.getParameter('github_repo')
        github_branch = param.getParameter('github_branch')
        secret_arn = param.getParameter('secret_arn')

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(self, 'CdkPipeline', 
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name=pipeline_name,            
            source_action=cpactions.BitBucketSourceAction(
                action_name='GithubAction',
                output=source_artifact,
                connection_arn=connection_arn,
                owner=github_owner,
                repo=github_repo,
                branch=github_branch
            ),
            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                role_policy_statements=[
                    aws_iam.PolicyStatement(
                        actions=["secretsmanager:GetSecretValue"],
                        resources=[secret_arn]
                    )
                ],
                install_command='npm install -g aws-cdk && pip install --upgrade pip && pip install -r requirements.txt',
                synth_command=f"cdk synth -v -c region={AppContext.region} -c secret_name={AppContext.secret_name}",
            )
        )

        pipeline.add_application_stage(DeployStage(self, 'Deploy'))