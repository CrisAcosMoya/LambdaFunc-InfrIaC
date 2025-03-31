import json
import os
import requests
import boto3
from botocore.exceptions import ClientError

# Configurar el endpoint y la región
endpoint_url = os.getenv('DYNAMODB_ENDPOINT', 'http://host.docker.internal:4566')
region = "us-east-1"

print("DEBUG: Usando endpoint:", endpoint_url)

# Definir el cliente de DynamoDB a nivel global.
try:
    client = boto3.client('dynamodb', endpoint_url=endpoint_url, region_name=region)
    # Para depuración: listar tablas
    tables = client.list_tables()
    print("DEBUG: Tablas disponibles:", tables)
except Exception as ex:
    print("DEBUG: Error al crear el cliente de DynamoDB:", ex)
    client = None  # O manejar el error de forma apropiada

# Para propósitos de 'upsert', si el cliente es necesario, se usará en la función upsert_launch.

def fetch_launches():
    """
    Consulta la API pública de SpaceX y retorna la lista de lanzamientos.
    """
    url = "https://api.spacexdata.com/v4/launches"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching SpaceX API: {str(e)}")

def process_launch(launch):
    """
    Extrae y transforma los datos relevantes de un lanzamiento.
    """
    processed = {
        'launch_id': str(launch.get('id') or 'N/A'),
        'mission_name': launch.get('name') or 'N/A',
        'launch_date': launch.get('date_utc') or 'N/A',
        'rocket': launch.get('rocket') or 'N/A',
        'status': 'upcoming' if launch.get('upcoming') else ('success' if launch.get('success') else 'failed')
    }
    return processed

def upsert_launch(launch_item):
    """
    Inserta o actualiza (upsert) el registro en DynamoDB utilizando el cliente.
    Cada atributo se formatea como un string (S) para DynamoDB.
    """
    if client is None:
        print("DEBUG: Cliente de DynamoDB no disponible")
        return False

    try:
        # Aseguramos que ningún valor requerido sea None (usamos 'N/A' como fallback)
        formatted_item = {
            'launch_id': {'S': launch_item.get('launch_id') or 'N/A'},
            'mission_name': {'S': launch_item.get('mission_name') or 'N/A'},
            'launch_date': {'S': launch_item.get('launch_date') or 'N/A'},
            'rocket': {'S': launch_item.get('rocket') or 'N/A'},
            'status': {'S': launch_item.get('status') or 'N/A'}
        }
        table_name = os.getenv('DYNAMODB_TABLE', 'SpaceXLaunches')
        print("DEBUG: Intentando insertar item:", formatted_item)
        client.put_item(TableName=table_name, Item=formatted_item)
        print("DEBUG: Inserción exitosa para:", launch_item.get('launch_id'))
        return True
    except ClientError as e:
        print(f"DEBUG: Error upserting item {launch_item.get('launch_id')}: {e.response['Error']['Message']}")
        return False

def lambda_handler(event, context):
    """
    Función principal de Lambda.
    - Si se invoca manualmente con {"manual": true} en el payload, retorna un resumen detallado.
    - En invocaciones programadas, actualiza la tabla con los lanzamientos de SpaceX.
    """
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
