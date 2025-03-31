import json
import os
import requests
import boto3
from botocore.exceptions import ClientError

endpoint_url = os.getenv('DYNAMODB_ENDPOINT', 'http://host.docker.internal:4566')
region = "us-east-1"

try:
    client = boto3.client('dynamodb', endpoint_url=endpoint_url, region_name=region)
    tables = client.list_tables()
except Exception as ex:
    client = None

def fetch_launches():
    url = "https://api.spacexdata.com/v4/launches"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching SpaceX API: {str(e)}")

def process_launch(launch):
    processed = {
        'launch_id': str(launch.get('id') or 'N/A'),
        'mission_name': launch.get('name') or 'N/A',
        'launch_date': launch.get('date_utc') or 'N/A',
        'rocket': launch.get('rocket') or 'N/A',
        'status': 'upcoming' if launch.get('upcoming') else ('success' if launch.get('success') else 'failed')
    }
    return processed

def upsert_launch(launch_item):
    if client is None:
        return False

    try:
        formatted_item = {
            'launch_id': {'S': launch_item.get('launch_id') or 'N/A'},
            'mission_name': {'S': launch_item.get('mission_name') or 'N/A'},
            'launch_date': {'S': launch_item.get('launch_date') or 'N/A'},
            'rocket': {'S': launch_item.get('rocket') or 'N/A'},
            'status': {'S': launch_item.get('status') or 'N/A'}
        }
        table_name = os.getenv('DYNAMODB_TABLE', 'SpaceXLaunches')
        client.put_item(TableName=table_name, Item=formatted_item)
        return True
    except ClientError as e:
        return False

def lambda_handler(event, context):
    manual_invocation = event.get('manual', False)
    processed_records = []
    updated_count = 0

    try:
        launches = fetch_launches()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    for launch in launches:
        processed = process_launch(launch)
        if upsert_launch(processed):
            updated_count += 1
            processed_records.append(processed)

    result = {
        'total_processed': len(launches),
        'updated_records': updated_count,
        'processed_details': processed_records if manual_invocation else None
    }
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
