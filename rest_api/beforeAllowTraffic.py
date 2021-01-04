import boto3


client = boto3.client('codedeploy')

def lambda_handler(event, context):
    '''
    Make sure code changes work after traffic starts getting routed to new lambda function
    '''
    print('Testing beforeAllowTraffic.py')

    deployment_id = event.get('DeploymentId')
    lifecycle_event_hook_execution_id = event.get('LifecycleEventHookExecutionId')
    response = client.put_lifecycle_event_hook_execution_status(
        deploymentId=deployment_id,
        lifecycleEventHookExecutionId=lifecycle_event_hook_execution_id,
        status='Succeeded'
    )
