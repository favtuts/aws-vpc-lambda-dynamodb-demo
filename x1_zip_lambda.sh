export ZIP_FILE='vpc-lambda-dynamodb-demo.zip'
export PYTHON_VERSION='python3.7'
export VIRTUALENV='venv-lambda'

# Clean up
rm -fr $VIRTUALENV
rm $ZIP_FILE

# Setup fresh virtualenv and install requirements
virtualenv $VIRTUALENV --python=$PYTHON_VERSION
source $VIRTUALENV/bin/activate
pip install -r requirements-lambda.txt
deactivate

# Zip dependencies from virtualenv, and lambda_function.py
cd $VIRTUALENV/lib/$PYTHON_VERSION/site-packages/
zip -r9 ../../../../$ZIP_FILE *
cd ../../../../
zip -g $ZIP_FILE lambda_function.py