Server Code (Flask App with Kyber512 and Fernet for Encryption):

python
```
from flask import Flask, request, jsonify
from kyber import Kyber512
from cryptography.fernet import Fernet

app = Flask(__name__)

# Placeholder for server's Kyber512 keypair
server_keys = {
    'public_key': None,
    'secret_key': None
}

# Generate a symmetric key for Fernet
fernet_key = Fernet.generate_key()
f = Fernet(fernet_key)

@app.route('/exchange_key', methods=['GET'])
def exchange_key():
    # Generate Kyber512 keypair
    pk, sk = Kyber512.keygen()
    server_keys['public_key'] = pk
    server_keys['secret_key'] = sk
    return jsonify({'public_key': pk.hex(), 'symmetric_key': fernet_key.decode()})

@app.route('/receive_encrypted', methods=['POST'])
def receive_encrypted():
    data = request.json
    encrypted_message = data['encrypted_message']
    decrypted_message = f.decrypt(encrypted_message.encode()).decode()
    return jsonify({'decrypted_message': decrypted_message})

if __name__ == '__main__':
    app.run(debug=True)
    ```
Client Code (Python Script to Interact with Server):
```
```
python
```
import requests
from kyber import Kyber512
from cryptography.fernet import Fernet

# Request the public key and symmetric key from the server
response = requests.get('http://localhost:5000/exchange_key')
keys = response.json()
server_public_key = bytes.fromhex(keys['public_key'])
symmetric_key = keys['symmetric_key'].encode()

# Initialize Fernet with the symmetric key
f = Fernet(symmetric_key)

# Encrypt a message using Fernet
message = "A really secret message. Not for prying eyes."
encrypted_message = f.encrypt(message.encode())

# Send encrypted message to the server
response = requests.post('http://localhost:5000/receive_encrypted', json={'encrypted_message': encrypted_message.decode()})
print(response.json())
```
This setup uses Kyber512 for the key exchange and Fernet for encrypting the actual message. The server generates a Kyber512 keypair and a Fernet symmetric key, which it shares with the client. The client then uses this symmetric key to encrypt messages, which the server can decrypt.

Remember to install the necessary packages (flask, cryptography, and kyber) in your Python environment.
