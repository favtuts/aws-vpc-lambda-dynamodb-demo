# aws-vpc-lambda-dynamodb-demo
Demo for blog: https://www.favtuts.com/how-to-access-dynamodb-from-aws-lambda-inside-vpc/

# lambda development

## setup virtual environment

Install virtualvenv
```
pip install virtualenv
```

Create and active virtual environment
```
cd <root-project-dir>
virtualenv venv --python=python3.7
source venv/bin/activate
```

Check python runtime version
```
(venv) > which python
(venv) > python --version
```

You can deactivate the environment after finishing your work
```
(venv) > deactivate
```

Delete venv folder
```
rm -r venv
```

## install dependencies

Install packages
```
(venv) > pip install python-json-logger
(venv) > pip install boto3
```

Export `requirements.txt` file
```
(venv) > pip freeze > requirements.txt
```

Quickly install packages from existed requirements.txt file
```
(venv) > pip install -r requirements.txt
```

# Lambda test and debug

To test or debug my lambda:
```
(venv) python test_lambda.py
```

# Lambda packaging

We copy another `requirements-lambda.txt` for neccessary-only packages on AWS

Set execute permission for my scripts
```
chmod +x x1_zip_lambda.sh
chmod +x x2_upload_s3.sh
chmod +x x3_create_stack.sh
```

Run this command to create Zip file
```
./x1_zip_lambda.sh
sh x1_zip_lambda
bash x1_zip_lambda
```

After we have zip file for lambda, we need to upload to S3 Bucket
```
./x2_upload_s3.sh
```

# Lambda deployment

To create new stack
```
./x3_create_stack.sh
```

Or run CLI commands: 
```
aws cloudformation create-stack \
    --stack-name 'vpc-lambda-dynamodb-demo-stack' \
    --template-body file://$(pwd)/cf.simple-scenario.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --profile tvt_admin

aws cloudformation wait \
    stack-create-complete \
    --stack-name 'vpc-lambda-dynamodb-demo-stack'
    --profile tvt_admin
```

To update changes to stack
```
aws cloudformation update-stack \
    --stack-name 'vpc-lambda-dynamodb-demo-stack' \
    --template-body file://$(pwd)/cf.simple-scenario.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --profile tvt_admin
```

To delete stack and clean up everything, run the following command:

```
aws cloudformation delete-stack \
    --stack-name 'vpc-lambda-dynamodb-demo-stack' \
    --profile tvt_admin
```


# Test Lambda

We can invoke the function manually to test it works:

```
aws lambda invoke --function-name Lambda-DynamoDB-Function-CFNExample --payload '{"null": "null"}' lambda-output.txt --cli-binary-format raw-in-base64-out --profile tvt_admin
```

```
aws lambda invoke --function-name Lambda-DynamoDB-Function-CFNExample \
    --invocation-type RequestResponse \
    --payload fileb://lambda-input.json \
    --profile tvt_admin \
    lambda-output.txt
```