import base64
import requests
import time
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path='.env.local')

api_key = os.getenv("OPENAI_API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "food.jpg"

base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    # 肉, 野菜, 魚介類, 麺, 揚げ物, 穀物, パン, デザート・スイーツ
                    "text": "画像の料理が次のリストの何%を占めているかjsonで教えて。[Meat, Vegetables, Seafood, Noodles, Fried food, Grains, Bread, Desserts and Sweets] json以外は答えないで",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "auto",
                    }
                }
            ]
        }
    ],
    "max_tokens": 100,
}

start_time = time.time()
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
end_time = time.time()

response_data = response.json()
content = response_data['choices'][0]['message']['content']
json_content = content.strip("```json\n").strip("\n```")
parsed_json = json.loads(json_content)
for key, value in parsed_json.items():
    print(f"{key}: {value}%")

print(f"Response time: {end_time - start_time} seconds")
