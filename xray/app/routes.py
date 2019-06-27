from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from app import app

@app.route('/')
@app.route('/index')
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
   
    resp = es.get(index=index, doc_type=doc_type, id=file_id)

    return render_template('one_image.html', result = resp(['_source']))


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)