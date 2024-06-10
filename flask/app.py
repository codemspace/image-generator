from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

DATABASE_URL = os.getenv('DATABASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PROXY_URL = os.getenv('PROXY_URL')  # Proxy URL with optional authentication
print(PROXY_URL)

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class GeneratedImage(Base):
    __tablename__ = 'generated_images'
    id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    image_url = Column(String, nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# @app.route('/', methods=['GET'])
# def get_generate_image():
#     logging.debug('GET request received at /generate-image')
#
#     return jsonify({'image_url'})

@app.route("/")
def hello_world():
    return f"<p>Hello, World!</p>"


@app.route('/generate-image', methods=['POST'])
def generate_image():
    logging.debug('POST request received at /generate-image')

    data = request.get_json()
    logging.debug(f'Request data: {data}')

    if not data or 'prompt' not in data:
        logging.error('Prompt is required')
        return jsonify({'error': 'Prompt is required'}), 400

    prompt = data['prompt']

    # Refined prompt with more details
    refined_prompt = f"High-quality, detailed image of {prompt}, 4K resolution, photorealistic"

    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    json_data = {
        'prompt': refined_prompt,
        'n': 4,  # Number of images to generate
        'size': '1024x1024'
    }
    proxies = {
        'http': PROXY_URL,
        'https': PROXY_URL,
    } if PROXY_URL else None

    try:
        response = requests.post(url, headers=headers, json=json_data, proxies=proxies)
        response.raise_for_status()
        image_urls = [item['url'] for item in response.json()['data']]
    except requests.exceptions.RequestException as e:
        logging.error(f'Error generating image: {e}')
        return jsonify({'error': 'Failed to generate image'}), 500

    new_images = [GeneratedImage(prompt=prompt, image_url=url) for url in image_urls]
    session.add_all(new_images)
    session.commit()

    return jsonify({'image_urls': image_urls})


if __name__ == '__main__':
    logging.debug('Starting Flask application')
    app.run(debug=True)
