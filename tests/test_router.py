import unittest
from lambda_universal_router import Router
from lambda_universal_router.events import APIGatewayEvent, SQSEvent, S3Event

class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = Router()

    def test_api_gateway_routing(self):
        @self.router.apigateway("/test", method="GET")
        def handler(event, context):
            return {"statusCode": 200, "body": "test"}

        event = {
            "httpMethod": "GET",
            "path": "/test",
            "requestContext": {},
            "headers": {},
            "queryStringParameters": {},
            "pathParameters": {}
        }

        result = self.router.dispatch(event, {})
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["body"], "test")

    def test_sqs_routing(self):
        @self.router.sqs()
        def handler(event, context):
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

if __name__ == '__main__':
    unittest.main()
