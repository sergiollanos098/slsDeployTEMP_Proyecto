import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomersTable')

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        customer_id = body["customerId"]
        phone = body["phone"]

        # Buscar cliente
        response = table.get_item(
            Key={
                "tenantId": "kfc-peru",
                "customerId": customer_id
            }
        )

        if "Item" not in response:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Customer not found"})
            }

        customer = response["Item"]

        if customer["phone"] != phone:
            return {
                "statusCode": 401,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Invalid phone"})
            }

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            },
            "body": json.dumps({
                "message": "Login successful",
                "customer": customer
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
