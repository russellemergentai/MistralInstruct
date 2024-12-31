from flask import Flask, request, jsonify
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from google.cloud import secretmanager

def access_secret_version(project_id, secret_id, version_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Get the token from Secrets Manager
project_id = "corded-photon-441814-g7"  # Replace with your actual project ID
secret_id = "HF_HUB_TOKEN"  # projects/226946013448/secrets/HF_HUB_TOKEN
version_id = "latest"  # Use the latest version of the secret
huggingface_token = access_secret_version(project_id, secret_id, version_id)

# Set the token as an environment variable
os.environ["HF_HUB_TOKEN"] = huggingface_token

# Load the model and tokenizer
model_name = "mistralai/Mistral-7B-Instruct"
config = BitsAndBytesConfig(load_in_8bit=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, config=config)

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'missing prompt'}), 400

    # Generate text
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output = model.generate(input_ids, max_length=200)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
