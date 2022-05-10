import json
import boto3
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

ec2_client = boto3.client('ec2')
ses_client = boto3.client('ses')
ec2_resource = boto3.resource('ec2')

# create date variables
wait_time = datetime.now() + relativedelta(hours=6)
wait_time.strftime('%d/%m/%Y')
today = datetime.now()


# Email Notification
def send_email(recipient, body, subject):
    CHARSET = "UTF-8"

    ses_response = ses_client.send_email(
        Destination={
            "ToAddresses": [recipient],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": [body],
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": [subject]
            },
        },
        Source="arn:aws:ses:us-west-1:851998132317:identity/singhshivani3416@gmail.com",
    )
    return ses_response


def lambda_handler(event, context):
    # Get all running ec2 instances 
    missing_tags = []
    reservations = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]).get('Reservations', [])

    for reservation in reservations:
        for instance in reservation["Instances"]:
            tags = {}
            count = 0
            instance_id = instance['InstanceId']
            for tag in instance['Tags']:
                tags[tag['Key']] = tag['Value']

            if 'Name' not in tags:
                missing_tags.append('Name')
                count += 1
            if 'Environment' not in tags:
                missing_tags.append('Environment')
                count += 1

            if count != 0:
                # Check if "TerminateOn" tag exists
                if 'TerminateOn' in tags:
                    # compare TerminateOn value with current date
                    if tags["TerminateOn"] == today:

                        # Check if termination protection is enabled
                        terminate_protection = ec2_client.describe_instance_attribute(
                            InstanceId=instance_id,
                            Attribute='disableApiTermination')
                        protection_value = (terminate_protection['DisableApiTermination']['Value'])

                        # if enabled then disable it
                        if protection_value:
                            ec2_client.modify_instance_attribute(InstanceId=instance_id,
                                                                 Attribute="disableApiTermination", Value="False")
                            # terminate instance
                            ec2_client.terminate_instances(InstanceIds=instance_id)
                            print("terminated" + str(instance_id))

                            # send email that instance is terminated
                            subject = 'Terminated Instance:' + str(instance_id)
                            body = 'The ' + str(instance_id) + ' instance is terminated due to improper tagging. '
                            response = send_email(tags['created by'], body, subject)
                            if response:
                                print('Sent Email !')
                            else:
                                print('Fail to sent !')

                        else:
                            now = datetime.now()
                            future = tags["TerminateOn"]
                            terminate_on = datetime.strptime(future, "%d/%m/%Y")
                            time_left = (terminate_on - now)
                            print(str(instance_id) + " will be removed in " + str(time_left) + " hours")

                elif 'TerminateOn' not in tags:
                    # , create the tag
                    ec2_resource.create_tags(Resources=[instance_id],
                                             Tags=[
                                                 {'Key': 'TerminateOn',
                                                  'Value': wait_time.strftime('%d/%m/%Y')}
                                             ])

                    # Send an email that this instance is missing tags and will be removed after 6 hours
                    subject = 'Reminder Mail ! Missing tags for ' + str(instance_id)
                    body = 'The ' + str(instance_id) + 'is missing ' + str(missing_tags) + 'tag(s). Please tag the ' \
                                                                                           'instance correctly, ' \
                                                                                           'otherwise it will get ' \
                                                                                           'terminated in 6 hours. '
                    response = send_email(tags['Created by'], body, subject)
                    if response:
                        print('Sent Email !')
                    else:
                        print('Fail to sent !')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
