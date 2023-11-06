import copy
import requests
from PIL import Image
import io
import base64
import boto3
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse
from prompts import PROMPT_EMAIL, PROMPT_WHATSAPP, PROMPT_IMAGE, IMAGE_NEG_PROMPT, PROMPT_HOLIDAY, PROMPT_PLANNER, PROMPT_SMS, PROMPT_CARDS, PROMPT_BANNER, PROMPT_PLANNER_V2
from llm.llm_api import  get_llm, call_llm
import time
from ast import literal_eval
import re
import json
from datetime import date



def generate_content(info):
    
    if info.get('channel') == 'email':
        prompt = copy.deepcopy(PROMPT_EMAIL[:])
        prompt[1]['content'] = prompt[1]['content'].format(info=info)
    elif info.get('channel') == 'whatsapp':
        prompt = copy.deepcopy(PROMPT_WHATSAPP[:])
        prompt[1]['content'] = prompt[1]['content'].format(info=info)
    elif info.get('channel') == 'sms':
        prompt = copy.deepcopy(PROMPT_SMS[:])
        prompt[1]['content'] = prompt[1]['content'].format(info=info)
    else:
        prompt = copy.deepcopy(PROMPT_IMAGE[:])
        prompt[1]['content'] = prompt[1]['content'].format(info=info)
    llm = get_llm(llm_provider="platform_http", version=3)
    output = call_llm(llm, prompt, sleep_time=1)

    return output
    

def get_best_holidays2(info):

    prompt = copy.deepcopy(PROMPT_HOLIDAY[:])
    prompt[1]['content'] = prompt[1]['content'].format(info=info)
    
    llm = get_llm(llm_provider="platform_http", version=3)
    output = call_llm(llm, prompt, sleep_time=1)
    output = json.dumps(output)
    return output
    
    
def get_best_holidays(info):
    print(info['holidays'])
    
    holc = list([re.sub(r'[^a-zA-Z0-9]', '', item.replace(',', '').lower()) for item in info['holidays']])
    print(holc)
    prompt = copy.deepcopy(PROMPT_HOLIDAY[:])
    prompt[1]['content'] = prompt[1]['content'].format(info=info)
    
    llm = get_llm(llm_provider="platform_http", version=3)
    output = call_llm(llm, prompt, sleep_time=1)
    print('output: ', output)
    if len(output['top_holidays'])==0:
        return {'top_holidays': []}
    ans = set([re.sub(r'[^a-zA-Z0-9]', '', item.replace(',', '').lower()) for item in output['top_holidays']])
    print(ans)

    best = []
    for i, item in enumerate(holc):
        if item in ans:
            best.append(info['holidays'][i])
    
    output = {"top_holidays": best}
    output = json.dumps(output)
    print('final output: ', output)

    return output

def get_plan(info):
    print('inside plan')
    prompt = copy.deepcopy(PROMPT_PLANNER[:])
    prompt[1]['content'] = prompt[1]['content'].format(info=info)

    llm = get_llm(llm_provider="platform_http", version=3)
    output = call_llm(llm, prompt, sleep_time=1)
    
    return output

def get_plan_v2(info):

    today = str(date.today())
    info['today_date'] = str(today)
    print('inside plan')
    prompt = copy.deepcopy(PROMPT_PLANNER_V2[:])
    prompt[1]['content'] = prompt[1]['content'].format(info=info)

    llm = get_llm(llm_provider="platform_http", version=3)
    output = call_llm(llm, prompt, sleep_time=1)
    
    return output

    
def gen_img(inp, height=1024, width=1024):
    
    payload = {"prompt": inp,"negatvive_prompt": IMAGE_NEG_PROMPT, "steps": 50, "height": height, "width": width,"sampler_index": "DPM++ 2M Karras", "cfg_scale": 30, "denoising_strength": 1}
    response = requests.post(url=f'http://10.102.51.94:7861/sdapi/v1/txt2img', json=payload, timeout=30)
    
    r = response.json()
    print(r)
        
    return {"items": r['images']}    
    
