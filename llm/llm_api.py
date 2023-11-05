"""
Module for LLM APIs
"""

import time
import json
import re

from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

from llm.platform_llm.llm_http import PlatformGPT


def get_llm(llm_provider, version=3, temperature=0):
    """function for instantiating LLM
        Parameters
        ----------
            llm_provider    : str
            version         : int
            temperature     : int

        Returns
        ---------
            : Object 
                - Instance of corresponding LLM provider
    """
    
    if llm_provider == "azure_api":
        
        return ChatOpenAI(
            model_name="gpt-3.5-turbo",
            engine="deployment-92439a0fad024f6381b48e0b41d0e235",
            temperature=temperature,
        )
    
    elif llm_provider == "platform_http":
        return PlatformGPT(version)

    else:
        raise NotImplementedError(
            f'Currenty llm_provider: {llm_provider} is not supported'
        )



def call_llm(llm, prompt, sleep_time=None):
        """
        makes a call to gpt with the given prompt and return back the json response of GPT

        Parameters
        ----------
        prompt: str
            input prompt to gpt
        sleep_time: int
            
        Returns
        -------
        llm_out_json: dict
            json output of gpt
        """
        tic = time.time()
        print('entered')
        with get_openai_callback() as cb:
            print('111')
            llm_output_json_string = llm(prompt, sleep_time).content
        

        tt = time.time() - tic
        print("LLM_TIME_TAKEN", tt)
        # print("LLM_COMPLETION_TOKEN", cb.completion_tokens)
        print(llm_output_json_string)
        llm_output_json_string = llm_output_json_string.replace("\n", " ")
        llm_output_json_string = llm_output_json_string[
            llm_output_json_string.find("{") : llm_output_json_string.rfind("}") + 1
        ]
        llm_output_json_string = llm_output_json_string.replace(',\n}', '}')
        llm_output_json_string = re.sub(r',\s+}', '}', llm_output_json_string)

        

        llm_out_json = json.loads(llm_output_json_string)
        # print(f"LLM Response: {llm_out_json}")
        return llm_out_json


