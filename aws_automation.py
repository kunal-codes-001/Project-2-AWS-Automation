import boto3


# ============================================================
# AWS SESSION
# ============================================================

session = boto3.Session(
    profile_name="aws-capstone",
    region_name="ap-south-1"
)

s3 = session.client("s3")
ec2 = session.client("ec2")


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

bucket_name = "aws-capstone-automation-2026-001"

file_path = "sample/test.txt"

# Latest EC2 instance created by this program
instance_id = None

# Default VPC
vpc_id = "vpc-0b6cf5c83832d81ee"

# Subnet in ap-south-1a
subnet_id = "subnet-0d9165ddc7e18de13"

# Default security group
security_group_id = "sg-0c65688a0abac6252"

# Amazon Linux 2023 AMI
ami_id = "ami-01e28c444f355e81e"

# Instance type
instance_type = "t3.micro"


# ============================================================
# 1. CREATE S3 BUCKET
# ============================================================

def create_s3_bucket():

    print("\nCreate S3 Bucket")
    print("--------------------")
    print("Bucket Name:", bucket_name)

    try:

        s3.head_bucket(
            Bucket=bucket_name
        )

        print("Bucket already exists!")
        print("Bucket:", bucket_name)

    except Exception:

        try:

            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": "ap-south-1"
                }
            )

            print("S3 bucket created successfully!")
            print("Bucket:", bucket_name)

        except Exception as e:

            print("Could not create S3 bucket.")
            print("Error:", e)


# ============================================================
# 2. LIST S3 BUCKETS
# ============================================================

def list_s3_buckets():

    print("\nS3 Buckets:")
    print("--------------------")

    try:

        response = s3.list_buckets()

        buckets = response.get(
            "Buckets",
            []
        )

        if not buckets:

            print("No S3 buckets found.")
            return

        for bucket in buckets:

            print(bucket["Name"])

    except Exception as e:

        print("Could not list S3 buckets.")
        print("Error:", e)


# ============================================================
# 3. UPLOAD FILE TO S3
# ============================================================

def upload_file_to_s3():

    print("\nUploading file to S3...")
    print("--------------------")

    try:

        s3.upload_file(
            file_path,
            bucket_name,
            "test.txt"
        )

        print("File uploaded successfully!")
        print("File:", file_path)
        print("S3 Bucket:", bucket_name)

    except Exception as e:

        print("Upload failed!")
        print("Error:", e)


# ============================================================
# 4. LIST FILES IN S3
# ============================================================

def list_s3_files():

    print("\nFiles in S3 bucket:")
    print("--------------------")

    try:

        response = s3.list_objects_v2(
            Bucket=bucket_name
        )

        contents = response.get(
            "Contents",
            []
        )

        if not contents:

            print("No files found.")
            return

        for obj in contents:

            print(obj["Key"])

    except Exception as e:

        print("Could not list S3 files.")
        print("Error:", e)


# ============================================================
# 5. LIST EC2 INSTANCES
# ============================================================

def list_ec2_instances():

    print("\nEC2 Instances:")
    print("--------------------")

    try:

        response = ec2.describe_instances()

        found = False

        for reservation in response["Reservations"]:

            for instance in reservation["Instances"]:

                found = True

                print(
                    f"Instance ID: {instance['InstanceId']} "
                    f"| State: {instance['State']['Name']} "
                    f"| Type: {instance['InstanceType']}"
                )

        if not found:

            print("No EC2 instances found.")

    except Exception as e:

        print("Could not list EC2 instances.")
        print("Error:", e)


# ============================================================
# 6. LAUNCH EC2 INSTANCE
# ============================================================

