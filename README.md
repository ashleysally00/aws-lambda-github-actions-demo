# Deploying AWS Lambda Using GitHub Actions

This guide explains how to automate the deployment of an AWS Lambda function using GitHub Actions. This setup allows your function to be updated automatically whenever you push changes to your GitHub repository.

## What is this for?

AWS Lambda is a serverless compute service that runs your code in response to events.

GitHub Actions is a CI/CD (Continuous Integration/Continuous Deployment) tool that automates workflows, like deploying your code.

This guide will show you how to deploy your AWS Lambda function automatically whenever you push code to GitHub.

## Prerequisites

Before starting, ensure you have:

* A GitHub account ([Sign up](https://github.com))
* An AWS account ([Sign up](https://aws.amazon.com))

## Step 1: Set Up AWS Lambda

### Create an AWS Lambda Function

1. Go to AWS Lambda Console
2. Click **Create function**
3. Choose **Author from scratch**
4. Set the function name (e.g., `myLambdaFunction`)
5. Choose **Python 3.x** as the runtime
6. Under Permissions, choose **Create a new role with basic Lambda permissions**
7. Click **Create function**

### Find Your Function & Region

1. Go to AWS Lambda Console
2. Click on your function
3. Check the region in the top-right corner (e.g., `us-east-1`)

## Step 2: Set Up IAM User & Permissions

### Create an IAM User for GitHub Actions

1. Go to AWS IAM Console
2. Click **Users** → **Add user**
3. Set the name (e.g., `GitHubActionsUser`)
4. Choose **Programmatic access**
5. Click **Next** and attach `AWSLambdaFullAccess`
6. Click **Create user** and download the Access Key & Secret Key

### Store AWS Credentials in GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:
   * `AWS_ACCESS_KEY_ID` → (Your AWS Access Key ID)
   * `AWS_SECRET_ACCESS_KEY` → (Your AWS Secret Access Key)

## Step 3: Set Up GitHub Actions Workflow

### Create the GitHub Actions Workflow File

1. In your GitHub repo, go to the `/.github/workflows/` directory (or create it if it doesn't exist)
2. Create a new file named `deploy-lambda.yml`
3. Add the following content:

```yaml
name: Deploy AWS Lambda

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1  # Change this to match your AWS region

      - name: Zip the Lambda function
        run: zip function.zip lambda_function.py

      - name: Deploy Lambda function
        run: |
          aws lambda update-function-code \
            --function-name myLambdaFunction \
            --zip-file fileb://function.zip
```

### Commit and Push the Workflow

Add and commit the workflow file:

```bash
git add .github/workflows/deploy-lambda.yml
git commit -m "Added GitHub Actions for AWS Lambda"
git push origin main
```

## Step 4: Deploy and Test

### Push Code Changes to Trigger Deployment

Whenever you update `lambda_function.py` and push the changes to GitHub, the GitHub Actions workflow will automatically deploy your function.

### Test the Lambda Function in AWS

1. Go to AWS Lambda Console
2. Click on your function `myLambdaFunction`
3. Click **Test**
4. Create a test event (default settings are fine)
5. Click **Test** again to execute the function

Check the response. If successful, you should see:

```json
{
    "statusCode": 200,
    "body": "AWS Lambda Updated via GitHub Actions!"
}
```

## Summary

### What We Did

* Created an AWS Lambda function
* Set up IAM permissions & GitHub Secrets
* Configured GitHub Actions for deployment
* Successfully deployed AWS Lambda via GitHub Actions
* Tested and confirmed that deployments work

Now, every time you push a change to GitHub, your AWS Lambda function will be updated automatically.

## FAQ

### How do I update my Lambda function?

Just edit `lambda_function.py` and push the changes to GitHub. GitHub Actions will automatically redeploy the function.

### What if the deployment fails?

* Check GitHub Actions logs for errors
* Ensure your IAM user has `AWSLambdaFullAccess`
* Make sure your AWS region is correct

### Can I use other runtimes (Node.js, Java, etc.)?

Yes. Just change the runtime in AWS Lambda and update the function code accordingly.

## Next Steps

* Add more functionality to your Lambda function
* Automate deployments for multiple Lambda functions
* Integrate with AWS API Gateway or other AWS services

Now you can easily deploy AWS Lambda with GitHub Actions.
