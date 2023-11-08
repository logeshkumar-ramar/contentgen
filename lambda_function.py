import json
import base64
import requests
from ast import literal_eval
from main import get_content_email, get_content_whatsapp, get_prompt_image, get_image, generate_content, get_best_holidays, get_plan, get_card, get_banner, get_cardv2, get_bannerv2, get_best_holidays2, get_plan_v2, get_url, get_product_specific
import os
def lambda_handler(event, context):

    path = event['path'].rstrip("/").split("/")[1:]
    if path[0]!='get_url':
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
    if path[0]=="get_plan_v2":
        content = get_plan_v2(context)
    if path[0]=="get_image":
        content = get_image(context)
    if path[0]=="get_card":
        content = get_card(context)
    if path[0]=="get_banner":
        content = get_banner(context)
    if path[0]=="testing":
        content = get_best_holidays2(context)
    if path[0]=="get_style":
        content = get_product_specific(context)
    if path[0]=="get_url":
        context = literal_eval(event['body'])
        content = get_url(context['image'])
        return {
            'statusCode': 200,
            'body': content
        }
    if path[0]=="get_card_v2":
        content = get_cardv2(context)
    if path[0]=="get_banner_v2":
        content = get_bannerv2(context)
    print('final_content: ', content)   
    return {
        'statusCode': 200,
        'body': json.dumps(f'{content}')
    }
