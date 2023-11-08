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

from pathlib import Path

from commons.template_utils import (
    replace_content_in_template,
    escape_unsafe_characters,
    replace_content_in_editor_configuration,
)

from random import shuffle

ALL_PRODUCTS = {
    "beautifying-serum": {"store": "https://stack16test.myshopify.com/products/beautifying-serum", "image": "https://stack16test.myshopify.com/cdn/shop/files/1_6_906x1156_81b6a386-134c-4ec0-a35c-8312d4403b39.jpg"},
    "chocolate-lip-balm": {"store": "https://stack16test.myshopify.com/products/chocolate-lip-balm", "image": "https://stack16test.myshopify.com/cdn/shop/files/62-Chocolatelipbalm-3_904x1156_5c1bcf39-fd0c-4c96-9210-129b341d9bed.jpg"},
    "coconut-milk-shampoo-bar": {"store": "https://stack16test.myshopify.com/products/coconut-milk-shampoo-bar", "image": "https://stack16test.myshopify.com/cdn/shop/files/CoconutMilkShampooBar_1_906x1154_1d80879d-b8c6-4cfc-ba64-8bee6ee7007b.jpg"},
    "eucalyptus-essential-oil": {"store": "https://stack16test.myshopify.com/products/eucalyptus-essential-oil", "image": "https://stack16test.myshopify.com/cdn/shop/files/Eucalyptus_600x767_9374f437-4188-4c0c-90ad-17adad5e52c6.jpg"},
    "hair-growth-oil": {"store": "https://stack16test.myshopify.com/products/hair-growth-oil", "image": "https://stack16test.myshopify.com/cdn/shop/files/47-05_905x1156_fe9e4fb9-e34d-4f90-8e96-48214daf66a0.jpg"},
    "lemon-mist": {"store": "https://stack16test.myshopify.com/products/lemon-mist", "image": "https://stack16test.myshopify.com/cdn/shop/files/Lemon_600x767_b42d5865-d0d3-47ba-bfbd-b0e9895e0786.jpg"},
    "man-body-powder": {"store": "https://stack16test.myshopify.com/products/man-body-powder", "image": "https://stack16test.myshopify.com/cdn/shop/files/MenBodyPowder_904x1156_5be7d05a-9deb-464f-bb91-755d3252e1d2.jpg"},
    "rice-water-shampoo-220ml": {"store": "https://stack16test.myshopify.com/products/rice-water-shampoo-220ml", "image": "https://stack16test.myshopify.com/cdn/shop/files/1-03_2_904x1156_c3ed2cd1-0012-4943-992d-cee1b2fce8c2.png"},
    "rose-scrub": {"store": "https://stack16test.myshopify.com/products/rose-scrub", "image": "https://stack16test.myshopify.com/cdn/shop/files/Rose_1_600x767_c788a90a-9f10-4af8-bd71-6fadb173e7e5.jpg"},
    "strawberry-lip-scrub": {"store": "https://stack16test.myshopify.com/products/strawberry-lip-scrub", "image": "https://stack16test.myshopify.com/cdn/shop/files/5_1407x1800_e5e9e345-494e-453a-88ef-7977d87ba661.png"},
    "sunscreen-spf-50": {"store": "https://stack16test.myshopify.com/products/sunscreen-spf-50", "image": "https://stack16test.myshopify.com/cdn/shop/files/5_2_906x1156_0601206c-48c3-48ce-9603-dbe2b69015d6.jpg"}
}


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
    
    payload = {"prompt": inp,"negatvive_prompt": IMAGE_NEG_PROMPT, "steps": 40, "height": height, "width": width,"sampler_index": "DPM++ 2M Karras", "cfg_scale": 7}
    response = requests.post(url=f'http://10.102.51.94:7861/sdapi/v1/txt2img', json=payload, timeout=5000)
    
    r = response.json()
    print(r)
        
    return {"items": r['images']}    
    
def upload_to_aws(val):
    print(val)
    # data = {'data': val}
    # headers = {"Content-Type": "application/json"}
    # url = 'https://s1ywpatgnb.execute-api.us-east-1.amazonaws.com/test/save_image_v2'
    # response = requests.post(url, json=val, headers=headers)
    # print(response.text)
    # r = response.text
    url = "https://s1ywpatgnb.execute-api.us-east-1.amazonaws.com/test/save_image_v2"

    payload = str({'data': val})
    headers = {
      'Content-Type': 'text/plain'
    }
    

    response = requests.request("POST", url, headers=headers, data=payload)
    r = response.text
    return r
    
def upload_to_aws2(val):
    print(val)
    # data = {'data': val}
    # headers = {"Content-Type": "application/json"}
    # url = 'https://s1ywpatgnb.execute-api.us-east-1.amazonaws.com/test/save_image_v2'
    # response = requests.post(url, json=val, headers=headers)
    # print(response.text)
    # r = response.text
    url = "https://s1ywpatgnb.execute-api.us-east-1.amazonaws.com/test/save_image_v2"
    
    payload = str({'data': str(val)})
    headers = {
      'Content-Type': 'text/plain'
    }
    

    response = requests.request("POST", url, headers=headers, data=payload)
    r = response.text
    return r


