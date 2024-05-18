import glob

import boto3
import cfnresponse

def lambda_handler(event, context):
    # Init ...
    the_event = event['RequestType']
    print("The event is: ", str(the_event))
    response_data = {}
    s3client = boto3.client('s3')
    # Retrieve parameters
    the_bucket = event['ResourceProperties']['the_bucket']

    try:
        if the_event in ('Create', 'Update'):
            for object_path in glob.glob('objects/**', recursive=True):
                print("Creating: ", object_path)
                s3client.upload_file(object_path, the_bucket, object_path)
        elif the_event == 'Delete':
            print("Deleting S3 content...")
            b_operator = boto3.resource('s3')
            b_operator.Bucket(str(the_bucket)).objects.all().delete()
        # Everything OK... send the signal back
        print("Operation successful!")
        cfnresponse.send(event,
                        context,
                        cfnresponse.SUCCESS,
                        response_data)
    except Exception as e:
        print("Operation failed...")
        print(str(e))
        response_data['Data'] = str(e)
        cfnresponse.send(event,
                        context,
                        cfnresponse.FAILED,
                        response_data)