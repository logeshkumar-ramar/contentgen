import subprocess
import shutil
import os
import wget
import shutil
import cv2
import boto3

class LoraTrain:

    def __init__(self, base_path) -> None:

        self.base_path = base_path
        self.pretrained_model = "/home/abhishekpal/models/juggernautXL_version5.safetensors"#"/home/abhishekpal/stable-diffusion-webui/models/Stable-diffusion/sd_xl_base_1.0_0.9vae.safetensors"#bonniebelle/juggernaut-xl-v5"#"r"stabilityai/stable-diffusion-xl-base-1.0"
        self.s3 = boto3.client('s3')
        self.bucket = "freddy-freshsales-staging"
        self.s3_key = "abhishek/lora_models"
    def get_folder(self, paths, random_word):

        os.mkdir(f'{self.base_path}/{random_word}_LORA')
        os.mkdir(f'{self.base_path}/{random_word}_LORA/model')
        os.mkdir(f'{self.base_path}/{random_word}_LORA/image')
        os.mkdir(f'{self.base_path}/{random_word}_LORA/log')
        os.mkdir(f'{self.base_path}/{random_word}_LORA/image/200_{random_word.lower()}')

        for i, item in enumerate(paths):
            pt = f'{self.base_path}/{random_word}_LORA/image/200_{random_word.lower()}/img{i}.png'
            nm = '/tmp/'+item.split('/')[-1]
            wget.download(item, nm)
            img = cv2.imread(nm)
            cv2.imwrite(pt, img)

        for item in os.listdir(f'{self.base_path}/{random_word}_LORA/image/200_{random_word.lower()}'):
            val = item.split('.')[0]
            with open(f'{self.base_path}/{random_word}_LORA/image/200_{random_word.lower()}/{val}.txt', 'w') as fp:
                fp.write(random_word.lower()+" product")
        items = os.listdir(f'{self.base_path}/{random_word}_LORA/image/200_{random_word.lower()}')
        ct = len(paths)
        tg = 15
        while(1):
            for i in range(ct):
                src = f'{self.base_path}/{random_word}_LORA/image/200_{random_word.lower()}/img{i}.txt'
                dst = f'{self.base_path}/{random_word}_LORA/image/200_{random_word.lower()}/img{ct}.txt'
                shutil.copy(src, dst)
                src = f'{self.base_path}/{random_word}_LORA/image/200_{random_word.lower()}/img{i}.png'
                dst = f'{self.base_path}/{random_word}_LORA/image/200_{random_word.lower()}/img{ct}.png'
                shutil.copy(src, dst)
                ct += 1
                if ct>=tg:
                    break
            if ct>=tg:
                break

    def train(self, paths, name_path, prod_name):

        #self.get_folder(paths, name_path)

        train_data_dir = r"{}/{}_LORA/image".format(self.base_path, name_path)
        output_dir = r"{}/{}_LORA/model".format(self.base_path, name_path)
        log_dir = r"{}/{}_LORA/log".format(self.base_path, name_path)
        output_name = prod_name#name_path.split('_')[0]

        print(train_data_dir)
        print(output_dir)
        print(log_dir)

        run_cmd = f'accelerate launch --num_cpu_threads_per_process=2 ../kohya_ss/sdxl_train_network.py --enable_bucket --min_bucket_reso=256 --max_bucket_reso=2048 --pretrained_model_name_or_path="{self.pretrained_model}" --train_data_dir="{train_data_dir}" --resolution="1024,1024" --output_dir="{output_dir}" --logging_dir="{log_dir}" --network_alpha="1" --save_model_as=safetensors --network_module=networks.lora --text_encoder_lr=5e-05 --unet_lr=0.001 --network_dim=8 --output_name="{output_name}" --lr_scheduler_num_cycles="1" --no_half_vae --learning_rate="0.001" --lr_scheduler="cosine" --lr_warmup_steps="50" --train_batch_size="1" --max_train_steps="500" --save_every_n_epochs="1" --mixed_precision="fp16" --save_precision="fp16" --cache_latents --optimizer_type="AdamW8bit" --max_data_loader_n_workers="0" --bucket_reso_steps=64 --xformers --bucket_no_upscale --noise_offset=0.0'
#        run_cmd = r"{}".format(run_cmd)
        print(run_cmd)
        #subprocess.run(run_cmd, shell=True)
        print(f"{self.base_path}/{name_path}_LORA/model/{output_name}.safetensors")
        print(self.bucket)
        print(self.s3_key+f'/{output_name}.safetensors')
        self.s3.upload_file(f"{self.base_path}/{name_path}_LORA/model/{output_name}.safetensors", self.bucket, self.s3_key+f'/{output_name}.safetensors')
        folder_path = r"{}/{}_LORA".format(self.base_path, name_path)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        else:
            print("Folder does not exist.")
        #shutil.copy(f"{self.base_path}/{name_path}_LORA/model/{output_name}.safetensors", f"../stable-diffusion-webui/models/Lora/{output_name}.safetensors")
