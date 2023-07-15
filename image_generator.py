import json
import os
import requests
from typing import Dict, List
from datetime import datetime

import openai
from dotenv import load_dotenv, find_dotenv

class ImageGenerator:
    def __init__(self, collection_file: str = 'images_collection.json'):
        self.prompt=''
        self.image_url=''
        self.image_name = self.set_image_name()
        self.collection_file = collection_file
        self.images_collection = []
        self.image_data_keys = ["id", "prompt", "image_name", "image_url"]

    def get_prompt_from_user(self) -> str:
        prompt = input('\nWhat image would you like me to create?\n')
        prompt = 'illustration of ' + prompt
        return prompt

    def save_collection(self):
        with open(self.collection_file, 'w') as f:
            json.dump(self.images_collection, f)

    def load_collection(self) -> List[Dict[str, str]]:
        if os.path.exists(self.collection_file):
            with open(self.collection_file, 'r') as f:
                return json.load(f)
        else:
            return []

    def generate_id(self) -> str:
        # empty list is 'falsy'
        if self.images_collection:
            max_id = max(image['id'] for image in self.images_collection)
            return str(int(max_id) + 1)
        else:
            return '1'

    def generate_an_image(self, prompt: str, size: str = "512x512") -> str:
        '''accepts an image prompt and size
        available sizes: 256x256, 512x512, or 1024x1024
        '''
        self.prompt=prompt
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
        self.image_url = response['data'][0]['url']
        return self.image_url

    def set_image_name(self, path: str ='./data/gallery/', name_prefix: str = 'dalee_') -> str:
            # Get the current datetime
            now = datetime.now()
            # Format the datetime as a string
            now_str = now.strftime('%Y%m%d%H%M%S')
            filename = f'{path}{name_prefix}{now_str}.jpg'
            return filename

    def save_image_to_collection(self, id: str):
        image_data = {
            "id": id,
            "prompt": self.prompt,
            "image_name": self.image_name,
            "image_url": self.image_url
        }
        self.images_collection.append(image_data)
        self.save_collection()

    def download_image(self) -> str:
        response = requests.get(self.image_url, stream=True)
        if response.status_code == 200:
            # Open the file in write and binary mode
            with open(self.image_name, 'wb') as f:
                f.write(response.content)
            return self.image_name


def main():
    # read in the environment variable with the API value
    _ = load_dotenv(find_dotenv('./config/.env'))

    openai.api_key  = os.getenv('OPENAIKEY')

    image_gen = ImageGenerator()
    prompt = image_gen.get_prompt_from_user()
    image_url = image_gen.generate_an_image(prompt)
    id = image_gen.generate_id()
    image_gen.save_image_to_collection(id, image_url, prompt)


if __name__ == '__main__':
    main()