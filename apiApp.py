from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from flask_cors import CORS
import json

# Initialize the Flask app
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
        
        # Assuming the decrypted text is a JSON string, parse it
        decrypted_json = json.loads(decrypted_text)

        # Return the decrypted data as JSON response
        return jsonify(decrypted_json)

    except Exception as e:
        # Return error message if decryption fails
        return jsonify({'error': str(e)}), 400

# Run the application (use host='0.0.0.0' when deploying to external server)
if __name__ == '__main__':
    # Set host='0.0.0.0' to make it accessible externally, and run on port 5000.
    app.run(debug=True, host='0.0.0.0', port=5000)
