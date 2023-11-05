"""
Wrapper Module for Platform GPT APIs
"""

import time
import json
import requests
import jwt
from commons.config import LLMConfig


class GPTResponse(dict):
    """Data Structure for platform GPT Response"""

    def __init__(self, **kwargs):
        self.d = dict(kwargs)
    def __getattr__(self, key, default=None):
        try:
            return self.d[key]
        except AttributeError:
            return default
        


class PlatformGPT:
    """Class for platform GPT wrapper implementation"""

    def __init__(self, version):
        self.version = version
        self.config = LLMConfig()
        
        self.headers = {
                'Content-Type': self.config.header_content_type,
                'Authorization': f'Bearer {self._get_jwt_auth_token()}',
                'Freddy-Ai-Platform-Authorization': self.config.header_freddy_ai_platform_authorization,
                'AI-Model-Version': self.config.header_ai_model_version
        }

        self.role_lc_req = {"human": "user",
                            "system": "system",
                            "ai": "assistant"}
        
        if self.version == 4:
          self.config = {'model': self.config.model_gpt4,
                        'url': self.config.url_gpt4,
                        'max_tokens': self.config.max_tokens}
        
        elif self.version==3:
          self.config = {'model': self.config.model_gpt3,
                        'url': self.config.url_gpt3,
                        'max_tokens': 400}
        else:
          raise Exception(f"Version {self.version} is not supported by platform")

    def _convert_lc_to_request_prompt(self, prompt):
        """function for converting the format of input prompt as required for platform GPT
        Parameters
        ----------
            prompt         : list[dict]

        Returns
        ---------
            : list[dict]
        """

        prompt_messages = [{"role": self.role_lc_req[message["type"]], "content": message["content"]} for message in prompt]
        return prompt_messages

    def __call__(self, prompt, sleep_time):
        """function for calling GPT on given prompt input
        Parameters
        ----------
            prompt         : list[dict]
            sleep_time     : bool

        Returns
        ---------
            : GPTResponse
        """

        prompt = self._convert_lc_to_request_prompt(prompt)

        payload = json.dumps({
            "body": {
                "model": self.config["model"],
                "messages": prompt,
                "max_tokens": self.config["max_tokens"]
            }
        })

        if sleep_time is not None:
          time.sleep(sleep_time)
        
        print('url: ',self.config["url"])
        # print('headers: ', self.headers)
        # print('payload: ', payload)
        response = requests.request("POST", self.config["url"], headers=self.headers, data=payload, timeout=20)
        print("GPT response: ",response, response.text)

        response_ns = GPTResponse(**response.json()['choices'][0]['message'])
        return response_ns
    

    def _get_jwt_auth_token(self):
        """function for generating jwt auth token
    
        Returns
        ---------
            : str
        """

        signing_secret = self.config.ai_platform_jwt_secret_key
        token = jwt.encode({"iss": "freddyai_freshmarketer"}, signing_secret, algorithm="HS512")
        return token
