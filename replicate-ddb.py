import json
import boto3

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('test-ddb-oregon')
    
    print(event)
    
    for record in event['Records']:
        
        print(record['eventName'])
        
        if(record['eventName']) == "MODIFY":
            print('modifying now')
            
            newFname = record['dynamodb']['NewImage']['fname']['S']
            newId = record['dynamodb']['NewImage']['id']['S']
            
            table.update_item(
                Key={
                    'id': newId
            },
            UpdateExpression='SET fname = :val1',
            ExpressionAttributeValues={
                ':val1': newFname
            })
            
        elif(record['eventName']) == "INSERT":
            print('inserting now')
            #newImage = record['dynamodb']['NewImage']
            #print(newImage)
            newFname = record['dynamodb']['NewImage']['fname']['S']
            newId = record['dynamodb']['NewImage']['id']['S']
            table.put_item(
                Item={
                    'id': newId,
                    'fname': newFname
            })
        elif(record['eventName']) == "REMOVE":
            print('removing now')
            
            newId = record['dynamodb']['Keys']['id']['S']
            table.delete_item(
                Key={
                    'id': newId
            })
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
