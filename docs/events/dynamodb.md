# DynamoDB Stream Events

DynamoDB Streams enable you to capture changes to your DynamoDB tables and process them with Lambda functions.

## Event Structure

```python
class DynamoDBStreamEvent:
    records: List[DynamoDBStreamRecord]  # List of DynamoDB stream records

class DynamoDBStreamRecord:
    event_id: str         # Unique event ID
    event_name: str       # INSERT, MODIFY, or REMOVE
    event_version: str    # Event version
    event_source: str     # aws:dynamodb
    aws_region: str       # AWS region
    dynamodb: Dict[str, Any]  # Contains Keys, NewImage, OldImage
```

## Usage Examples

### Basic Change Processing

```python
from lambda_universal_router import Router
from lambda_universal_router.events import DynamoDBStreamEvent

router = Router()

@router.dynamodb()
def process_changes(event: DynamoDBStreamEvent, context):
    for record in event.records:
        print(f"Event ID: {record.event_id}")
        print(f"Event Type: {record.event_name}")
        
        if record.event_name == "INSERT":
            handle_insert(record.dynamodb['NewImage'])
        elif record.event_name == "MODIFY":
            handle_update(
                record.dynamodb['OldImage'],
                record.dynamodb['NewImage']
            )
        elif record.event_name == "REMOVE":
            handle_delete(record.dynamodb['OldImage'])
```

### Change Data Capture (CDC)

```python
@router.dynamodb()
def sync_to_elasticsearch(event: DynamoDBStreamEvent, context):
    for record in event.records:
        if record.event_name in ["INSERT", "MODIFY"]:
            # Get the new version of the document
            document = record.dynamodb['NewImage']
            # Index in Elasticsearch
            index_document(document)
        elif record.event_name == "REMOVE":
            # Delete from Elasticsearch
            delete_document(record.dynamodb['Keys'])
```

### Filtering and Validation

```python
@router.dynamodb()
def filtered_processing(event: DynamoDBStreamEvent, context):
    for record in event.records:
        # Only process high-priority items
        if record.event_name != "REMOVE":
            new_image = record.dynamodb['NewImage']
            if new_image.get('priority', {}).get('S') == 'HIGH':
                process_priority_item(new_image)
```

### Cross-Region Replication

```python
@router.dynamodb()
def replicate_changes(event: DynamoDBStreamEvent, context):
    for record in event.records:
        # Replicate to another region
        if record.event_name in ["INSERT", "MODIFY"]:
            replicate_item(
                record.dynamodb['NewImage'],
                target_region="us-west-2"
            )
        elif record.event_name == "REMOVE":
            delete_item(
                record.dynamodb['Keys'],
                target_region="us-west-2"
            )
```

## Event Examples

1. **Insert Event**
   ```python
   {
       "Records": [
           {
               "eventID": "1",
               "eventName": "INSERT",
               "eventVersion": "1.0",
               "eventSource": "aws:dynamodb",
               "awsRegion": "us-east-1",
               "dynamodb": {
                   "Keys": {
                       "Id": {"S": "101"}
                   },
                   "NewImage": {
                       "Id": {"S": "101"},
                       "Title": {"S": "Book 101"},
                       "ISBN": {"S": "978-1234567890"},
                       "Price": {"N": "29.99"}
                   },
                   "SequenceNumber": "111",
                   "SizeBytes": 26,
                   "StreamViewType": "NEW_AND_OLD_IMAGES"
               }
           }
       ]
   }
   ```

2. **Modify Event**
   ```python
   {
       "Records": [
           {
               "eventName": "MODIFY",
               "dynamodb": {
                   "OldImage": {
                       "Id": {"S": "101"},
                       "Price": {"N": "29.99"}
                   },
                   "NewImage": {
                       "Id": {"S": "101"},
                       "Price": {"N": "25.99"}
                   }
               }
           }
       ]
   }
   ```

## Best Practices

1. **Error Handling**
   ```python
   @router.dynamodb()
   def safe_process(event: DynamoDBStreamEvent, context):
       for record in event.records:
           try:
               process_record(record)
           except ValidationError:
               # Data validation failed
               log_validation_error(record)
           except ConnectionError:
               # Failed to connect to downstream service
               # Re-throw to retry
               raise
           except Exception as e:
               # Unexpected error
               log_error(record, e)
               raise
   ```

2. **Batch Processing**
   ```python
   @router.dynamodb()
   def batch_process(event: DynamoDBStreamEvent, context):
       inserts = []
       updates = []
       deletes = []
       
       for record in event.records:
           if record.event_name == "INSERT":
               inserts.append(record.dynamodb['NewImage'])
           elif record.event_name == "MODIFY":
               updates.append(record.dynamodb['NewImage'])
           elif record.event_name == "REMOVE":
               deletes.append(record.dynamodb['Keys'])
       
       if inserts:
           batch_insert(inserts)
       if updates:
           batch_update(updates)
       if deletes:
           batch_delete(deletes)
   ```

3. **Monitoring**
   ```python
   @router.dynamodb()
   def monitored_process(event: DynamoDBStreamEvent, context):
       metrics = {
           "inserts": 0,
           "updates": 0,
           "deletes": 0,
           "errors": 0
       }
       
       for record in event.records:
           try:
               if record.event_name == "INSERT":
                   metrics["inserts"] += 1
               elif record.event_name == "MODIFY":
                   metrics["updates"] += 1
               elif record.event_name == "REMOVE":
                   metrics["deletes"] += 1
               
               process_record(record)
           except Exception:
               metrics["errors"] += 1
       
       log_metrics(metrics)
   ```

## Configuration Tips

1. **Stream Settings**
   - Choose appropriate StreamViewType
   - Configure batch size
   - Set proper retention period

2. **Lambda Settings**
   - Set memory based on record size
   - Configure timeout for batch processing
   - Enable X-Ray tracing

3. **Performance**
   - Use batch processing when possible
   - Implement concurrent processing
   - Monitor throughput and latency

## See Also

- [Using AWS Lambda with DynamoDB](https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html)
- [DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)
- [Best Practices for DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.BestPractices.html)
