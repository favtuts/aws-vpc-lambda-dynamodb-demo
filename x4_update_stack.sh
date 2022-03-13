export CF_STACK_NAME='vpc-lambda-dynamodb-demo-stack'
export CF_TEMPLATE_FILE=file://$(pwd)/cloudformation.yml

aws cloudformation update-stack \
    --stack-name $CF_STACK_NAME \
    --template-body $CF_TEMPLATE_FILE \
    --capabilities CAPABILITY_NAMED_IAM \
    --profile tvt_admin

aws cloudformation wait \
    stack-update-complete \
    --stack-name $CF_STACK_NAME \
    --profile tvt_admin