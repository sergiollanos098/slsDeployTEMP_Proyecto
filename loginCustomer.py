import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomersTable')

def lambda_handler(event, context):
    # DNI como customerId
    customerId = event["pathParameters"]["customerId"]

    # tenantId y phone vienen por querystring
    params = event.get("queryStringParameters", {}) or {}
    tenantId = params.get("tenantId", "kfc")
    phone = params.get("phone")

    if not phone:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Phone number is required"})
        }

    # Buscar cliente por DNI
    response = table.get_item(
        Key={
            "tenantId": tenantId,
            "customerId": customerId
        }
    )

    # Verificar si existe
    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Customer not found"})
        }

    customer = response["Item"]

    # Validar que el teléfono coincida
    if customer.get("phone") != phone:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Invalid phone number"})
        }

    # Login correcto
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Login successful",
            "customer": customer
        })
    }
