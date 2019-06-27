from elasticsearch import Elasticsearch

def getOneImageData(imgId):
    """Function to retrieve one image's data from elasticseach."""

    host = 'http://10.0.0.13:9200'

    index = 'xray_chest'
    doc_type = 'staff_notes'

    es = Elasticsearch(host)
    file_id = '000' + str(imgId) + '.png'
   
    resp = es.get(index=index, doc_type=doc_type, id=file_id)

    return resp(['_source'])

