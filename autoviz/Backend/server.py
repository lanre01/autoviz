from flask import Flask, request
from flask_cors import CORS
 
 
# Initializing flask app
app = Flask(__name__)
CORS(app)
 
# Route for seeing a data
@app.route('/compute', methods=['GET','POST'])
def compute():
    #csv_file = request.files['file.csv']
    
    return "<p>Hello, World!</p>"

# Running app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


""" 
import io
from base64 import encodebytes
from PIL import Image
from flask import jsonify

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img

@app.route('/get_images', methods=['GET'])
def get_images():
    result = get_images_from_local_storage()  # Replace with your logic
    encoded_images = [get_response_image(image_path) for image_path in result]
    return jsonify({'result': encoded_images}) 
    
"""
