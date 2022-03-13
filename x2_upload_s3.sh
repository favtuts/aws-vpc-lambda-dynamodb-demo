export LAMBDA_ZIP='vpc-lambda-dynamodb-demo-2022031301.zip'
export SERVICE_S3_BUCKET='tvt-artifacts-bucket'

aws s3 cp $LAMBDA_ZIP s3://$SERVICE_S3_BUCKET/lambdas/$LAMBDA_ZIP --profile tvt_admin
echo "Use CFN stack to deploy Lambda from s3://$SERVICE_S3_BUCKET/lambdas/$LAMBDA_ZIP"