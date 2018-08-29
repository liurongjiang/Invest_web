#coding=utf-8
import re
from elasticsearch import Elasticsearch
from run import logger

es=Elasticsearch('http://192.168.1.180:9200/')

def search_by_elasticsearch(keyword, start, length):
    keyword=keyword.strip()
    index='invest'
    q0={ 
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
                "should": [{ 
                    "multi_match": { 
                        "query": "%s" % keyword,
                        "type": "phrase",
                        "fields": ["*name^2", "institution^2", "introduction^2"],
                        "slop" : 10
                      } 
                }] 
            } 
        }
    q1={ 
            "bool": { 
                "must": [ 
                    { "match": { 
                        "_all":{
                            "query": " %s " % keyword,
                            "minimum_should_match": "100%"
                        } 
                      } 
                    } 
                ], 
                "should": [{ 
                    "match_phrase": { 
                        "_all": { 
                            "query": "%s" % keyword, 
                            "slop" : 10
                        } 
                    } 
                }] 
            } 
        }
    q2={
        "multi_match": {
            "query": "%s" % keyword,
            "type": "phrase",
            "fields": ["*name", "institution", "introduction^2"],
            "slop" : 100
            #"tie_breaker":          0.3,
            #"minimum_should_match": "30%"
        }
    }
    q3={
        "dis_max": {
            "queries": [
                { "match_phrase": { "company_name": "%s" % keyword }},
                { "match_phrase": { "project_name": "%s" % keyword }},
                { "match_phrase": { "institution": "%s" % keyword }},
                { "match_phrase": { "introduction": "%s" % keyword }},
            ],
            "tie_breaker": 1,
        }
    }
    q4={
        "multi_match": {
            "query": "%s" % keyword,
            "type": "most_fields",
            "fields": ["*name", "institution", "introduction^2"],
            "operator": "and"
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
        "query": q0,
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
    if query_sql["from"] >= 5000:
        query_sql["from"]=5000
    response = es.search(body=query_sql, index=index)
    results=response['hits']['hits']
    total=response['hits']['total']
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
    
    if not docs: return resp
    
    resp['data']=docs
    resp['recordsTotal']=total
    resp['recordsLength']=total
    resp['recordsFiltered']=total
    return resp

