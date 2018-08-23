#coding=utf-8
import re
from elasticsearch import Elasticsearch

es=Elasticsearch('http://192.168.1.180:9200/')

def search_by_elasticsearch(keyword, start, length):
    index='invest'
    query_sql={
        "from" : start if isinstance(start, int) else int(start), 
        "size" : length if isinstance(length, int) else int(length),
        "query": {
            "multi_match": {
                "query": "%s" % keyword,
                "type": "most_fields",
                "fields": ["*name", "institution", "introduction"]
            }
        },
        "highlight": {
            "fields": {
                "project_name": {},
                "company_name": {},
                "institution": {},
                "introduction": {},
                "cleaned_company_name": {}
            }
        }
    }
    response = es.search(body=query_sql, index=index)
    results=response['hits']['hits']
    total=response['hits']['total']
    resp={}
    docs=[]
    for result in results:
        doc={}
        doc=result['_source']
        highlight=result['highlight']
        for key in highlight:
            doc[key]=re.sub('</em><em>', '', ''.join(highlight[key]) )
        docs.append(doc)
    if not docs: return None

    resp['data']=docs
    resp['recordsTotal']=total
    resp['recordsLength']=total
    resp['recordsFiltered']=total
    return resp

