import boto3


def send_batch_job(job_definition, job_name, job_queue, container_overides):
    # Function uses boto3 to programmatically launch Batch job with input

    client = boto3.client('batch')
    try:
        # If there are no inputs in Batch job
        if container_overides == {}:
            response = client.submit_job(
                jobDefinition=job_definition,
                jobName=job_name,
                jobQueue=job_queue)

        else:
            # If there are inputs in Batch job
            response = client.submit_job(
                jobDefinition=job_definition,
                jobName=job_name,
                jobQueue=job_queue,
                containerOverrides=container_overides)

        # Successfully submitted
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
    Lambda handler receives input from MongoDB event and preprocess data to
    send it to launch Batch job
    """

    # Extract data from MongoDB event and get collection
    data = event['detail']['fullDocument']

    # Get key value from Mongo Collection
    PD_DATA = data['Query']

    overrides = {'environment': [
        {
            'name': 'Query',
            'value': PD_DATA,
        }
    ]
    }
    send_job = send_batch_job(job_definition='', job_name='', job_queue='', container_overides=overrides)
    print(send_job)
