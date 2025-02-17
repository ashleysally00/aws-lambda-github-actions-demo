import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('🚀 AWS Lambda Updated via GitHub Actions!')
    }
