import boto3


client = boto3.client('codedeploy')

def lambda_handler(event, context):
    print('Testing beforeAllowTraffic.py')
    print('EVENT', event)
    print('CONTEXT', context)
    deployment_id = event.get('DeploymentId')
    lifecycle_event_hook_execution_id = event.get('LifecycleEventHookExecutionId')
    response = client.put_lifecycle_event_hook_execution_status(
        deploymentId=deployment_id,
        lifecycleEventHookExecutionId=lifecycle_event_hook_execution_id,
        status='Succeeded'
    )
