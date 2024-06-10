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
    data = request.json
    logging.debug(f'Request data: {data}')

    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    url = 'https://api.openai.com/v1/images/generations'

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
    }
    json_data = {
        'prompt': prompt,
        'n': 1,
        'size': '1024x1024'
    }
    proxy = {
        'http': PROXY_URL,
        'https': PROXY_URL,
    }
    try:
        response = requests.post(url, headers=headers, json=json_data, proxies=proxy)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f'Error generating image: {e}')
        return jsonify({'error': 'Failed to generate image'}), 500

    image_url = response.json()['data'][0]['url']

    new_image = GeneratedImage(prompt=prompt, image_url=image_url)
    session.add(new_image)
    session.commit()

    return jsonify({'image_url': image_url})


if __name__ == '__main__':
    logging.debug('Starting Flask application')
    app.run(debug=True)
