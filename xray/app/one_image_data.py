from elasticsearch import Elasticsearch
import sys


def getOneImageData(imgId):
    """Function to retrieve one image's data from elasticseach."""

    print(imgId)

    host = 'http://10.0.0.13:9200'

    index = 'xray_chest'
    doc_type = 'staff_notes'

    es = Elasticsearch(host)
    file_id = str(imgId) + '.png'
   
    resp = es.get(index=index, doc_type=doc_type, id=file_id)

    return resp(['_source'])

