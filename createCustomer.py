import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomersTable')

def lambda_handler(event, context):
    body = json.loads(event["body"])

    item = {
        "tenantId": body["tenantId"],
        "customerId": body["customerId"],
        "name": body.get("name", ""),
        "phone": body.get("phone", ""),
        "email": body.get("email", ""),
        "address": body.get("address", ""),
        "createdAt": int(time.time() * 1000)
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Customer created", "customer": item})
    }
