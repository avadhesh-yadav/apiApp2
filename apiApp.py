from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for any Salesforce instance (wildcard for Salesforce domains)
CORS(app, origins=["https://*.lightning.force.com", "https://*.force.com"])

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        # Extract the encrypted token and key from the request
        encrypted_token = data.get('token')
        key = data.get('key')

        # Ensure the token and key are provided
        if not encrypted_token or not key:
            return jsonify({'error': 'Both token and key must be provided'}), 400

        # Create a Fernet object with the provided key
        f = Fernet(key)

        # Decrypt the token
        decrypted_text = f.decrypt(encrypted_token.encode('utf-8')).decode('utf-8')

        # Return the decrypted text
        return jsonify({'decrypted': decrypted_text})

    except Exception as e:
        # Return error message if decryption fails
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
