from __future__ import annotations
import unittest
from lambda_universal_router import Router
from lambda_universal_router.events import APIGatewayEvent, SQSEvent, S3Event

class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = Router()

    def test_api_gateway_routing(self):
        @self.router.apigateway("/test", method="GET")
        def handler(event: APIGatewayEvent, context):
            return {"statusCode": 200, "body": "test"}

        event = {
            "httpMethod": "GET",
            "path": "/test",
            "requestContext": {
                "httpMethod": "GET",
                "path": "/test",
                "stage": "prod",
                "requestId": "test-id"
            },
            "headers": {},
            "queryStringParameters": {},
            "pathParameters": {}
        }

        result = self.router.dispatch(event, {})
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["body"], "test")

    def test_sqs_routing(self):
        @self.router.sqs()
        def handler(event: SQSEvent, context):
            return "processed"

        event = {
            "Records": [{
                "messageId": "test",
                "body": "test message",
                "messageAttributes": {},
                "eventSource": "aws:sqs"
            }]
        }

        result = self.router.dispatch(event, {})
        self.assertEqual(result, "processed")

    def test_s3_routing(self):
        @self.router.s3()
        def handler(event: S3Event, context):
            return "processed"

        event = {
            "Records": [{
                "eventName": "ObjectCreated:Put",
                "eventTime": "2024-03-17T12:00:00.000Z",
                "s3": {
                    "bucket": {
                        "name": "test-bucket",
                        "arn": "arn:aws:s3:::test-bucket"
                    },
                    "object": {
                        "key": "test.txt",
                        "size": 123,
                        "eTag": "abc123"
                    }
                },
                "eventSource": "aws:s3"
            }]
        }

        result = self.router.dispatch(event, {})
        self.assertEqual(result, "processed")

if __name__ == '__main__':
    unittest.main()