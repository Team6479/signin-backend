import boto3
import os

aws = boto3.Session(
    aws_access_key_id=os.environ['AWS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_KEY_SECRET'],
    region_name='us-east-1'
)
dynamodb = aws.resource('dynamodb')

entries = dynamodb.Table('6479-signin-times')
users = dynamodb.Table('6479-signin-users')

def get_user_data(id: int):
    try:
        return users.get_item(Key={
            'id': id
        })['Item']
    except:
        return None

def create_user(id: int, name: str):
    users.put_item(Item={
        'id': id,
        'name': name
    })

def push_entry(id: int, start: int, end: int):
    entries.put_item(Item={
        'id': id,
        'date': time.strftime('%Y-%m-%d', time.localtime(start)),
        'start': start,
        'end': end,
        'duration': (end - start)
    })
    log('[' + time.strftime('%Y-%m-%d', time.localtime(start)) + '] ' + str(id) + ' from ' + str(start) + '-' + str(end) + ' (' + str(end - start) + 's)')