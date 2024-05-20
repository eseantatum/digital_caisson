# CDK Pipeline Elastic Beanstalk Demo

This project demonstrates how to set up a CI/CD pipeline using AWS CDK to deploy a web application to AWS Elastic Beanstalk. The pipeline leverages AWS CodePipeline, CodeBuild, and Elastic Beanstalk services.

## Project Structure

cdk-pipeline-eb-demo/
├── bin/
│ └── cdk-pipeline-eb-demo.ts
├── lib/
│ ├── cdk-pipeline-eb-demo-stack.ts
│ ├── cdk-pipeline-stack.ts
│ ├── eb-appln-stack.ts
│ └── eb-stage.ts
├── src/
│ └── <your-application-code>
├── .gitignore
├── cdk.json
├── package.json
├── README.md
└── tsconfig.json

markdown


### Directory and File Descriptions

- **bin/cdk-pipeline-eb-demo.ts**: Entry point for the CDK application. It initializes the CDK app and stacks.
- **lib/cdk-pipeline-eb-demo-stack.ts**: Defines the main application stack (currently a placeholder).
- **lib/cdk-pipeline-stack.ts**: Defines the CI/CD pipeline using AWS CodePipeline.
- **lib/eb-appln-stack.ts**: Defines the Elastic Beanstalk application and environment stack.
- **lib/eb-stage.ts**: Defines the deployment stage for the Elastic Beanstalk application.
- **src/**: Directory containing your application code to be deployed.
- **cdk.json**: Configuration file for the CDK CLI.
- **package.json**: Node.js project file, including dependencies.
- **tsconfig.json**: TypeScript configuration file.

## Getting Started

### Prerequisites

- AWS CLI configured with appropriate permissions.
- AWS CDK installed.
- Node.js and npm installed.
- Docker installed and running (if your application requires Docker).

### Setup

1. **Clone the repository**:

    ```sh
    git clone <repository-url>
    cd cdk-pipeline-eb-demo
    ```

2. **Install dependencies**:

    ```sh
    npm install
    ```

3. **Bootstrap the CDK environment**:

    ```sh
    cdk bootstrap
    ```

4. **Deploy the pipeline stack**:

    ```sh
    cdk deploy CdkPipelineStack
    ```

## Code Explanation

### bin/cdk-pipeline-eb-demo.ts

This file initializes the CDK application and defines the `CdkPipelineStack` stack with the AWS account and region specified.

### lib/cdk-pipeline-eb-demo-stack.ts

Defines the `CdkPipelineEbDemoStack` class which is a placeholder for additional resources required by the application.

### lib/cdk-pipeline-stack.ts

Defines the `CdkPipelineStack` class which sets up the CI/CD pipeline using AWS CodePipeline. The pipeline includes a source stage that pulls code from GitHub, and a build stage that installs dependencies, builds the project, and synthesizes the CDK app.

### lib/eb-appln-stack.ts

Defines the `EBApplnStack` class which creates an Elastic Beanstalk application and environment. It uploads the application code to an S3 bucket, creates an Elastic Beanstalk application and application version, sets up an IAM role and instance profile, and configures the environment settings.

### lib/eb-stage.ts

Defines the `CdkEBStage` class which represents a deployable unit of the web service application. It creates an instance of `EBApplnStack` with the provided properties for minimum and maximum instance sizes, instance types, and environment name.

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

This project demonstrates how to set up a CI/CD pipeline using AWS CDK to deploy a web application to AWS Elastic Beanstalk. The pipeline leverages AWS CodePipeline, CodeBuild, and Elastic Beanstalk services.
