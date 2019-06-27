from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import boto3
from app import app

@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/one_image/<imgId>')
def getOneImageData(imgId):
    """Function to retrieve one image's data from elasticseach."""

    host = 'http://10.0.0.13:9200'
    index = 'xray_chest'
    doc_type = 'staff_notes'
    es = Elasticsearch(host)
    file_id = '000' + str(imgId) + '.png'

    s3_loc = 's3://chest-xray-source-images/image_store/' + file_id
   
    resp = es.get(index=index, doc_type=doc_type, id=file_id)
    resp1 = resp['_source']
    resp1.update({'Image_Location': s3_loc})

    print(resp1)

    return render_template('one_image.html',  result = resp1)


if __name__ == '__main__':
    app.run('54.245.40.185', 5000, debug=True)