import json
import os
import asyncio
import aiohttp
import time
import random
import re
import pennylane as qml
from pennylane import numpy as np
from textblob import TextBlob
from llama_cpp import Llama
import logging

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

llm = Llama(
  model_path="llama-2-7b-chat.ggmlv3.q8_0.bin",
  n_gpu_layers=-1,
  n_ctx=3900,
)
# Initialize the quantum device
dev = qml.device("default.qubit", wires=4)

# Quantum circuit definition
@qml.qnode(dev)
def quantum_circuit(color_code, amplitude):
    r, g, b = [int(color_code[i:i+2], 16) for i in (1, 3, 5)]
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    qml.RY(r * np.pi, wires=0)
    qml.RY(g * np.pi, wires=1)
    qml.RY(b * np.pi, wires=2)
    qml.RY(amplitude * np.pi, wires=3)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    qml.CNOT(wires=[2, 3])
    return qml.state()

# Sentiment analysis to amplitude mapping
def sentiment_to_amplitude(text):
    analysis = TextBlob(text)
    return (analysis.sentiment.polarity + 1) / 2



# Llama2 text generation and color code extraction
async def llama_generate_and_colorize(session, prompt, max_tokens=3900, chunk_size=980):
    prompt_chunks = [prompt[i:i + chunk_size] for i in range(0, len(prompt), chunk_size)]
    generated_text = ""
    color_code = "#000000"
    for chunk in prompt_chunks:
        output = llm(chunk, max_tokens=min(max_tokens, chunk_size), stop=["Q:", "\n"], echo=True)
        text = output.get("choices", [{}])[0].get("text", "")
        generated_text += text
        color_code = re.findall(r'#[0-9A-Fa-f]{6}', text)[-1] if re.findall(r'#[0-9A-Fa-f]{6}', text) else color_code
    return generated_text, color_code

# Function to split the large JSON file into smaller chunks
def split_json_file(input_file, max_size_mb=1, output_dir='split_jsons'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r') as file:
        data = json.load(file)

    current_file_size = 0
    current_file_data = []
    file_count = 1

    for item in data:
        item_json = json.dumps(item)
        item_size = len(item_json.encode('utf-8'))

        if current_file_size + item_size > max_size_mb * 1024 * 1024:
            with open(f'{output_dir}/part_{file_count}.json', 'w') as output_file:
                json.dump(current_file_data, output_file, indent=4)
            current_file_data = [item]
            current_file_size = item_size
            file_count += 1
        else:
            current_file_data.append(item)
            current_file_size += item_size

    if current_file_data:
        with open(f'{output_dir}/part_{file_count}.json', 'w') as output_file:
            json.dump(current_file_data, output_file, indent=4)

    print(f"Split into {file_count} files.")

# Asynchronous batch sending function
async def send_batch_async(batch, batch_number, session, weaviate_url):
    start_time = time.time()
    tasks = []
    for item in batch:
        if 'id' in item:
            item['message_id'] = item.pop('id')
        if 'mapping' in item and isinstance(item['mapping'], dict):
            item['mapping'] = json.dumps(item['mapping'])
        if 'moderation_results' in item and isinstance(item['moderation_results'], list):
            item['moderation_results'] = json.dumps(item['moderation_results'])
        url = f"{weaviate_url}/objects"
        tasks.append(session.post(url, json={"class": "ChatGPTHistory", "properties": item}))
    responses = await asyncio.gather(*tasks)
    end_time = time.time()

# Main asynchronous function
async def main():
    weaviate_url = "http://"
    timeout = aiohttp.ClientTimeout(total=9990)
    split_json_file('conversations.json')  # Split the large JSON file

    max_chars_per_batch = 2000
    batch_number = 1

    for part_file in os.listdir('split_jsons'):
        with open(f'split_jsons/{part_file}', 'r') as file:
            data = json.load(file)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            while data:
                current_batch = []
                current_char_count = 0
                while current_char_count < max_chars_per_batch and data:
                    item = random.choice(data)
                    data.remove(item)
                    item_json = json.dumps(item)
                    item_size = len(item_json)
                    if current_char_count + item_size <= max_chars_per_batch:
                        current_batch.append(item)
                        current_char_count += item_size
                if current_batch:
                    await send_batch_async(current_batch, batch_number, session, weaviate_url)
                    batch_number += 1
    print("All data sent.")

# Run the main coroutine
asyncio.run(main())
