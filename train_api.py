from train import LoraTrain
llm = get_llm(llm_provider="platform_http", version=3)
app = FastAPI()
import time


@app.post("/train")
async def get_image(content: dict):

    urls = content.get("urls", [])
    folder_name = content.get("name", "PQRW")
    model_name = content.get("model_name", "test")
    lt = LoraTrain('../Images')
    lt.train(urls, folder_name, model_name)

    return "Train Completed"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



"""
    Testing Example:

import requests
from ast import literal_eval
# The URL you want to send the POST request to
url = "http://0.0.0.0:8000/train"

# Data to be sent in the POST request, in this example, we are sending a JSON payload

data = {"urls":["https://deyga.in/cdn/shop/files/1-04_3_900x.png", "https://deyga.in/cdn/shop/files/1-03_2_1024x.png", "https://deyga.in/cdn/shop/files/1-02_4_900x.png", "https://deyga.in/cdn/shop/files/1-05_2_900x.png", "https://deyga.in/cdn/shop/files/1-01_2_900x.png"],
        "name": "OHWP", "model_name": 'bottle_high'}

# Headers, if needed (e.g., to set the content type)
headers = {"Content-Type": "application/json"}

# Make the POST request
response = requests.post(url, json=data, headers=headers)
    """