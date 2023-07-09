import json
import os
from typing import Dict, List

import openai
from dotenv import load_dotenv, find_dotenv

class ImageGenerator:
    def __init__(self, collection_file: str = 'images_collection.json'):
        self.collection_file = collection_file
        self.images_collection = self.load_collection()
        self.image_data_keys = ["id", "image_url", "prompt"]

    def generate_an_image(self, prompt: str, size: str = "512x512") -> str:
        '''accepts an image prompt and size
        available sizes: 256x256, 512x512, or 1024x1024
        '''
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
        return response['data'][0]['url']

    def get_prompt_from_user(self) -> str:
        prompt = input('\nWhat image would you like me to create?\n')
        prompt = 'illustration of ' + prompt
        return prompt

    def save_image_to_collection(self, id: str, image_url: str, prompt: str):
        image_data = {
            "id": id,
            "image_url": image_url, 
            "prompt": prompt
        }
        self.images_collection.append(image_data)
        self.save_collection()

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
        if self.images_collection:
            max_id = max(image['id'] for image in self.images_collection)
            return str(int(max_id) + 1)
        else:
            return '1'


def main():
    # read in the environment variable with the API value
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv('./config/.env'))

    openai.api_key  = os.getenv('OPENAIKEY')

    image_gen = ImageGenerator()
    prompt = image_gen.get_prompt_from_user()
    image_url = image_gen.generate_an_image(prompt)
    id = image_gen.generate_id()
    image_gen.save_image_to_collection(id, image_url, prompt)
    print(f'Image: {image_url}')



if __name__ == '__main__':
    main()