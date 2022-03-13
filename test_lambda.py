import os
# fake environment variables
os.environ["TableName"] = "DynamoDB-Table-CFNExample"
os.environ["KeyName"] = "itemId"

# === FOR TESTING PERPOSE === #
# Change the profile of the default session in code
# Ref: https://stackoverflow.com/questions/33378422/how-to-choose-an-aws-profile-when-using-boto3-to-connect-to-cloudfront
import boto3
boto3.setup_default_session(profile_name='tvt_admin')

# should import lambda code after fake environment variables
import lambda_function as fn

if __name__ == '__main__':
    response = fn.lambda_handler(event={}, context={})
    print(response)