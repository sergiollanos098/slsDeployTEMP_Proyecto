import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('OrdersTable')

def lambda_handler(event, context):
    tenantId = event["queryStringParameters"].get("tenantId", "kfc")
    orderId = event["pathParameters"]["orderId"]

    response = table.get_item(
        Key={
            "tenantId": tenantId,
            "orderId": orderId
        }
    )

    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Order not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response["Item"])
    }
