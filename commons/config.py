import os
import yaml

import commons.constants as C

global batch_prefix_path, online_prefix_path
batch_prefix_path, online_prefix_path = C.BATCH_CONFIG_PREFIX, C.ONLINE_CONFIG_PREFIX
is_lambda_env = any([os.environ.get("AWS_EXECUTION_ENV", "").startswith("AWS_Lambda") , os.environ.get("AWS_EXECUTION_ENV", "").startswith("AWS_EC2")])


class Struct(dict):
    
    def __init__(self, dobj):
        super(Struct, self).__init__(dobj)
        for k, v in dobj.items():
            if not isinstance(v, dict):
                self[k] = v
            else:
                self[k] = Struct(v)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Struct, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Struct, self).__delitem__(key)
        del self.__dict__[key]


def get_config(config_file, module=None, prefix_path=None, flag_offline=True):
    
    # #if run mode is dev, then read offline config from repo's config
    # #otherwise read offline configs from dbfs location
    # repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # if C.RUN_DEV_MODE:
    #     main_config_dir = os.path.join(repo_path, 'config')
    # else:
    #     main_config_dir = C.MAIN_CONFIG_DIR

    # #add main_dir path
    # if flag_offline:
    #     config_file = os.path.join(main_config_dir, config_file)
    # else:
    #     config_file = os.path.join(C.MAIN_ONLINE_CONFIG_DIR, config_file)

    # #add prefix_path
    # if prefix_path is not None:
    #     config_file = os.path.join(prefix_path, config_file)
    
    # with open(config_file) as handle:
    #     config = yaml.safe_load(handle)

    # if module:
    #     config = config[module]
    
    config = {"ai_platform_jwt_secret_key": os.environ.get("ai_platform_jwt_secret_key"), "header_ai_model_version": os.environ.get('header_ai_model_version'), "header_content_type": os.environ.get('header_content_type'),
                "header_freddy_ai_platform_authorization": os.environ.get('header_freddy_ai_platform_authorization'), "max_tokens": os.environ.get('max_tokens'), "model_gpt3": os.environ.get('model_gpt3'),
                "model_gpt4": os.environ.get('model_gpt4'), "url_gpt3": os.environ.get('url_gpt3'), "url_gpt4": os.environ.get('url_gpt4')}

    return config



class BaseConfig(Struct):
    STAGE = C.PRODUCTION


# configs for offline (batch) setting

class JobConfig(BaseConfig):
    def __init__(self):
        config_dict = get_config(
            config_file=C.JOB_CONFIG, module=C.TRAIN, prefix_path=batch_prefix_path
        )
        super(JobConfig, self).__init__(config_dict)


class ModelConfig(BaseConfig):
    def __init__(self, model_type=None, config_dict=None):
        if config_dict is None:
            config_dict = get_config(
                config_file=C.MODEL_CONFIG,
                module=model_type,
                prefix_path=batch_prefix_path
            )
        super(ModelConfig, self).__init__(config_dict)


class DataConfig(BaseConfig):
    def __init__(self, model_type=None, config_dict=None):
        if config_dict is None:
            config_dict = get_config(
                C.DATA_CONFIG, model_type, prefix_path=batch_prefix_path
            )
        super(DataConfig, self).__init__(config_dict)


class TaskConfig(BaseConfig):
    def __init__(self, category):
        config_dict = get_config(C.TASK_CONFIG, category, prefix_path=batch_prefix_path)
        super(TaskConfig, self).__init__(config_dict)



# configs for online setting


# class SMMMEConfigBatch(BaseConfig):
#     def __init__(self):
#         config_dict = get_config(C.APP_CONFIG, prefix_path=batch_prefix_path,flag_offline=False)
#         super(SMMMEConfigBatch, self).__init__(config_dict)

class APIConfig(BaseConfig):
    def __init__(self):
        config_dict = get_config(C.API_USECASE_CONFIG, prefix_path=online_prefix_path, flag_offline=False)
        super(APIConfig, self).__init__(config_dict)


class SMMMEConfig(BaseConfig):
    def __init__(self):
        config_dict = get_config(C.SMMME_CONFIG, prefix_path=online_prefix_path, flag_offline=False)
        super(SMMMEConfig, self).__init__(config_dict)



#common config for both offline and online setting

class AppConfig(BaseConfig):
    def __init__(self):
        config_dict = get_config(
            config_file=C.APP_CONFIG, prefix_path=batch_prefix_path, flag_offline = not(is_lambda_env)
        )
        super(AppConfig, self).__init__(config_dict)

class SagemakerAppConfig(BaseConfig):
    def __init__(self, base_path=None):
        if base_path is not None:
            config_dict = get_config(
                config_file=C.APP_CONFIG, prefix_path=base_path, flag_offline = False
            )
        else:
            config_dict = get_config(
                config_file=C.APP_CONFIG, prefix_path=online_prefix_path, flag_offline = False
            )
        super(SagemakerAppConfig, self).__init__(config_dict)


class LogConfig(BaseConfig):
    def __init__(self):
        config_dict = get_config(C.LOGGER_CONFIG, prefix_path=online_prefix_path, flag_offline = not(is_lambda_env))
        super(LogConfig, self).__init__(config_dict)


class LLMConfig(BaseConfig):
    def __init__(self):

        config_dict = get_config(C.LLM_CONFIG, prefix_path=online_prefix_path, flag_offline = not(is_lambda_env))

        super(LLMConfig, self).__init__(config_dict)