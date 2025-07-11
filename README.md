# DevOps Assignment – AWS Serverless Project

This project defines and deploys a simple serverless application using **AWS CDK (Python)**. It uses **Lambda**, **S3**, and **SNS**, with all infrastructure managed as code and deployed through **GitHub Actions**.

***It is important to mention that without inserting AWS secret to GitHub, and changing subs.EmailSubscription("REPLACE_ME@example.com") into your email, it will not work well.***

---

## 📁 Contents (What’s Included)

- ✅ Infrastructure as Code (AWS CDK in Python)
- ✅ Lambda function to list S3 objects and send email via SNS
- ✅ Lambda to upload sample files to S3 during deployment
- ✅ `sample_files/` folder with sample S3 data
- ✅ GitHub Actions workflow for CI/CD
- ✅ Script for manually triggering the Lambda
- ✅ This README with setup and instructions

---

## 🧰 Tools Used

- **AWS CDK** (Infrastructure as Code)
- **AWS Lambda** (Python 3.9)
- **Amazon S3** (Object storage)
- **Amazon SNS** (Email notifications)
- **Boto3** (Manual test trigger)
  
 ***(all above are in devops_assignment in the project)***

- **GitHub Actions** (CI/CD)
  
  ***(under .github/workflows)***


---

## Setup and Deployment

> You’ll need AWS credentials (access key, secret, account ID) to deploy.

### 1. Install dependencies

pip install -r requirements.txt
npm install -g aws-cdk

### 2. Bootstrap CDK (first time only)

cdk bootstrap
### 3. Deploy manually

cdk deploy
## GitHub Actions CI/CD
The project includes a deployment workflow at .github/workflows/deploy.yml.

To run it:

### Add these GitHub secrets:

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_ACCOUNT_ID (your 12-digit AWS account ID)

Trigger the deploy:

Go to the Actions tab

Select the Deploy workflow

Click Run workflow

## SNS Subscription (Email)
SNS is used to send an email listing the files in the S3 bucket.

The subscription email is set as a placeholder:

subs.EmailSubscription("REPLACE_ME@example.com")
### Replace this with your own email and confirm the subscription when prompted by AWS.

## 📂 Files Uploaded to S3 on Deploy
During deployment, a helper Lambda (upload_files.py) uploads everything in the sample_files/ folder to the S3 bucket.

Examples:

checkcheck.txt

heyWrold.txt

This runs automatically during cdk deploy.

## Manual Lambda Trigger (Test)
You can test the main Lambda manually using the provided script.
***in the project - under tests/test_trigger_lambda***

### Option 1: Python + Boto3

python tests/test_trigger_lambda.py
This invokes the Lambda named ListS3Lambda and prints the list of S3 objects.

### Option 2: AWS CLI

aws lambda invoke \
  --function-name ListS3Lambda \
  --payload '{}' \
  response.json

## ✅ Checklist: Assignment Requirements
- Deliverable	Status
- GitHub repo with CDK IaC	✅
- Lambda function to list S3 + send SNS	✅
- SNS topic with email subscription	✅ (placeholder)
- Upload files to S3 during deploy	✅
- GitHub Actions workflow for deployment	✅
- Manual Lambda trigger method (script)	✅
- README with all required sections	✅

### Notes
All secrets are handled via GitHub Secrets — none are committed to the repo.

SNS requires email confirmation after first deploy.

This project is designed to work with the AWS Free Tier.

