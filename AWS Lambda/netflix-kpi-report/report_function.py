import json, os
from elasticsearch import Elasticsearch
import jwt
from report_function import get_locqc_result,get_asset_result,get_abandonded_data
import requests

ID = os.environ.get('ES_ID')
PW = os.environ.get('ES_PW')
URL = os.environ.get('ES_URL')

SERVER = {'dev' : 'https://dev.gloground.com',
          'test' : 'https://gloground.com',
          'live' : 'https://platform.glozinc.com'}

client = Elasticsearch(
  URL,
  basic_auth=(ID,PW)
)

report_data = {1:'netflix-dtt_netflix_locqc_view', 2 : 'netflix-dtt_all_assetqc_view'}
def count(index,query):
  res = client.count(index=index,query=query)
  res = json.dumps(res,default= dict) # 인코딩
  res = json.loads(res) # 디코딩
  size = int(res['count'])
  return size

def search(index,query,size):
  res = client.search(index=index,query=query,size =size)
  return res
  
def get_kpi_data(email,idx,startdate,enddate):
  QUERY ={
    "bool":{
      "must":[
        {
          "match_phrase": {
            "author": email
          }
        },
        {
          "range":{
            "submitdate":{
              "gte":startdate,
              "lt":enddate
            }
          }
        }
      ]
    }
}
  #size = count(report_data[idx],QUERY)
  res = search(report_data[idx],QUERY,size = 10000)
  #res = client.search(index=report_data[idx],query=QUERY,size = 1000)
  res = json.dumps(res,default=dict)
  res = json.loads(res) # 디코딩
  data = res['hits']['hits']
  '''
  2022.07.27 수정내용
  origination 삭제, locqc, assetqc만 사용 / duedate 삭제
  '''
  if idx == 1:
    netflix_report = get_locqc_result(data)
  elif idx == 2:
    netflix_report = get_asset_result(data)

    
  return netflix_report
  
def get_abandon_data(email,startdate,enddate):
  INDEX = 'netflix-dtt_abandonment'
  QUERY ={
    "bool":{
      "must":[
        {
          "match_phrase": {
            "author": email
          }
        },
        {
          "range":{
            "abandonmentdate":{
              "gte":startdate,
              "lt":enddate
            }
          }
        }
      ]
    }
}

  res = client.search(index=INDEX,query=QUERY)
  res = json.dumps(res,default=dict)
  res = json.loads(res) # 디코딩
  data = res['hits']['hits']
  
  # Abandon데이터 없을 경우 공백
  try:
    abandon = get_abandonded_data(data)
  except Exception as e:
    abandon = ''

  return abandon
  
def lambda_handler(event, context):
  # TODO implement
  body = ""
  origin_summary = ""
  locqc_result = ""
  asset_result = ""
  locqc_resulttest = ""
  abandon_data = ""
  status_code = 200
  email =""
  serverType = ""
  try:
    userJWT = event['headers']['auth'].split(' ')[1]
    servermode = event['headers']['mode'] 
    servertype = SERVER[servermode]
    url = servertype + '/api/pichu/auth'
    #url = 'https://dev.gloground.com/api/pichu/auth'
    headers = {'Authorization': 'Bearer '+userJWT }
    
    response_api = requests.get(url, headers=headers)
    if response_api.status_code == 401:
      #토큰 유효하지 않을 경우.
      status_code = 401
    else:
      email = response_api.json()['originatorEmail']
      # originatorEmail 정보가 없는 경우.
      if email == None:
        status_code = 500
      
    #email = jwt.decode(userJWT, options={"verify_signature": False})['user']['email']
    startDate = event['queryStringParameters']['startDate']
    endDate = event['queryStringParameters']['endDate']

    
    #origin_summary = get_kpi_data(email,1,startDate,endDate)
    locqc_result = get_kpi_data(email,1,startDate,endDate)
    asset_result = get_kpi_data(email,2,startDate,endDate)
    #locqc_resulttest = get_kpi_data(email,3,startDate,endDate)
    #asset_resulttest = get_kpi_data(email,4,startDate,endDate)
    #locqc_resulttest = get_kpi_data(email,4,startDate,endDate)
    
    all_report_data = []
    all_report_data.append(locqc_result)
    all_report_data.append(asset_result)

    
    abandon_data = get_abandon_data(email,startDate,endDate)
    body = json.dumps({'logicstatusCode':status_code,'startdate':startDate,'Submmited':all_report_data,'Abandoned':abandon_data})
  except Exception as e:
    print("에러발생")
    body += str(e)
  return {
    'statusCode': 200,
    'headers': {
            "Content-Type": "application/json"
        },
    'body':body
  #  'test':all_report_data_test

    
  }
