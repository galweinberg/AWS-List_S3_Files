# DevOps Assignment – AWS  Project

This project defines and deploys a simple serverless application using **AWS CDK (Python)**. It uses **Lambda**, **S3**, and **SNS**, with all infrastructure managed as code and deployed through **GitHub Actions**.

***It is important to mention that without inserting AWS secret to GitHub, and also adding your email to secrets as `NOTIFY_EMAIL` , it will not work well.***

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
  
  ***(all above are under devops_assignment in the project)***

- **GitHub Actions** (CI/CD)
  
  ***(under .github/workflows)***


---

# Setup and Deployment

> You’ll need AWS credentials (access key, secret, account ID) and an available email to deploy.

### 1. Install dependencies

pip install -r requirements.txt
npm install -g aws-cdk

### 2. Configure AWS Locally (optional, for manual deploy)

### In your console:

aws configure

Then enter:

- AWS Access Key ID

- AWS Secret Access Key

- Default region (e.g., us-east-1)

This allows you to use cdk bootstrap and cdk deploy locally.

### 3. Set Up GitHub Secrets

In your GitHub repo:

- Go to Settings → Secrets and variables → Actions

- Click New repository secret

 Add the following secrets:


- `AWS_ACCESS_KEY_ID` — Your access key ID
  
- `AWS_SECRET_ACCESS_KEY` — Your secret access key
  
- `AWS_ACCOUNT_ID` — Your 12-digit AWS Account ID  

These are required for the GitHub Actions deployment.



### 4. Replace SNS Email

In addition to AWS credentials, add the following GitHub secret:

- `NOTIFY_EMAIL` — The email address to receive SNS notifications. Must be confirmed via email after deployment.

<img width="1563" height="412" alt="image" src="https://github.com/user-attachments/assets/08c889a9-754b-441c-9f12-8bf845ce70b0" />


✅ Important: After deployment, you will receive an email from AWS SNS — click "Confirm subscription" to start receiving notifications.

### 5. Bootstrap CDK (first time only)

***cdk bootstrap***

### 6. Deploy manually

***cdk deploy***

this will

- Create the S3 bucket

- Upload files from sample_files/

- Deploy both Lambda functions

- Set up the SNS topic and subscription

## GitHub Actions CI/CD
The project includes a deployment workflow at .github/workflows/deploy.yml.

To run it:

### Only after adding the secrets to GitHub:

Trigger the deploy:

Go to the Actions tab

Select the Deploy workflow

Click Run workflow


# 🔍 Main AWS Components (Explanation)


## 🔐 IAM Role

The main Lambda function uses a dedicated IAM role with least-privilege permissions:

- Basic Lambda execution 

- Read access to the specific S3 bucket 

- Permission to publish messages to the SNS topic 

This is defined in the CDK.


## 🪣 Amazon S3
The stack creates a new versioned S3 bucket where files from sample_files/ are uploaded during deployment.


- Files are uploaded by the helper Lambda function

- Bucket is set to auto-delete on stack destruction (for testing/demo use)



## 📝 AWS Lambda
There are two Lambda functions in the project:

### Main Lambda (main_lambda.py)

- Lists all objects in the S3 bucket

- Sends the object list via SNS email notification


### Helper Lambda (upload_files.py)

- Uploads local files from sample_files/ to the bucket at deployment time

- Triggered automatically using a CDK CustomResource

- Both functions are written in Python and defined as part of the CDK stack


## 📬 SNS Subscription (Email)
SNS is used to send an email listing the files in the S3 bucket.

it should look like that:

<img width="1562" height="233" alt="image" src="https://github.com/user-attachments/assets/d06ab852-2e80-4061-9a2c-54a7e7dfa936" />


### Remember to update the email as a secret and confirm the subscription when prompted by AWS.



## 📂 Files Uploaded to S3 on Deploy
During deployment, a helper Lambda (upload_files.py) uploads everything in the sample_files/ folder to the S3 bucket.

Examples:

checkcheck.txt

heyWorld.txt

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
- SNS topic with email subscription	✅ 
- Upload files to S3 during deploy	✅
- GitHub Actions workflow for deployment	✅
- Manual Lambda trigger method (script)	✅
- README with all required sections	✅

### Notes
All secrets are handled via GitHub Secrets — none are committed to the repo.

SNS requires email confirmation after first deploy.

This project is designed to work with the AWS Free Tier.

x
