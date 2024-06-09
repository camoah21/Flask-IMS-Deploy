from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import pytesseract;
from PIL import Image
app = Flask(__name__)
inventory = {}




@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    bill_of_lading = data['billOfLading']
    item_name = data['itemName']
    item_quantity = data['itemQuantity']
    item_price = data['itemPrice']

    inventory[bill_of_lading] = {
        'name': item_name,
        'quantity': item_quantity,
        'price': item_price
    }
    return jsonify(inventory)

@app.route('/get_inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)

        # Process the image to extract "B/L & INV" number
        image = Image.open(file_path)
        left, top, right, bottom = 500, 60, 700, 120  # Adjust these coordinates as needed
        cropped_image = image.crop((left, top, right, bottom))
        bl_inv_number = pytesseract.image_to_string(cropped_image, config='--psm 6').strip()

        # Here, add processing of the text file content if needed
        # This part of the code assumes you are uploading text files as well
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    bill_of_lading, item_name, item_quantity, item_price = line.strip().split(',')
                    inventory[bill_of_lading] = {
                        'name': item_name,
                        'quantity': int(item_quantity),
                        'price': float(item_price)
                    }

        return jsonify({'bl_inv_number': bl_inv_number, 'inventory': inventory})

@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



