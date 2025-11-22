import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomersTable')

def lambda_handler(event, context):
    tenantId = event["queryStringParameters"].get("tenantId", "kfc")
    customerId = event["pathParameters"]["customerId"]

    response = table.get_item(
        Key={
            "tenantId": tenantId,
            "customerId": customerId
        }
    )

    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Customer not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response["Item"])
    }
