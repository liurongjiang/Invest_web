#coding=utf-8
import re
from elasticsearch import Elasticsearch
from event import logger

es=Elasticsearch('http://192.168.1.180:9200/')

def search_by_elasticsearch(keyword, start, length, doc_type):
    keyword=keyword.strip()
    index='invest'
    query={ 
            "bool": { 
                "must": [ 
                    { "multi_match": { 
                        "query": "%s" % keyword,
                        "type": "most_fields",
                        "fields": ["*name", "institution", "introduction"],
                        "operator": "and",
                        #"minimum_should_match": "100%"
                      } 
                    } 
                ], 
                "should": [
                    { 
                        "multi_match": { 
                            "query": "%s" % keyword,
                            "type": "phrase",
                            "fields": ["*name^2", "institution^2", "introduction^2"],
                            "slop" : 10
                        }
                    }
                ] 
            } 
        }
    sort=[
        {
            "_score": {"order": "desc"}
        }
    ]
    query_sql={
        "from" : start if isinstance(start, int) else int(start), 
        "size" : length if isinstance(length, int) else int(length),
        "query": query,
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
    #if query_sql["from"] >= 5000:
    #    query_sql["from"]=5000
    response = es.search(body=query_sql, index=index, doc_type=doc_type)
    results=response['hits']['hits']
    total=response['hits']['total']
    if total > 5000:
        total=5000
    resp={}
    docs=[]
    
    logger.debug('__es_query_sql: %s' % query_sql)
    for result in results:
        doc={}
        doc=result['_source']
        highlight=result['highlight']
        for key in highlight:
            doc[key]=re.sub('</em><em>', '', ''.join(highlight[key]) )
        docs.append(doc)
    
    resp['data']=docs
    resp['recordsTotal']=total
    resp['recordsLength']=total
    resp['recordsFiltered']=total
    return resp

