from flask import Flask, render_template, request, send_file
from elasticsearch import Elasticsearch
import boto3
from app import app

@app.route('/')
def index():
    return render_template('index.html', title='Home')

""" @app.route("/splash.png")
def load_image():
    return send_file('splash.png') """


@app.route('/one_image/<imgId>')
def getOneImageData(imgId):
    """Function to retrieve one image's data from elasticseach."""

    if len(imgId) != 9:
        resp1 = {imgId: "Format error! Please use format '00000_000' "}
    else:
        host = 'http://10.0.0.13:9200'
        index = 'xray_chest'
        doc_type = 'staff_notes'
        es = Elasticsearch(host)
        file_id = '000' + str(imgId) + '.png'

        s3_loc = 'https://chest-xray-source-images.s3-us-west-2.amazonaws.com/image_store/' + file_id

        try:
            resp = es.get(index=index, doc_type=doc_type, id=file_id)
            resp1 = resp['_source']
            resp1.update({'Image_View': s3_loc})
        except :
            resp1 = {imgId: "Requested Image Not Found."}

    return render_template('one_image.html',  result = resp1)


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0")
