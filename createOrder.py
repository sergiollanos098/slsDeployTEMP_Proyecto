import json
import boto3
import time
import uuid

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('OrdersTable')
customers_table = dynamodb.Table('CustomersTable')

eventbridge = boto3.client('events')

def lambda_handler(event, context):
    body = json.loads(event["body"])

    tenantId = body["tenantId"]
    customerId = body["customerId"]

    # Validar si existe el cliente
    customer = customers_table.get_item(
        Key={"tenantId": tenantId, "customerId": customerId}
    )

    if "Item" not in customer:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Customer does not exist"})
        }

    orderId = "ORD-" + str(uuid.uuid4())[:8]

    item = {
        "tenantId": tenantId,
        "orderId": orderId,
        "customerId": customerId,
        "items": body["items"],
        "total": body["total"],
        "status": "created",
        "createdAt": int(time.time() * 1000)
    }

    orders_table.put_item(Item=item)

    # Emitir evento order.created a EventBridge
    eventbridge.put_events(
        Entries=[
            {
                "Source": "order.service",
                "DetailType": "order.created",
                "Detail": json.dumps(item)
            }
        ]
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Order created", "order": item})
    }
