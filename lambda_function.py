import json
import base64
import requests
from ast import literal_eval
from main import get_content_email, get_content_whatsapp, get_prompt_image, get_image, generate_content, get_best_holidays, get_plan, get_card, get_banner, get_best_holidays2
import os
def lambda_handler(event, context):

    path = event['path'].rstrip("/").split("/")[1:]
    context = literal_eval(event['body'])
    print('path: ', path, event['path'])
    # path = ['get_content', 'email']
    # context = {'industry': 'skin care and grooming', 'festival': 'diwali'}
    content = ""
    if path[0]=='get_content':
        context['channel'] = path[1]
        if path[1] in ['sms', 'email', 'whatsapp']:
            content = generate_content(context)
    if path[0]=='best_holiday':
        content = get_best_holidays(context)
    if path[0]=="get_plan":
        content = get_plan(context)
    if path[0]=="get_image":
        content = get_image(context)
    if path[0]=="get_card":
        content = get_card(context)
    if path[0]=="get_banner":
        content = get_banner(context)
    if path[0]=="testing":
        content = get_best_holidays2(context)
    print('final_content: ', content)   
    return {
        'statusCode': 200,
        'body': json.dumps(f'{content}')
    }