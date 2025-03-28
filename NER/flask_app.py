from flask import Flask, render_template, request
import pandas as pd
import zipfile
from gradio_app import process_zip_file, category_populate
from io import BytesIO

gradio_app = Flask(__name__)

@gradio_app.route('/')
def index():
    return '''
    <h1>Upload a Zip File</h1>
    <form method="POST" enctype="multipart/form-data" action="/upload">
        <input type="file" name="zipfile">
        <input type="submit" value="Upload">
    </form>
    '''

@gradio_app.route('/upload', methods=['POST'])
def upload():
    if 'zipfile' not in request.files:
        return "No file part"
    
    file = request.files['zipfile']

    if file.filename == '':
        return "No selected file"
    
    if file and file.filename.endswith(('.zip', '.txt')):
        # ip_object = process_zip_file(file)
        # I am calling process_zip file inside my category_populate function
        op_dataframe = category_populate(file)
        # Render the DataFrame as an HTML table
        return render_template('table.html', table=op_dataframe.to_html())

    return "Invalid file format. Please upload a .zip file."

if __name__ == '__main__':
    gradio_app.run(debug=True)
