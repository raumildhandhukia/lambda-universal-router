# Amazon MSK (Kafka) Events

Amazon MSK (Managed Streaming for Apache Kafka) integration allows Lambda functions to process records from Kafka topics.

## Event Structure

```python
class KafkaEvent:
    event_source: str       # 'aws:kafka' or 'aws:self-managed-kafka'
    event_source_arn: str   # ARN of the MSK cluster
    bootstrap_servers: str  # Kafka bootstrap servers
    records: List[KafkaRecord]  # List of Kafka records

class KafkaRecord:
    topic: str             # Kafka topic name
    partition: int         # Topic partition number
    offset: int           # Record offset in partition
    timestamp: int        # Record timestamp
    timestamp_type: str   # Timestamp type
    key: bytes           # Record key (Base64 decoded)
    value: bytes         # Record value (Base64 decoded)
    headers: List[Dict[str, str]]  # Kafka record headers
```

## Usage Examples

### Basic Record Processing

```python
from lambda_universal_router import Router
from lambda_universal_router.events import KafkaEvent

router = Router()

@router.kafka()
def process_records(event: KafkaEvent, context):
    print(f"Processing records from {event.event_source}")
    print(f"Bootstrap servers: {event.bootstrap_servers}")
    
    for record in event.records:
        print(f"Topic: {record.topic}")
        print(f"Partition: {record.partition}")
        print(f"Offset: {record.offset}")
        print(f"Value: {record.value.decode('utf-8')}")
```

### Topic-Specific Processing

```python
@router.kafka()
def handle_topics(event: KafkaEvent, context):
    for record in event.records:
        if record.topic == "orders":
            process_order(record.value)
        elif record.topic == "users":
            process_user(record.value)
```

### Batch Processing with Error Handling

```python
@router.kafka()
def safe_process(event: KafkaEvent, context):
    results = {
        "successful": [],
        "failed": []
    }
    
    for record in event.records:
        try:
            process_record(record)
            results["successful"].append({
                "topic": record.topic,
                "partition": record.partition,
                "offset": record.offset
            })
        except Exception as e:
            results["failed"].append({
                "topic": record.topic,
                "partition": record.partition,
                "offset": record.offset,
                "error": str(e)
            })
    
    return results
```

### Working with Headers

```python
@router.kafka()
def process_with_headers(event: KafkaEvent, context):
    for record in event.records:
        # Extract headers
        headers = {
            header['key']: header['value']
            for header in record.headers
        }
        
        # Process based on headers
        if headers.get('message-type') == 'priority':
            process_priority_message(record)
        else:
            process_normal_message(record)
```

## Event Examples

1. **Basic Event**
   ```python
   {
       "eventSource": "aws:kafka",
       "eventSourceArn": "arn:aws:kafka:us-east-1:123456789012:cluster/msk-cluster/1a2b3c4d",
       "bootstrapServers": "b-1.msk-cluster.123456.kafka.us-east-1.amazonaws.com:9092",
       "records": {
           "mytopic-0": [
               {
                   "topic": "mytopic",
                   "partition": 0,
                   "offset": 15,
                   "timestamp": 1545084650987,
                   "timestampType": "CREATE_TIME",
                   "key": "SGVsbG8=",  # Base64 encoded
                   "value": "V29ybGQ=",  # Base64 encoded
                   "headers": [
                       {
                           "key": "message-type",
                           "value": "standard"
                       }
                   ]
               }
           ]
       }
   }
   ```

## Best Practices

1. **Error Handling**
   ```python
   @router.kafka()
   def handle_records(event: KafkaEvent, context):
       for record in event.records:
           try:
               value = record.value.decode('utf-8')
               process_message(value)
           except UnicodeDecodeError:
               handle_binary_data(record.value)
           except Exception as e:
               log_error(record, e)
   ```

2. **Performance**
   ```python
   @router.kafka()
   def batch_process(event: KafkaEvent, context):
       # Group records by topic
       records_by_topic = {}
       for record in event.records:
           records_by_topic.setdefault(record.topic, []).append(record)
       
       # Process each topic's records in batch
       for topic, records in records_by_topic.items():
           batch_process_topic(topic, records)
   ```

3. **Monitoring**
   ```python
   @router.kafka()
   def monitored_process(event: KafkaEvent, context):
       metrics = {
           "processed": 0,
           "errors": 0,
           "bytes_processed": 0
       }
       
       for record in event.records:
           try:
               process_record(record)
               metrics["processed"] += 1
               metrics["bytes_processed"] += len(record.value)
           except Exception:
               metrics["errors"] += 1
       
       log_metrics(metrics)
   ```

## See Also

- [Using Lambda with Amazon MSK](https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html)
- [Amazon MSK Documentation](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
