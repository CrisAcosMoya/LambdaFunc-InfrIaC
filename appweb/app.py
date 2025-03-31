from flask import Flask, render_template, request
import os
import boto3
from boto3.dynamodb.types import TypeDeserializer

app = Flask(__name__)

dynamodb_endpoint = os.getenv('DYNAMODB_ENDPOINT', 'http://host.docker.internal:4566')
region = "us-east-1"
table_name = os.getenv('DYNAMODB_TABLE', 'SpaceXLaunches')

client = boto3.client('dynamodb', endpoint_url=dynamodb_endpoint, region_name=region)

deserializer = TypeDeserializer()

def deserialize_item(item):
    """
    Convierte un item del formato DynamoDB (con tipos) a un diccionario Python.
    """
    return {k: deserializer.deserialize(v) for k, v in item.items()}

@app.route('/')
def index():
    status_filter = request.args.get('status')
    if status_filter:
        response = client.scan(
            TableName=table_name,
            FilterExpression="#s = :status_val",
            ExpressionAttributeNames={
                "#s": "status"
            },
            ExpressionAttributeValues={
                ":status_val": {"S": status_filter}
            }
        )
    else:
        response = client.scan(TableName=table_name)
    
    items = response.get('Items', [])
    deserialized_items = [deserialize_item(item) for item in items]
    return render_template('index.html', launches=deserialized_items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)