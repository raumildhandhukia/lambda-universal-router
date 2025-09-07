# Kinesis Stream Events

Amazon Kinesis Data Streams allows you to process streaming data using Lambda functions.

## Event Structure

```python
class KinesisStreamEvent:
    records: List[KinesisRecord]  # List of Kinesis records

class KinesisRecord:
    kinesis_schema_version: str    # Schema version
    partition_key: str            # Partition key
    sequence_number: str          # Sequence number
    data: bytes                   # Base64-decoded data
    approximate_arrival_timestamp: float  # Record timestamp
```

## Usage Examples

### Basic Record Processing

```python
from lambda_universal_router import Router
from lambda_universal_router.events import KinesisStreamEvent

router = Router()

@router.kinesis()
def process_stream(event: KinesisStreamEvent, context):
    for record in event.records:
        # Data comes as bytes, decode if it's text
        data = record.data.decode('utf-8')
        print(f"Processing record: {data}")
        print(f"Partition key: {record.partition_key}")
        print(f"Sequence number: {record.sequence_number}")
```

### JSON Data Processing

```python
import json

@router.kinesis()
def process_json(event: KinesisStreamEvent, context):
    for record in event.records:
        try:
            # Decode bytes to string, then parse JSON
            data = json.loads(record.data.decode('utf-8'))
            process_data(data)
        except json.JSONDecodeError:
            print(f"Invalid JSON in record: {record.sequence_number}")
```

### Batch Processing

```python
@router.kinesis()
def batch_process(event: KinesisStreamEvent, context):
    # Group records by partition key
    records_by_partition = {}
    for record in event.records:
        key = record.partition_key
        records_by_partition.setdefault(key, []).append(record)
    
    # Process each partition's records together
    for partition_key, records in records_by_partition.items():
        process_partition(partition_key, records)
```

### Time-Based Processing

```python
@router.kinesis()
def time_based_process(event: KinesisStreamEvent, context):
    for record in event.records:
        # Check record timestamp
        if record.approximate_arrival_timestamp > get_last_processed_time():
            process_new_record(record)
        else:
            handle_late_record(record)
```

## Event Examples

1. **Basic Kinesis Event**
   ```python
   {
       "Records": [
           {
               "kinesis": {
                   "kinesisSchemaVersion": "1.0",
                   "partitionKey": "1",
                   "sequenceNumber": "49590338271490256608559692538361571095921575989136588898",
                   "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0Lg==",
                   "approximateArrivalTimestamp": 1545084650.987
               },
               "eventSource": "aws:kinesis",
               "eventVersion": "1.0",
               "eventID": "shardId-000000000006:49590338271490256608559692538361571095921575989136588898",
               "eventName": "aws:kinesis:record",
               "invokeIdentityArn": "arn:aws:iam::123456789012:role/lambda-role",
               "awsRegion": "us-east-1",
               "eventSourceARN": "arn:aws:kinesis:us-east-1:123456789012:stream/lambda-stream"
           }
       ]
   }
   ```

2. **JSON Data Record**
   ```python
   {
       "Records": [
           {
               "kinesis": {
                   "data": "eyJ0eXBlIjoibG9nIiwibWVzc2FnZSI6IlRlc3QgbG9nIn0=",  # {"type":"log","message":"Test log"}
                   "partitionKey": "logs",
                   "sequenceNumber": "123456789"
               }
           }
       ]
   }
   ```

## Best Practices

1. **Error Handling**
   ```python
   @router.kinesis()
   def safe_process(event: KinesisStreamEvent, context):
       for record in event.records:
           try:
               process_record(record)
           except ValueError:
               # Data validation error
               log_validation_error(record)
           except ProcessingError:
               # Processing error, might want to retry
               queue_for_retry(record)
           except Exception as e:
               # Unexpected error
               log_error(record, e)
               raise
   ```

2. **Performance Optimization**
   ```python
   @router.kinesis()
   def optimized_process(event: KinesisStreamEvent, context):
       # Process records in batches for better performance
       batch_size = 100
       records = event.records
       
       for i in range(0, len(records), batch_size):
           batch = records[i:i + batch_size]
           process_batch(batch)
   ```

3. **Monitoring**
   ```python
   @router.kinesis()
   def monitored_process(event: KinesisStreamEvent, context):
       metrics = {
           "processed": 0,
           "errors": 0,
           "bytes_processed": 0,
           "processing_time": 0
       }
       
       start_time = time.time()
       
       for record in event.records:
           try:
               process_record(record)
               metrics["processed"] += 1
               metrics["bytes_processed"] += len(record.data)
           except Exception:
               metrics["errors"] += 1
       
       metrics["processing_time"] = time.time() - start_time
       log_metrics(metrics)
   ```

## Configuration Tips

1. **Stream Settings**
   - Configure appropriate shard count
   - Set retention period
   - Enable enhanced fan-out if needed

2. **Lambda Settings**
   - Set memory based on record size
   - Configure batch size
   - Set appropriate timeout

3. **Performance**
   - Use batch processing
   - Implement concurrent processing
   - Monitor throughput and latency

## See Also

- [Using AWS Lambda with Amazon Kinesis](https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html)
- [Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/introduction.html)
- [Lambda Function Configuration](https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html#services-kinesis-configure)