def get_card(info):
    print('inside plan')
    # prompt = copy.deepcopy(PROMPT_CARDS[:])
    # prompt[1]['content'] = prompt[1]['content'].format(info=info)
    # llm = get_llm(llm_provider="platform_http", version=3)
    # output = call_llm(llm, prompt, sleep_time=1)
    # output = {"prompt": f"{info.get('festival', '')} themed image postcard, depicting the products from {info.get('industry', '')} industry. Highly detailed. Highly Detailed. Realistic. Professional Photography"}
    output = {"prompt": f"{info.get('festival', '')} themed bulletin board, with products from {info.get('industry', '')} industry. Keep the background color to: {info.get('background', 'yellow')}. Human thoughts art, elegant fantasy, intricate, crisp quality, 35mm film, 35mm photography, 8k uhd, hdr, ultra-detailed, (style of Vassily Kandinsky). Masterpiece, expert, insanely detailed, 4k resolution, best quality, high quality, vivid, detailed background, otherworldly, digital art, ebula, cinematic, dreaming, Film light, bathing in light, very sharp focus, Hyper detailed, Hyper realistic, masterpiece, spiritual, surreal, atmospheric,High resolution, Vibrant, High contrast, Ultra-detail, (highres:1.1), best quality, (masterpiece:1.3), cinematic lighting"}
    # output = {"prompt": f"{info.get('festival', '')} themed, with products from {info.get('industry', '')} industry. Tatami Galaxy Style, detailed, fineart, minimilistic"}
    
    # industry = info.get('industry', '')
    # ocassion = info.get('festival', '')
    # print(industry, ocassion)
    # output = {"prompt": f"Image with theme of ocassion of {ocassion} in style of a beautiful painting by da vinci"}
    # print(output)
    output = gen_img(output['prompt'], height=1000, width=600)
    # output = gen_img(output['prompt'], height=512, width=512)
    
    
    output = upload_to_aws(output['items'][0])
    return output
    # print(output)
    # image = Image.open(io.BytesIO(base64.b64decode(output['items'][0].split(",",1)[0])))
    # name = f"{info.get('festival', 'temp').lower()}.png"
    # im1 = image.save(r"/tmp/name")
    # print(name)

    # url = copy_to_s3(name)
    # print(url)
    # return url

def get_cardv2(info):
    print('inside plan')
    # prompt = copy.deepcopy(PROMPT_CARDS[:])
    # prompt[1]['content'] = prompt[1]['content'].format(info=info)
    # llm = get_llm(llm_provider="platform_http", version=3)
    # output = call_llm(llm, prompt, sleep_time=1)
    # output = {"prompt": f"{info.get('festival', '')} themed image postcard, depicting the products from {info.get('industry', '')} industry. Highly detailed. Highly Detailed. Realistic. Professional Photography"}
    output = {"prompt": f"{info.get('festival', '')} themed bulletin board, with products from {info.get('industry', '')} industry. Keep the background color to: {info.get('background', 'yellow')}. Human thoughts art, elegant fantasy, intricate, crisp quality, 35mm film, 35mm photography, 8k uhd, hdr, ultra-detailed, (style of Vassily Kandinsky). Masterpiece, expert, insanely detailed, 4k resolution, best quality, high quality, vivid, detailed background, otherworldly, digital art, ebula, cinematic, dreaming, Film light, bathing in light, very sharp focus, Hyper detailed, Hyper realistic, masterpiece, spiritual, surreal, atmospheric,High resolution, Vibrant, High contrast, Ultra-detail, (highres:1.1), best quality, (masterpiece:1.3), cinematic lighting"}
    # output = {"prompt": f"{info.get('festival', '')} themed, with products from {info.get('industry', '')} industry. Tatami Galaxy Style, detailed, fineart, minimilistic"}
    
    # industry = info.get('industry', '')
    # ocassion = info.get('festival', '')
    # print(industry, ocassion)
    # output = {"prompt": f"Image with theme of ocassion of {ocassion} in style of a beautiful painting by da vinci"}
    # print(output)
    output = gen_img(output['prompt'], height=1000, width=600)

    return output['items'][0]

 
def get_banner(info):
    print('inside plan')
    prompt = copy.deepcopy(PROMPT_BANNER[:])
    prompt[1]['content'] = prompt[1]['content'].format(info=info)
    # llm = get_llm(llm_provider="platform_http", version=3)
    # output = call_llm(llm, prompt, sleep_time=1)
    output = {"prompt": f"{info.get('festival', '')} themed vector art poster, include products from {info.get('industry', '')} industry. intricate, crisp quality, 35mm film, 35mm photography, 8k uhd, hdr, ultra-detailed. Masterpiece, expert, insanely detailed, 4k resolution, best quality, high quality, vivid, detailed background, otherworldly, digital art, ebula, cinematic, dreaming, Film light, bathing in light, very sharp focus, Hyper detailed, Hyper realistic, masterpiece, spiritual, surreal, atmospheric, High resolution, Vibrant, High contrast, Ultra-detail, (highres:1.1), best quality, (masterpiece:1.3), cinematic lighting"}
    
    print(output)
    output = gen_img(output['prompt'], height=800, width=1200)
    output = upload_to_aws(output['items'][0])
    return output
    
