import json
import boto3
from botocore.exceptions import ClientError

def send_batch_job(job_definition, job_name, job_queue, container_overides):
    # Function uses boto3 to programatically launch Batch job with input
    
    client = boto3.client('batch')
    try:
       
        # If there are inputs in Batch job
        response = client.submit_job(
            jobDefinition=job_definition,
            jobName=job_name,
            jobQueue=job_queue,
            containerOverrides=container_overides)
        
        # Succesfully submitted
        return {
            "status": 0,
            "data": {
                "response": response
            }
        }

    # Error with Submission
    except Exception as error:
        return {
            "status": -1,
            "data": container_overides,
            "error": {
                "message": str(error)
            }
        }



def lambda_handler(event, context):
    """
    Lambda handler receives input from MongoDB event and retrieve secrets from AWS 
    Secret Manager to launch Batch job
    """
    
    secret_name = "MongoDB_Creds"
    region_name = "us-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    username = secret['DB_USER']
    password = secret['DB_PASSWORD']
    
    print(secret)
    overides = {'environment': [
            {
               'name': 'DB_USER',
               'value': username,
            },
            
            {
               'name': 'DB_PASSWORD',
               'value': password,
            }
        ]
    }
    sendJob = send_batch_job(job_definition, job_name, job_queue, overides)
    print(sendJob)
    