def launch_ec2_instance():

    global instance_id

    print("\nLaunch EC2 Instance")
    print("--------------------")

    print("AMI:", ami_id)
    print("Instance Type:", instance_type)
    print("Subnet:", subnet_id)
    print("Security Group:", security_group_id)

    confirmation = input(
        "\nDo you want to launch a new EC2 instance? (yes/no): "
    )

    if confirmation.lower() != "yes":

        print("Launch cancelled.")
        return

    try:

        response = ec2.run_instances(

            ImageId=ami_id,

            InstanceType=instance_type,

            MinCount=1,

            MaxCount=1,

            SubnetId=subnet_id,

            SecurityGroupIds=[
                security_group_id
            ],

            TagSpecifications=[
                {
                    "ResourceType": "instance",

                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "aws-capstone-automation-ec2"
                        }
                    ]
                }
            ]
        )

        new_instance = response["Instances"][0]

        new_instance_id = new_instance["InstanceId"]

        # Remember the newly created instance
        instance_id = new_instance_id

        print("\nEC2 instance launch request sent successfully!")

        print(
            "New Instance ID:",
            new_instance_id
        )

        print(
            "Initial State:",
            new_instance["State"]["Name"]
        )

        print("\nWaiting for EC2 instance to start...")

        waiter = ec2.get_waiter(
            "instance_running"
        )

        waiter.wait(
            InstanceIds=[
                new_instance_id
            ]
        )

        print("EC2 instance is now running!")

        print(
            "Instance ID:",
            new_instance_id
        )

        print(
            "Python is now managing this instance."
        )

    except Exception as e:

        print("\nEC2 launch failed!")
        print("Error:", e)


# ============================================================
# CHECK INSTANCE ID
# ============================================================
def check_instance_id():

    global instance_id

    if instance_id is not None:
        return True

    try:

        response = ec2.describe_instances(
            Filters=[
                {
                    "Name": "tag:Name",
                    "Values": ["aws-capstone-automation-ec2"]
                }
            ]
        )

        for reservation in response["Reservations"]:

            for instance in reservation["Instances"]:

                state = instance["State"]["Name"]

                if state in ["running", "stopped", "stopping", "pending"]:

                    instance_id = instance["InstanceId"]

                    print(
                        "Selected EC2 instance:",
                        instance_id
                    )

                    return True

        print("\nNo active automation EC2 instance found.")
        print("Please use option 6 to launch an EC2 instance.")

        return False

    except Exception as e:

        print("Could not find EC2 instance.")
        print("Error:", e)

        return False


# ============================================================
# 7. START EC2 INSTANCE
# ============================================================

def start_ec2_instance():

    print("\nStarting EC2 instance...")
    print("--------------------")

    if not check_instance_id():
        return

    try:

        response = ec2.describe_instances(
            InstanceIds=[
                instance_id
            ]
        )

        current_state = response[
            "Reservations"
        ][0]["Instances"][0][
            "State"
        ]["Name"]

        print("Instance ID:", instance_id)
        print("Current State:", current_state)

        if current_state == "running":

            print("Instance is already running.")
            return

        if current_state == "pending":

            print("Instance is already starting.")
            return

        if current_state == "terminated":

            print("Instance is terminated.")
            print("Launch a new instance using option 6.")
            return

        ec2.start_instances(
            InstanceIds=[
                instance_id
            ]
        )

        print("Start request sent successfully!")

        print(
            "Instance ID:",
            instance_id
        )

        waiter = ec2.get_waiter(
            "instance_running"
        )

        waiter.wait(
            InstanceIds=[
                instance_id
            ]
        )

        print("Current State: running")

    except Exception as e:

        print("Could not start EC2 instance.")
        print("Error:", e)


# ============================================================
# 8. STOP EC2 INSTANCE
# ============================================================

def stop_ec2_instance():

    print("\nStopping EC2 instance...")
    print("--------------------")

    if not check_instance_id():
        return

    try:

        response = ec2.describe_instances(
            InstanceIds=[
                instance_id
            ]
        )

        current_state = response[
            "Reservations"
        ][0]["Instances"][0][
            "State"
        ]["Name"]

        print("Instance ID:", instance_id)
        print("Current State:", current_state)

        if current_state == "stopped":

            print("Instance is already stopped.")
            return

        if current_state == "stopping":

            print("Instance is already stopping.")
            return

        if current_state == "terminated":

            print("Instance is terminated.")
            print("Launch a new instance using option 6.")
            return

        ec2.stop_instances(
            InstanceIds=[
                instance_id
            ]
        )

        print("Stop request sent successfully!")

        print(
            "Instance ID:",
            instance_id
        )

        waiter = ec2.get_waiter(
            "instance_stopped"
        )

        waiter.wait(
            InstanceIds=[
                instance_id
            ]
        )

        print("Current State: stopped")

    except Exception as e:

        print("Could not stop EC2 instance.")
        print("Error:", e)