def copy_to_s3(name):
    
    aws_access_key = ''
    aws_secret_key = ''
    print(aws_access_key, aws_secret_key)
    # Replace this with your S3 bucket name
    bucket_name = 'test-fm'
    url = f"https://{bucket_name}.s3.amazonaws.com/hackathon-event-cards/{name}"
    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    print('made')
    local_file_path = f'/tmp/{name}'
    s3_object_key = f'hackathon-event-cards/{name}'  # The object key in your S3 bucket

    # Upload the file to your S3 bucket
    s3.upload_file(local_file_path, bucket_name, s3_object_key)


def get_card(info):
    print('inside plan')
    prompt = copy.deepcopy(PROMPT_CARDS[:])
    prompt[1]['content'] = prompt[1]['content'].format(info=info)
    # llm = get_llm(llm_provider="platform_http", version=3)
    # output = call_llm(llm, prompt, sleep_time=1)
    # output = {"prompt": f"{info.get('festival', '')} themed image postcard, depicting the products from {info.get('industry', '')} industry. Highly detailed. Highly Detailed. Realistic. Professional Photography"}
    output = {"prompt": f"{info.get('festival', '')} themed bulletin board, depicting the products from {info.get('industry', '')} industry. Highly detailed. Highly Detailed. Realistic. Photography"}
    # industry = info.get('industry', '')
    # ocassion = info.get('festival', '')
    # print(industry, ocassion)
    # output = {"prompt": f"Image with theme of ocassion of {ocassion} in style of a beautiful painting by da vinci"}
    # print(output)
    output = gen_img(output['prompt'], height=1024, width=683)
    return output
    # print(output)
    # image = Image.open(io.BytesIO(base64.b64decode(output['items'][0].split(",",1)[0])))
    # name = f"{info.get('festival', 'temp').lower()}.png"
    # im1 = image.save(r"/tmp/name")
    # print(name)

    # url = copy_to_s3(name)
    # print(url)
    # return url
    
def get_banner(info):
    print('inside plan')
    prompt = copy.deepcopy(PROMPT_BANNER[:])
    prompt[1]['content'] = prompt[1]['content'].format(info=info)
    llm = get_llm(llm_provider="platform_http", version=3)
    output = call_llm(llm, prompt, sleep_time=1)
    print(output)
    output = gen_img(output['prompt'], height=510, width=1024)

    return output

def get_content_email(content: dict):

    context = content.get("context", "")
    return {"email_content": generate_content(context)}

def get_content_whatsapp(content: dict):

    context = content.get("context", "")

    return {"whatsapp_content": generate_content(context)}

def get_prompt_image(content: dict):

    context = content.get("context", "")
    return {"image_prompt": generate_content(context)}

def get_image(context: dict):
    print('context: ', context)
    payload = {"prompt": context.get("prompt", "beautiful template"),"negatvive_prompt": IMAGE_NEG_PROMPT, "steps": 30, "height": context.get("height", 1024), "width": context.get("width", 1024),"sampler_index": "DPM++ 2M Karras"}
    response = requests.post(url=f'http://10.102.51.94:7861/sdapi/v1/txt2img', json=payload, timeout=30)

    r = response.json()
    print(r)
    # generated_images = []
    # for i in r['images']:
    #     image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
    #     img_byte_array = io.BytesIO()
    #     img_bytes = img_byte_array.getvalue()
    #     # Encode the image bytes as base64 for the response
    #     encoded_image = base64.b64encode(img_bytes).decode('utf-8')
    #     generated_images.append(encoded_image)
        
    return {"items": r['images']}

def get_product_specific(context: dict):
    print('context: ', context)
    product = context.get('product', 'sunscreen')
    payload = {"prompt": f"ohwx product <lora:{product}:1>, {context.get("prompt")}", "negatvive_prompt": IMAGE_NEG_PROMPT, "steps": 30, "height": context.get("height", 1024), "width": context.get("width", 1024),"sampler_index": "DPM++ 2M Karras"}
    response = requests.post(url=f'http://10.102.51.94:7861/sdapi/v1/txt2img', json=payload, timeout=60)

    r = response.json()
    return {"items": r['images']}


def get_image2(content: dict):
        
    urls = content.get("context", "")
    folder_name = content.get("name", "PQRW")
    model_name = content.get("model_name", "test")
    
        
    return {"items": generated_images}
