import lambda_function as fn

if __name__ == '__main__':
    response = fn.lambda_handler(event={}, context={})
    print(response)