# ============================================================
# 9. TERMINATE EC2 INSTANCE
# ============================================================

def terminate_ec2_instance():

    global instance_id

    print("\nTerminate EC2 Instance")
    print("--------------------")

    if not check_instance_id():
        return

    print(
        "Instance ID:",
        instance_id
    )

    confirmation = input(
        "\nWARNING: This will permanently terminate "
        "the test instance.\n"
        "Type 'terminate' to continue: "
    )

    if confirmation.lower() != "terminate":

        print("Termination cancelled.")
        return

    try:

        response = ec2.describe_instances(
            InstanceIds=[
                instance_id
            ]
        )

        current_state = response[
            "Reservations"
        ][0]["Instances"][0][
            "State"
        ]["Name"]

        print("Current State:", current_state)

        if current_state == "terminated":

            print("Instance is already terminated.")
            return

        ec2.terminate_instances(
            InstanceIds=[
                instance_id
            ]
        )

        print("\nTermination request sent successfully!")

        print(
            "Instance ID:",
            instance_id
        )

        waiter = ec2.get_waiter(
            "instance_terminated"
        )

        waiter.wait(
            InstanceIds=[
                instance_id
            ]
        )

        print("Current State: terminated")

        # Clear the stored instance ID
        instance_id = None

        print(
            "Python instance selection cleared."
        )

    except Exception as e:

        print("Could not terminate EC2 instance.")
        print("Error:", e)


# ============================================================
# 10. PROJECT INFORMATION
# ============================================================

def show_project_info():

    print("\n========================================")
    print("        PROJECT INFORMATION")
    print("========================================")

    print("Project: AWS Resource Automation")
    print("Language: Python")
    print("SDK: boto3")
    print("Region: ap-south-1")

    print("\nAWS Services:")
    print("--------------------")
    print("Amazon S3")
    print("Amazon EC2")
    print("AWS IAM")

    print("\nS3 Bucket:")
    print(bucket_name)

    print("\nCurrent EC2 Instance:")
    
    if instance_id is None:
        print("No active Python-managed instance.")
    else:
        print(instance_id)

    print("\nAMI:")
    print(ami_id)

    print("\nInstance Type:")
    print(instance_type)

    print("\nVPC:")
    print(vpc_id)

    print("\nSubnet:")
    print(subnet_id)

    print("\nSecurity Group:")
    print(security_group_id)


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n========================================")
        print("        AWS AUTOMATION TOOL")
        print("========================================")

        print("1. Create S3 Bucket")
        print("2. List S3 Buckets")
        print("3. Upload File to S3")
        print("4. List S3 Files")
        print("5. List EC2 Instances")
        print("6. Launch EC2 Instance")
        print("7. Start EC2 Instance")
        print("8. Stop EC2 Instance")
        print("9. Terminate EC2 Instance")
        print("10. Show Project Information")
        print("11. Exit")

        print("========================================")

        choice = input("Enter your choice: ")

        if choice == "1":

            create_s3_bucket()

        elif choice == "2":

            list_s3_buckets()

        elif choice == "3":

            upload_file_to_s3()

        elif choice == "4":

            list_s3_files()

        elif choice == "5":

            list_ec2_instances()

        elif choice == "6":

            launch_ec2_instance()

        elif choice == "7":

            start_ec2_instance()

        elif choice == "8":

            stop_ec2_instance()

        elif choice == "9":

            terminate_ec2_instance()

        elif choice == "10":

            show_project_info()

        elif choice == "11":

            print("\nExiting AWS Automation Tool...")
            break

        else:

            print(
                "\nInvalid choice. Please select 1-11."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()