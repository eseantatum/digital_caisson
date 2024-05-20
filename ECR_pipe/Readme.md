# ECR_Pipe Project

This project sets up a CI/CD pipeline using AWS CDK to manage the deployment of Docker-based applications to Amazon ECR and Elastic Beanstalk. The pipeline leverages AWS CodeCommit, CodeBuild, and CodePipeline services.

## Project Structure

ECR_pipe/
- ├── cicd_workshop/
- │ ├── app-cdk/
- │ │ ├── app.py
- │ │ ├── app_cdk/
- │ │ │ ├── app_cdk_stack.py
- │ │ │ ├── ecr_cdk_stack.py
- │ │ │ ├── pipeline_cdk_stack.py
- │ │ └── readme.md
- │ ├── buildspec_docker.yml
- │ └── buildspec_test.yml

markdown


### Directory and File Descriptions

- **cicd_workshop/app-cdk/app.py**: The main entry point for the CDK application. It initializes the CDK stacks.
- **cicd_workshop/app-cdk/app_cdk/app_cdk_stack.py**: Defines the `AppCdkStack`, a placeholder for additional application resources.
- **cicd_workshop/app-cdk/app_cdk/ecr_cdk_stack.py**: Defines the `EcrCdkStack` which creates ECR repositories for the services.
- **cicd_workshop/app-cdk/app_cdk/pipeline_cdk_stack.py**: Defines the `PipelineCdkStack` which sets up the CI/CD pipeline using CodePipeline and CodeBuild.
- **cicd_workshop/buildspec_docker.yml**: The build specification for building and pushing Docker images to ECR.
- **cicd_workshop/buildspec_test.yml**: The build specification for running tests (not detailed here).
- **cicd_workshop/app-cdk/readme.md**: Instructions for setting up and using the CDK application in the `app-cdk` directory.

## Getting Started

### Prerequisites

- AWS CLI configured with appropriate permissions.
- AWS CDK installed.
- Docker installed and running.

### Setup

1. **Clone the repository**:

    ```sh
    git clone <repository-url>
    cd ECR_pipe/cicd_workshop/app-cdk
    ```

2. **Create and activate a virtual environment**:

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate.bat`
    ```

3. **Install the required dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Bootstrap the CDK environment**:

    ```sh
    cdk bootstrap
    ```

5. **Deploy the stacks**:

    ```sh
    cdk deploy
    ```

### Build and Push Docker Images

The `buildspec_docker.yml` file contains the build specification for building and pushing Docker images to ECR. It performs the following steps:

1. Logs in to Amazon ECR.
2. Builds the Docker images for each service defined in the `docker-compose.yml` file.
3. Tags the images with the latest tag.
4. Pushes the images to the respective ECR repositories.

### Code Explanation

#### app.py

This file initializes the CDK application and defines three stacks:

- `EcrCdkStack`: Creates ECR repositories for different services.
- `AppCdkStack`: A placeholder stack for application-specific resources.
- `PipelineCdkStack`: Sets up the CI/CD pipeline.

#### ecr_cdk_stack.py

Defines the `EcrCdkStack` class which creates ECR repositories for each service specified in the `services` list.

#### pipeline_cdk_stack.py

Defines the `PipelineCdkStack` class which sets up the CI/CD pipeline. The pipeline includes stages for source, unit tests, and Docker build and push.

### Useful Commands

- **List all stacks in the app**:

    ```sh
    cdk ls
    ```

- **Synthesize the CloudFormation template**:

    ```sh
    cdk synth
    ```

- **Deploy the stack to your default AWS account/region**:

    ```sh
    cdk deploy
    ```

- **Compare the deployed stack with the current state**:

    ```sh
    cdk diff
    ```

## Conclusion

This project demonstrates how to set up a CI/CD pipeline using AWS CDK to manage Docker-based applications. The pipeline handles source control with CodeCommit, builds with CodeBuild, and deployment with CodePipeline. The Docker images are built and pushed to ECR, and the application is deployed using Elastic Beanstalk.

This README provides an overview of the project structure, setup instructions, and details about the main components and their functionalities. Make sure to replace <repository-url> with the actual URL of your repository.
