# Examples

## API Gateway Examples

### REST API with Multiple Endpoints

```python
from lambda_universal_router import Router
from lambda_universal_router.events import APIGatewayEvent

router = Router()

@router.apigateway("/users", method="GET")
def list_users(event: APIGatewayEvent, context):
    page = event.query_string_parameters.get('page', '1')
    limit = event.query_string_parameters.get('limit', '10')
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {
            "users": [{"id": 1, "name": "John"}],
            "page": int(page),
            "limit": int(limit)
        }
    }

@router.apigateway("/users/{user_id}", method="GET")
def get_user(event: APIGatewayEvent, context):
    user_id = event.path_parameters['user_id']
    return {
        "statusCode": 200,
        "body": {"id": user_id, "name": "John Doe"}
    }

@router.apigateway("/users", method="POST")
def create_user(event: APIGatewayEvent, context):
    user_data = json.loads(event.body)
    return {
        "statusCode": 201,
        "body": {"message": "User created", "user": user_data}
    }
```

## Queue Processing Examples

### SQS Message Processing

```python
from lambda_universal_router import Router
from lambda_universal_router.events import SQSEvent

router = Router()

@router.sqs()
def process_orders(event: SQSEvent, context):
    for message in event.records:
        order = json.loads(message.body)
        print(f"Processing order {order['id']}")
        
        # Access message attributes
        priority = message.attributes.get('Priority')
        if priority == 'HIGH':
            process_priority_order(order)
        else:
            process_normal_order(order)
```

### Batch Processing with Error Handling

```python
@router.sqs()
def safe_process(event: SQSEvent, context):
    results = {
        "successful": [],
        "failed": []
    }
    
    for message in event.records:
        try:
            process_message(message)
            results["successful"].append(message.message_id)
        except Exception as e:
            results["failed"].append({
                "message_id": message.message_id,
                "error": str(e)
            })
    
    return results
```

## S3 Event Examples

### File Processing

```python
from lambda_universal_router import Router
from lambda_universal_router.events import S3Event

router = Router()

@router.s3()
def process_uploads(event: S3Event, context):
    for record in event.records:
        if record.event_name.startswith('ObjectCreated:'):
            bucket = record.bucket.name
            key = record.s3_object.key
            size = record.s3_object.size
            
            print(f"Processing new file: {key}")
            print(f"Size: {size} bytes")
            
            if key.endswith('.jpg'):
                process_image(bucket, key)
            elif key.endswith('.pdf'):
                process_document(bucket, key)
```

## DynamoDB Stream Examples

### Change Data Capture

```python
from lambda_universal_router import Router
from lambda_universal_router.events import DynamoDBStreamEvent

router = Router()

@router.dynamodb()
def sync_changes(event: DynamoDBStreamEvent, context):
    for record in event.records:
        table_name = record.dynamodb.get('TableName')
        
        if record.event_name == 'INSERT':
            handle_insert(record.dynamodb['NewImage'])
        elif record.event_name == 'MODIFY':
            handle_update(
                record.dynamodb['OldImage'],
                record.dynamodb['NewImage']
            )
        elif record.event_name == 'REMOVE':
            handle_delete(record.dynamodb['OldImage'])
```

## EventBridge Examples

### Scheduled Tasks

```python
from lambda_universal_router import Router
from lambda_universal_router.events import EventBridgeEvent

router = Router()

@router.eventbridge()
def daily_cleanup(event: EventBridgeEvent, context):
    if event.detail_type == "Scheduled Event":
        print(f"Running daily cleanup at {event.time}")
        cleanup_old_data()
```

## Custom Event Handler Example

### Fallback Handler

```python
from lambda_universal_router import Router
from lambda_universal_router.events import CustomEvent

router = Router()

@router.custom()
def handle_unknown(event: CustomEvent, context):
    # Log unknown event type
    print(f"Received unknown event: {event.event_data}")
    
    # Try to handle based on event structure
    if 'Records' in event.event_data:
        return handle_record_based_event(event.event_data)
    elif 'detail-type' in event.event_data:
        return handle_eventbridge_like_event(event.event_data)
    else:
        return {
            "statusCode": 200,
            "body": "Event processed by fallback handler"
        }
```

## Complete Example

```python
from lambda_universal_router import Router
from lambda_universal_router.events import (
    APIGatewayEvent, SQSEvent, S3Event,
    DynamoDBStreamEvent, CustomEvent
)

router = Router()

# API Gateway handler
@router.apigateway("/process", method="POST")
def process_api(event: APIGatewayEvent, context):
    return {"statusCode": 200, "body": "Processed"}

# SQS handler
@router.sqs()
def process_queue(event: SQSEvent, context):
    for msg in event.records:
        process_message(msg)

# S3 handler
@router.s3()
def process_files(event: S3Event, context):
    for record in event.records:
        process_file(record)

# DynamoDB handler
@router.dynamodb()
def sync_data(event: DynamoDBStreamEvent, context):
    for record in event.records:
        sync_record(record)

# Fallback handler
@router.custom()
def handle_unknown(event: CustomEvent, context):
    return {"status": "processed by fallback"}

# Main handler
def lambda_handler(event, context):
    return router.dispatch(event, context)
```
