import os
import cv2
from paddleocr import PPStructure, draw_structure_result, save_structure_res
from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS, cross_origin
from LLMService import llm_differentiation
from transformers import AutoTokenizer, AutoModel
import torch

app = Flask(__name__)
CORS(app, resources={r"/structureocr": {"origins": "*"}})


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/structureocr', methods=['POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def main():
    if 'image' not in request.files:
        return 'No image file part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        img_path = os.path.join('./', file.filename)
        file.save(img_path)

        table_engine = PPStructure(show_log=True, image_orientation=True)
        llm_differentiation = llm_differentiation

        save_folder = './output'
        img = cv2.imread(img_path)
        result = table_engine(img)

        save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])

        for line in result:
            line.pop('img')
            print(line)

        from PIL import Image

        font_path = './simfang.ttf'
        image = Image.open(img_path).convert('RGB')
        im_show = draw_structure_result(image, result,font_path=font_path)
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')
        
        # Extract the 'text' field from each item in the 'res' list
        texts = [item['text'] for item in result[0]['res']]
        doc = " ".join(item['text'] for item in result[0]['res'])
        # Convert each text into a vector
        
        #return result[0]
        return llm_differentiation(doc)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0", port=8081)