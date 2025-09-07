from lambda_universal_router import Router
from lambda_universal_router.events import APIGatewayEvent, SQSEvent, S3Event
import json

router = Router()

# API Gateway Examples
@router.apigateway("/users", method="GET")
def list_users(event: APIGatewayEvent, context):
    # Access query parameters
    page = event.query_string_parameters.get('page', '1')
    limit = event.query_string_parameters.get('limit', '10')
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "users": [{"id": 1, "name": "John"}],
            "page": page,
            "limit": limit
        })
    }

@router.apigateway("/users", method="POST")
def create_user(event: APIGatewayEvent, context):
    # Access request body
    user_data = json.loads(event.body)
    
    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "User created",
            "user": user_data
        })
    }

@router.apigateway("/users/{user_id}", method="GET")
def get_user(event: APIGatewayEvent, context):
    # Access path parameters
    user_id = event.path_parameters.get('user_id')
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "id": user_id,
            "name": "John Doe"
        })
    }

# SQS Example
@router.sqs()
def process_messages(event: SQSEvent, context):
    for message in event.records:
        # Access message attributes and body
        print(f"Processing message {message.message_id}")
        
        # Message body is a string - parse it if it's JSON
        try:
            payload = json.loads(message.body)
            print(f"Message payload: {payload}")
        except json.JSONDecodeError:
            print(f"Raw message: {message.body}")
        
        # Access message attributes
        for attr_name, attr_value in message.attributes.items():
            print(f"Attribute {attr_name}: {attr_value}")

# S3 Example
@router.s3()
def handle_s3_events(event: S3Event, context):
    for record in event.records:
        # Access bucket and object information
        bucket_name = record.bucket.name
        object_key = record.object.key
        object_size = record.object.size
        
        print(f"Event: {record.event_name}")
        print(f"Bucket: {bucket_name}")
        print(f"Key: {object_key}")
        print(f"Size: {object_size} bytes")
        
        if record.event_name.startswith('ObjectCreated:'):
            print(f"New object created: s3://{bucket_name}/{object_key}")
        elif record.event_name.startswith('ObjectRemoved:'):
            print(f"Object deleted: s3://{bucket_name}/{object_key}")

# Main Lambda handler
def lambda_handler(event, context):
    """
    Main Lambda handler that receives all events and routes them
    to the appropriate handler based on the event type.
    """
    return router.dispatch(event, context)