def get_bannerv2(info):
    print('inside plan')
    prompt = copy.deepcopy(PROMPT_BANNER[:])
    prompt[1]['content'] = prompt[1]['content'].format(info=info)
    # llm = get_llm(llm_provider="platform_http", version=3)
    # output = call_llm(llm, prompt, sleep_time=1)
    output = {"prompt": f"{info.get('festival', '')} themed vector art poster, include products from {info.get('industry', '')} industry. intricate, crisp quality, 35mm film, 35mm photography, 8k uhd, hdr, ultra-detailed. Masterpiece, expert, insanely detailed, 4k resolution, best quality, high quality, vivid, detailed background, otherworldly, digital art, ebula, cinematic, dreaming, Film light, bathing in light, very sharp focus, Hyper detailed, Hyper realistic, masterpiece, spiritual, surreal, atmospheric, High resolution, Vibrant, High contrast, Ultra-detail, (highres:1.1), best quality, (masterpiece:1.3), cinematic lighting"}
    
    print(output)
    output = gen_img(output['prompt'], height=800, width=1200)
    
    return output['items'][0]

def get_content_email(content: dict):

    context = content.get("context", "")
    

    output = generate_content(context)

    ##
    
    replace_content_in_template()

    # product_id
    # product_url
    # product_image_url

    html_body_path = "template.html"
    json_body_path = "bee2.json"

    response ={}
    resources_base = Path(__file__).parent.resolve() / "resources" 
    with (resources_base / html_body_path).open() as template, (
            resources_base / json_body_path
        ).open() as editor_config:

            response_output = json.loads(output)
            response ={}

            response["subject"] = response_output["Subject"]
            response["title"] = response_output["Title"]


            sanitized_template_content = escape_unsafe_characters(response_output["Body"])



            updated_template = replace_content_in_template(
                template.read(), sanitized_template_content,links=[],recommended_product={}
            )

            updated_configuration = replace_content_in_editor_configuration(
            editor_config.read(),sanitized_template_content,links=[],recommended_product={})


            response["html"]= updated_template
            response["json"]= updated_configuration
            


    return {"email_content": response}

def get_content_whatsapp(content: dict):

    context = content.get("context", "")

    return {"whatsapp_content": generate_content(context)}

def get_prompt_image(content: dict):

    context = content.get("context", "")
    return {"image_prompt": generate_content(context)}

def get_image(context: dict):
    print('context: ', context)
    
    payload = {"prompt": context.get("prompt", "beautiful template")+ "intricate, crisp quality, 35mm film, 35mm photography, 8k uhd, hdr, ultra-detailed. Masterpiece, expert, insanely detailed, 4k resolution, best quality, high quality, vivid, detailed background, otherworldly, digital art, ebula, cinematic, dreaming, Film light, bathing in light, very sharp focus, Hyper detailed, Hyper realistic, masterpiece, spiritual, surreal, atmospheric, High resolution, Vibrant, High contrast, Ultra-detail, (highres:1.1), best quality, (masterpiece:1.3), cinematic lighting","negatvive_prompt": IMAGE_NEG_PROMPT, "steps": 40, "height": context.get("height", 750), "width": context.get("width", 750),"sampler_index": "DPM++ 2M Karras"}
    response = requests.post(url=f'http://10.102.51.94:7861/sdapi/v1/txt2img', json=payload, timeout=5000)

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
    output = upload_to_aws(r['images'][0])
    return output
    
def get_url(context):
    print('get url:')
    # image = literal_eval(context["image"])

    output = upload_to_aws2(context)
    return output

def get_product_specific(context: dict):
    print('context: ', context)
    product = context.get('product', 'shampoo')
    payload = {"prompt": f"ohwp product <lora:{product}:1>, {context.get('prompt')}", "negatvive_prompt": IMAGE_NEG_PROMPT, "steps": 50, "height": context.get("height", 750), "width": context.get("width", 750),"sampler_index": "DPM++ 2M Karras"}
    response = requests.post(url=f'http://10.102.51.94:7861/sdapi/v1/txt2img', json=payload, timeout=60)

    r = response.json()
    # return r['images'][0]
    output = upload_to_aws(r['images'][0])
    return output

def get_recommmendation(context):

    keys = list(ALL_PRODUCTS.keys())
    shuffle(keys)

    items = [ALL_PRODUCTS[item] for item in keys[:3]]

    return items




def get_image2(content: dict):
        
    urls = content.get("context", "")
    folder_name = content.get("name", "PQRW")
    model_name = content.get("model_name", "test")
    
        
    return {"items": generated_images}

    
