# AWS Resource Automation Using Python and Boto3

A Python-based command-line application for automating common AWS resource management tasks across Amazon S3 and Amazon EC2 using Boto3.

**Project Type:** AWS Cloud Automation
**Language:** Python
**AWS Region:** Asia Pacific (Mumbai) — `ap-south-1`
**Repository:** [Project-2-AWS-Automation](https://github.com/kunal-codes-001/Project-2-AWS-Automation)

---

## Table of Contents

* [Project Overview](#project-overview)
* [Objectives](#objectives)
* [Technologies and AWS Services](#technologies-and-aws-services)
* [Architecture](#architecture)
* [Features](#features)
* [Project Structure](#project-structure)
* [AWS Configuration](#aws-configuration)
* [S3 Automation](#s3-automation)
* [EC2 Automation](#ec2-automation)
* [Screenshots](#screenshots)
* [Installation and Setup](#installation-and-setup)
* [Running the Application](#running-the-application)
* [Security Practices](#security-practices)
* [Testing Results](#testing-results)
* [Key Learnings](#key-learnings)
* [Future Improvements](#future-improvements)
* [Conclusion](#conclusion)

---

## Project Overview

Managing AWS resources manually through the AWS Management Console can involve repetitive tasks. This project demonstrates how Python and Boto3 can be used to automate common AWS operations through a menu-driven command-line interface (CLI).

The application provides functionality for Amazon S3 bucket and file operations, as well as Amazon EC2 instance management. It uses an AWS CLI profile to establish a Boto3 session and communicate with AWS services.

This project provides hands-on experience with Python scripting, AWS SDK integration, cloud resource management, IAM permissions, and AWS CLI configuration.

## Objectives

* Automate common AWS resource operations using Python.
* Use Boto3 to interact with AWS services programmatically.
* Create and list Amazon S3 buckets.
* Upload files to Amazon S3 and list stored objects.
* List and manage Amazon EC2 instances.
* Use AWS IAM to manage access permissions.
* Configure AWS CLI profiles for authentication.
* Build a simple, menu-driven automation tool.
* Practice basic cloud security and credential management.

## Technologies and AWS Services

| Technology or Service               | Purpose                                  |
| ----------------------------------- | ---------------------------------------- |
| Python 3                            | Application logic and automation         |
| Boto3                               | Python SDK for AWS service interactions  |
| AWS CLI                             | AWS profile and credential configuration |
| Amazon S3                           | Bucket and object management             |
| Amazon EC2                          | Virtual machine lifecycle management     |
| AWS IAM                             | Identity and access management           |
| Windows PowerShell / Command Prompt | Development and execution environment    |
| Git and GitHub                      | Version control and source code hosting  |

## Architecture

The application follows a simple architecture in which a user selects an operation from the CLI. Python processes the selection, and Boto3 sends API requests to AWS.

```text
                  USER
                    |
                    v
             Python CLI Tool
                    |
                    v
                 Boto3 SDK
                    |
                    v
              AWS API Requests
                    |
             +------+------+
             |             |
             v             v
         Amazon S3      Amazon EC2
             |             |
       Buckets/Files   EC2 Instances
```

**Architecture flow:**

1. The user selects an operation from the CLI menu.
2. Python executes the corresponding function.
3. Boto3 uses the configured AWS profile and region.
4. AWS receives the request and checks the relevant IAM permissions.
5. The application displays the operation result.

## Features

### Amazon S3 Automation

* Create an S3 bucket.
* List available S3 buckets.
* Upload a local file to an S3 bucket.
* List objects stored in an S3 bucket.
* Check whether the required project bucket exists.

### Amazon EC2 Automation

* List EC2 instances.
* Launch an EC2 instance.
* Start a stopped EC2 instance.
* Stop a running EC2 instance.
* Terminate an EC2 instance.
* Find the project instance using its Name tag.

### Project Information

The application can display configuration information such as:

* Project name
* Python and SDK information
* AWS region
* S3 bucket name
* EC2 AMI and instance type
* VPC, subnet, and security group information

The availability of individual configuration details depends on the application implementation and AWS resources.

## Project Structure

```text
Project-2-AWS-Automation/
│
├── aws_automation.py
├── README.md
├── requirements.txt
├── .gitignore
├── commands_forun_project.txt
├── test_aws.py
│
├── sample/
│   └── test.txt
│
└── screenshots/
    ├── 01-cli-menu.png
    ├── 02-s3-bucket.png
    ├── 03-s3-upload.png
    ├── 04-s3-files.png
    ├── 05-ec2-launch.png
    ├── 06-ec2-stop.png
    ├── 07-ec2-start.png
    ├── 08-ec2-terminate.png
    └── 09-project-info.png
```

The `venv/` directory is excluded from version control because each developer can create their own local Python environment.

## AWS Configuration

The project uses a dedicated AWS CLI profile:

```text
aws-capstone
```

The configured AWS region is:

```text
ap-south-1
```

This is the Asia Pacific (Mumbai) AWS Region.

The application creates a Boto3 session using the configured profile and region:

```python
session = boto3.Session(
    profile_name="aws-capstone",
    region_name="ap-south-1"
)
```

This allows the application to use the selected AWS profile instead of embedding AWS credentials directly in the Python source code.

## IAM Configuration

The project configuration uses the following IAM resources:

| Resource   | Name                             |
| ---------- | -------------------------------- |
| IAM User   | `aws-capstone-automation`        |
| IAM Group  | `aws-capstone-automation-group`  |
| IAM Policy | `AWS-Capstone-Automation-Policy` |

The IAM policy is intended to provide permissions for the S3 and EC2 operations performed by the application.

For production use, review the policy to ensure it grants only the permissions and resource access required by the application. Avoid broad permissions where narrower permissions are possible.

## S3 Automation

The application demonstrates common S3 operations using Boto3.

**Configured project bucket:**

```text
aws-capstone-automation-2026-001
```

### File Upload

The application uploads a sample file from the local project directory:

```text
sample/test.txt
```

The file is uploaded to S3 with the object key `test.txt`.

Example Boto3 operation:

```python
s3.upload_file(
    file_path,
    bucket_name,
    "test.txt"
)
```

### S3 Operations Demonstrated

* Checking for the required bucket.
* Creating a bucket when requested.
* Listing S3 buckets.
* Uploading a local file.
* Listing objects stored in the bucket.

Example output:

```text
File uploaded successfully!

File: sample/test.txt
S3 Bucket: aws-capstone-automation-2026-001
```

Example object listing:

```text
Files in S3 bucket:
--------------------
test.txt
```

The bucket must exist in the appropriate region, and the configured AWS identity must have the necessary permissions.

## EC2 Automation

The application uses Boto3 to manage EC2 instances programmatically.

### EC2 Configuration

| Setting            | Value             |
| ------------------ | ----------------- |
| Instance Type      | `t3.micro`        |
| Operating System   | Amazon Linux 2023 |
| AWS Region         | `ap-south-1`      |
| Instance Selection | Name tag          |

### Supported Operations

| Operation          | Description                            |
| ------------------ | -------------------------------------- |
| List Instances     | Retrieve EC2 instance information      |
| Launch Instance    | Request a new EC2 instance             |
| Start Instance     | Start a stopped instance               |
| Stop Instance      | Stop a running instance                |
| Terminate Instance | Request permanent instance termination |

### Dynamic EC2 Instance Selection

The application can identify the project instance using its Name tag:

```text
aws-capstone-automation-ec2
```

This reduces the need to enter an instance ID manually when selecting the configured project instance.

Example output:

```text
Selected EC2 instance: i-0019a1c9bff31e04f
```

The instance must exist and be discoverable using the application's configured selection logic.

### EC2 Lifecycle

The demonstrated lifecycle operations include:

```text
Running
   |
   v
 Stop Instance
   |
   v
Stopped
   |
   v
 Start Instance
   |
   v
Running
   |
   v
Terminate Instance
   |
   v
Terminated
```

**Cost and safety note:** EC2 termination is a destructive action. Verify the selected instance ID before confirming termination. Stopping an instance does not necessarily eliminate all associated costs, such as applicable EBS storage charges.

## Screenshots

The following screenshots document the application's CLI and AWS operations.

### 1. CLI Menu

![AWS Automation CLI Menu](https://github.com/kunal-codes-001/Project-2-AWS-Automation/raw/main/screenshots/01-cli-menu.png)

[View CLI Menu](https://github.com/kunal-codes-001/Project-2-AWS-Automation/blob/main/screenshots/01-cli-menu.png)

### 2. S3 Bucket

![S3 Bucket](https://github.com/kunal-codes-001/Project-2-AWS-Automation/raw/main/screenshots/02-s3-bucket.png)

[View S3 Bucket Screenshot](https://github.com/kunal-codes-001/Project-2-AWS-Automation/blob/main/screenshots/02-s3-bucket.png)

### 3. S3 File Upload

![S3 File Upload](https://github.com/kunal-codes-001/Project-2-AWS-Automation/raw/main/screenshots/03-s3-upload.png)

[View S3 Upload Screenshot](https://github.com/kunal-codes-001/Project-2-AWS-Automation/blob/main/screenshots/03-s3-upload.png)

### 4. S3 Files

![S3 Files](https://github.com/kunal-codes-001/Project-2-AWS-Automation/raw/main/screenshots/04-s3-files.png)

[View S3 Files Screenshot](https://github.com/kunal-codes-001/Project-2-AWS-Automation/blob/main/screenshots/04-s3-files.png)

### 5. EC2 Launch

![EC2 Launch](https://github.com/kunal-codes-001/Project-2-AWS-Automation/raw/main/screenshots/05-ec2-launch.png)

[View EC2 Launch Screenshot](https://github.com/kunal-codes-001/Project-2-AWS-Automation/blob/main/screenshots/05-ec2-launch.png)

### 6. EC2 Stop

![EC2 Stop](https://github.com/kunal-codes-001/Project-2-AWS-Automation/raw/main/screenshots/06-ec2-stop.png)

[View EC2 Stop Screenshot](https://github.com/kunal-codes-001/Project-2-AWS-Automation/blob/main/screenshots/06-ec2-stop.png)

### 7. EC2 Start

![EC2 Start](https://github.com/kunal-codes-001/Project-2-AWS-Automation/raw/main/screenshots/07-ec2-start.png)

[View EC2 Start Screenshot](https://github.com/kunal-codes-001/Project-2-AWS-Automation/blob/main/screenshots/07-ec2-start.png)

### 8. EC2 Termination

![EC2 Termination](https://github.com/kunal-codes-001/Project-2-AWS-Automation/raw/main/screenshots/08-ec2-terminate.png)

[View EC2 Termination Screenshot](https://github.com/kunal-codes-001/Project-2-AWS-Automation/blob/main/screenshots/08-ec2-terminate.png)

### 9. Project Information

![Project Information](https://github.com/kunal-codes-001/Project-2-AWS-Automation/raw/main/screenshots/09-project-info.png)

[View Project Information Screenshot](https://github.com/kunal-codes-001/Project-2-AWS-Automation/blob/main/screenshots/09-project-info.png)

## Installation and Setup

### Prerequisites

Before running the application, make sure you have:

* Python 3 installed.
* Git installed.
* AWS CLI installed.
* An AWS account with the required permissions.
* An AWS CLI profile configured for this project.

### Step 1: Clone the Repository

```bash
git clone https://github.com/kunal-codes-001/Project-2-AWS-Automation.git
```

Navigate to the project directory:

```bash
cd Project-2-AWS-Automation
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## AWS CLI Configuration

Configure the dedicated AWS CLI profile:

```bash
aws configure --profile aws-capstone
```

Enter the appropriate AWS access key ID, secret access key, default region (`ap-south-1`), and output format when prompted.

Verify the AWS identity:

```bash
aws sts get-caller-identity --profile aws-capstone
```

The command should return the AWS account and identity information associated with the configured credentials.

Use credentials only for the intended AWS account and follow your organization's credential management practices. Never paste credentials into source code, README files, screenshots, or public repositories.

## Running the Application

After installing the dependencies and configuring the AWS profile, run:

```bash
python aws_automation.py
```

The application displays a menu similar to the following:

```text
========================================
         AWS AUTOMATION TOOL
========================================

1. Create S3 Bucket
2. List S3 Buckets
3. Upload File to S3
4. List S3 Files
5. List EC2 Instances
6. Launch EC2 Instance
7. Start EC2 Instance
8. Stop EC2 Instance
9. Terminate EC2 Instance
10. Show Project Information
11. Exit

========================================
```

Enter the menu number corresponding to the operation you want to perform.

Available operations depend on the AWS profile, IAM permissions, resource configuration, and implementation of the application.

## Security Practices

The project incorporates the following security considerations:

* Uses an AWS CLI profile instead of hardcoding credentials in the Python source.
* Excludes `.env` files from version control.
* Excludes `.pem` files from version control.
* Excludes local AWS configuration directories.
* Excludes the local Python virtual environment.
* Uses IAM identities and policies for access control.
* Uses a configurable AWS region.
* Keeps local credentials separate from application code.

These exclusions help reduce the risk of accidentally committing sensitive files, but they do not guarantee that all secrets are absent. Review files, screenshots, commit history, and IAM permissions before making a repository public.

For production deployments, consider IAM roles and temporary credentials instead of long-lived IAM user access keys.

## Testing Results

The project documentation records the following operations as successfully tested:

| Operation                   | Documented Result |
| --------------------------- | ----------------- |
| S3 bucket check             | Successful        |
| S3 bucket listing           | Successful        |
| S3 file upload              | Successful        |
| S3 object listing           | Successful        |
| EC2 instance listing        | Successful        |
| EC2 instance selection      | Successful        |
| EC2 stop                    | Successful        |
| EC2 start                   | Successful        |
| EC2 termination             | Successful        |
| Project information display | Successful        |

These results reflect the documented project tests. Results may vary depending on the current AWS account configuration, permissions, resource availability, and region.

## Key Learnings

Through this project, I gained practical experience with:

* Python-based AWS automation.
* Using Boto3 to interact with AWS services.
* Automating Amazon S3 bucket and object operations.
* Managing the EC2 instance lifecycle programmatically.
* Configuring AWS CLI profiles and Boto3 sessions.
* Understanding IAM identities, policies, and permissions.
* Building a menu-driven command-line application.
* Organizing code and project documentation with Git and GitHub.
* Applying basic security practices to cloud automation projects.

## Future Improvements

Potential enhancements include:

* Add structured logging for AWS operations.
* Improve error handling for AWS API failures.
* Add confirmation prompts for destructive operations.
* Add EC2 status monitoring.
* Support multiple S3 buckets and configurable resources.
* Add command-line arguments for non-interactive execution.
* Add automated tests using mocked AWS responses.
* Extend automation to services such as AWS Lambda and Amazon DynamoDB.
* Integrate automated checks into a CI/CD workflow.

## Conclusion

This project demonstrates how Python and Boto3 can simplify common AWS resource management tasks through a command-line application.

By integrating Amazon S3, Amazon EC2, AWS IAM, and AWS CLI configuration, the project provides practical experience in cloud automation and AWS SDK usage.

It serves as a foundation for further learning in AWS, DevOps, infrastructure automation, and cloud engineering.

---

**GitHub Repository:** [AWS Resource Automation Using Python and Boto3](https://github.com/kunal-codes-001/Project-2-AWS-Automation)
