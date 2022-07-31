import json, os
from elasticsearch import Elasticsearch
import jwt
from datetime import datetime, timedelta

# 제이 공유 참고 코 드 
ID = os.environ.get('ES_ID')
PW = os.environ.get('ES_PW')
URL = os.environ.get('ES_URL')

client = Elasticsearch(
  URL,
  basic_auth=(ID,PW)
)
ytd_index = {
    1:'netflix-dtt_asset_qc_ranking',
    2:'netflix-dtt_locqc_ranking'
}

# 가장 최근 ytd 데이터의 startdate, enddate가져오기
def get_kpi_date():
  INDEX = "netflix-dtt_asset_qc_ranking"
  AGG = {
    "properties": {
        "max": {
          "field": "startdate"
        }
      }
  }
  res = client.search(index=INDEX,size = 0,aggs = AGG)
  res = json.dumps(res,default= dict) # 인코딩
  res = json.loads(res) # 디코딩
  
  asset_ranking = res['aggregations']['properties']['value_as_string']
  asset_ranking = asset_ranking.split('T')[0]
  
  startdate=datetime.strptime(asset_ranking,'%Y-%m-%d')
  enddate = startdate+timedelta(days=6)
  return str(startdate.date()), str(enddate.date())


def get_kpi_ytd(startdate,enddate,index):
  QUERY ={
    "bool": {
      "must": {
        "range": {
          "startdate": {
            "gte": startdate,
            "lte": enddate
          
          }
        }
        
      }
    }
  }
  res = client.search(index = ytd_index[index],query = QUERY,size = 100)
  res = json.dumps(res,default=dict)
  res = json.loads(res) # 디코딩
  
  ytd_query = res['hits']['hits']
  ytd_data = get_ytd_data(ytd_query,index)

  return ytd_data

#locqc 에는 orgination request ids , qc request ids
#asset에는 origination request ids, eps, epsDiff


def get_ytd_data(ytd_query,idx):
  updated = False
  ytd_data = []
  test = 100
  if idx == 1: # asset
    for i in ytd_query:
        target_language_code = i['_source']['targetlanguagecode']
        ranknumerator = i['_source']['ranknumerator']
        rankdenominator = i['_source']['rankdenominator']
        lastranknumerator = i['_source']['lastranknumerator']
        lastrankdenominator = i['_source']['lastrankdenominator']
        lastfailerate = i['_source']['lastfailrate']
        failrate = i['_source']['failrate']
        originationrequestids = i['_source']['originationrequestids']
        qcrequestids = i['_source']['qcrequestids']
        
        if ranknumerator == None or lastranknumerator == None:
          ranknumeratorDiff = None
        else: 
          ranknumeratorDiff = lastranknumerator - ranknumerator 
          
        if failrate == None or lastfailerate == None :
          failRateDiff = None
        else: 
          failRateDiff = lastfailerate - failrate
          
      
        
        if rankdenominator != lastrankdenominator:
            updated = True
            
        ytd_data.append({'target_code':target_language_code,'ranknumerator':ranknumerator,'rankdenominator':rankdenominator,'failrate':failrate,'failRateDiff':round(failRateDiff,2),'ranknumeratorDiff':ranknumeratorDiff,'updated':updated,'originationrequestids':originationrequestids,'qcrequestids':qcrequestids})
  else: #locqc
      for i in ytd_query:
        target_language_code = i['_source']['targetlanguagecode']
        ranknumerator = i['_source']['ranknumerator']
        rankdenominator = i['_source']['rankdenominator']
        lastranknumerator = i['_source']['lastranknumerator']
        lastrankdenominator = i['_source']['lastrankdenominator']
        originationrequestids = i['_source']['originationrequestids']
        epe = i['_source']['errorsperevent']
        lastepe = i['_source']['lasterrorsperevent']
        
        if epe == None or lastepe == None:
           epeDiff = None
        else:
          epeDiff = round(lastepe - epe,3)
          
        if ranknumerator == None or lastranknumerator == None:
          ranknumeratorDiff = None
        else:
           ranknumeratorDiff = lastranknumerator - ranknumerator 

        if rankdenominator != lastrankdenominator:
            updated = True
        
        ytd_data.append({'target_code':target_language_code,'ranknumerator':ranknumerator,'rankdenominator':rankdenominator,'ranknumeratorDiff':ranknumeratorDiff,'updated':updated,'originationrequestids':originationrequestids,'epe':epe,'epeDiff':epeDiff})
        #ytd_data.append({'target_code':target_language_code,'ranknumerator':ranknumerator,'rankdenominator':rankdenominator,'ranknumeratorDiff':ranknumeratorDiff,'updated':updated})
  return ytd_data

    
def lambda_handler(event, context):
  # TODO implement
  body = ""
  asset_ytd = ""
  locqc_ytd = ""
  try:
    startdate, enddate = get_kpi_date()
    asset_ytd = get_kpi_ytd(startdate,enddate,1)
    locqc_ytd = get_kpi_ytd(startdate,enddate,2)
    body = json.dumps({'logicstatusCode':200,'enddate':enddate,'asset_ytd':asset_ytd,'locqc_ytd':locqc_ytd})
  except Exception as e:
    print("에러발생")
    body += str(e)

 
  response = {
    'statusCode': 200,
    'headers': {
            "Content-Type": "application/json"},
    'body' : body
  }
  
  
  return response
