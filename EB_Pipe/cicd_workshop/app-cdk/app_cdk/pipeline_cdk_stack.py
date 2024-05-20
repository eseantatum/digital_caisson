import os
from constructs import Construct
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codebuild as codebuild,
    aws_codepipeline_actions as codepipeline_actions,
    aws_iam as iam,
)
import aws_cdk as cdk
from app_cdk.eb_stack import (
    CdkEBStage,
    EBApplnStack
)

class PipelineCdkStack(Stack):

    def __init__(self, scope: Construct, id: str, ecr_repository, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repository called 'CICD_Workshop'
        repo = codecommit.Repository(
            self, 'CICD_Workshop-eb',
            repository_name = 'CICD_Workshop',
            description = 'Repository for my application code and infrastructure'
        )

        pipeline = codepipeline.Pipeline(
            self, 'CICD_Pipeline-eb',
            cross_account_keys = False
        )

        code_quality_build = codebuild.PipelineProject(
            self, 'Code Quality',
            build_spec = codebuild.BuildSpec.from_source_filename('./buildspec_test.yml'),
            #build_spec = codebuild.BuildSpec.from_object({
            #    'version': '0.2'

            #}),
            environment = codebuild.BuildEnvironment(
                build_image = codebuild.LinuxBuildImage.STANDARD_5_0,
                privileged = True,
                compute_type = codebuild.ComputeType.LARGE,
            ),
        )

        docker_build_project = codebuild.PipelineProject(
            self, 'Docker Build',
            build_spec = codebuild.BuildSpec.from_source_filename('./buildspec_docker.yml'),
            environment = codebuild.BuildEnvironment(
                build_image = codebuild.LinuxBuildImage.STANDARD_5_0,
                privileged = True,
                compute_type = codebuild.ComputeType.LARGE,
                environment_variables = {
                    'IMAGE_TAG': codebuild.BuildEnvironmentVariable(
                        type = codebuild.BuildEnvironmentVariableType.PLAINTEXT,
                        value = 'latest'
                    ),
                    'IMAGE_REPO_URI': codebuild.BuildEnvironmentVariable(
                        type = codebuild.BuildEnvironmentVariableType.PLAINTEXT,
                        value = ecr_repository.repository_uri
                    ),
                    'AWS_DEFAULT_REGION': codebuild.BuildEnvironmentVariable(
                        type = codebuild.BuildEnvironmentVariableType.PLAINTEXT,
                        value = os.environ['CDK_DEFAULT_REGION']
                    )
                }
            ),
        )

        docker_build_project.add_to_role_policy(iam.PolicyStatement(
            effect = iam.Effect.ALLOW,
            actions = [
                'ecr:GetAuthorizationToken',
                'ecr:BatchCheckLayerAvailability',
                'ecr:GetDownloadUrlForLayer',
                'ecr:GetRepositoryPolicy',
                'ecr:DescribeRepositories',
                'ecr:ListImages',
                'ecr:DescribeImages',
                'ecr:BatchGetImage',
                'ecr:InitiateLayerUpload',
                'ecr:UploadLayerPart',
                'ecr:CompleteLayerUpload',
                'ecr:PutImage'
            ],
            resources = ['*'],
        ))

        source_output = codepipeline.Artifact()
        unit_test_output = codepipeline.Artifact()
        docker_build_output = codepipeline.Artifact()

        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name = 'CodeCommit',
            repository = repo,
            output = source_output,
            branch = 'main'
        )

        pipeline.add_stage(
            stage_name = 'Source',
            actions = [source_action]
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name = 'Unit-Test',
            project = code_quality_build,
            input = source_output,  # The build action must use the CodeCommitSourceAction output as input.
            outputs = [unit_test_output]
        )

        pipeline.add_stage(
            stage_name = 'Code-Quality-Testing',
            actions = [build_action]
        )

        docker_build_action = codepipeline_actions.CodeBuildAction(
            action_name = 'Docker-Build',
            project = docker_build_project,
            input = source_output,
            outputs = [docker_build_output]
        )

        pipeline.add_stage(
            stage_name = 'Docker-Push-ECR',
            actions = [docker_build_action]
        )

        deploy = CdkEBStage(
            self, 'Pre-Prod', [1,2],
        )
        
        deploy_stage = pipeline.add_stage(stage_name='Deploy')
        deploy_stage.add_action(
            codepipeline_actions.CloudFormationCreateReplaceChangeSetAction(
                action_name='CreateChangeSet',
                stack_name=deploy.stack_name,
                change_set_name='DeployChangeSet',
                template_path=pipeline.artifact_stages['Synth'].output_artifacts[0].file_path,
                admin_permissions=True
            )
        )

        CfnOutput(
            self, 'CodeCommitRepositoryUrl',
            value = repo.repository_clone_url_http
        )



class CdkPipelineStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        pipeline = codepipeline.Pipeline(
            self, 'Pipeline',
            pipeline_name='MyServicePipeline',
            synth=codepipeline.ShellStep(
                'Synth',
                input=codepipeline_actions.GitHubSourceAction(
                    action_name='GitHub',
                    output=codepipeline.Artifact(),
                    oauth_token=cdk.SecretValue.secrets_manager('github-token'),
                    owner='eseantatum',
                    repo='eb_tut',
                    branch='main'
                ),
                commands=[
                    'npm i -g npm@latest',
                    'npm ci',
                    'npm run build',
                    'npx cdk synth'
                ]
            )
        )

        deploy = CdkEBStage(
            self, 'Pre-Prod',
            min_size='1',
            max_size='2'
        )
        deploy_stage = pipeline.add_stage(stage_name='Deploy')
        deploy_stage.add_action(
            codepipeline_actions.CloudFormationCreateReplaceChangeSetAction(
                action_name='CreateChangeSet',
                stack_name=deploy.stack_name,
                change_set_name='DeployChangeSet',
                template_path=pipeline.artifact_stages['Synth'].output_artifacts[0].file_path,
                admin_permissions=True
            )
        )

