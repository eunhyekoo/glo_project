import json, os
from elasticsearch import Elasticsearch
import jwt
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from netflix_kpi import get_netflix_kpi,get_otd_rtm,get_epm_eps,get_failrate
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


def search(index,query,size):
  res = client.search(index=index,query=query,size =size)
  return res

def count(index,query):
  res = client.count(index=index,query=query)
  res = json.dumps(res,default= dict) # 인코딩
  res = json.loads(res) # 디코딩
  size = int(res['count'])
  return size

def elastic_query(index,startDate,endDate):
  QUERY = {
    "bool": {
      "must": {
        "range": {
          "submitdate": {
            "gte": startDate,
            "lt": endDate
          }
        }
      }
    }
  }
  #size = count(index,QUERY)
  res = search(index,QUERY,10000) # 7000
  res = json.dumps(res,default= dict) # 인코딩
  res = json.loads(res) # 디코딩
  netflix_data = res['hits']['hits']
  return netflix_data
  

def agg_epm_eps(email,startDate,endDate):
  index = 'netflix-dtt_locqc_result'
  size = 0
  query= {
    "bool":{
      "must":[
        {
          "range":{
            "submitdate":{
              "gte":startDate,
              "lt":endDate
            }
          }
        }
      ]
    }
  }
  aggs = {
    "group_by_state":{
      "terms":{
        "field": "author.keyword",
        "size":10000
      },
      "aggs":{
        "sum_runtime":{
          "sum":{
            "field": "runtimeminutes"
          }
        },
        "sum_error":{
          "sum":{
            "field": "allerrors"
          }
        },
        "sum_subtitle":{
          "sum":{
            "field": "subtitleevents"
          }
        },
        "sum_objective":{
          "sum":{
            "field": "objectiveerrors"
          }
        }
      }
    }
  }
  res = client.search(index=index,query=query,size =size,aggs = aggs)
  res = json.dumps(res,default= dict) # 인코딩
  res = json.loads(res) # 디코딩
  
  netflix_data = res["aggregations"]["group_by_state"]["buckets"]
  epm_avg,eps_avg,user_epm,user_eps = get_epm_eps(netflix_data,email)
  
  return epm_avg,eps_avg,user_epm,user_eps

def agg_failrate(email,startDate,endDate):
  index = 'netflix-dtt_asset_qc_result'
  size = 0
  query = {
    "bool":{
      "must":[
        {
          "match": {
            "isnetneutral": True
          }
        },
        {
          "range":{
            "submitdate":{
              "gte":startDate,
              "lt": endDate
            }
          }
        }
      ]
    }
  }
  aggs = {
    "group_by_state":{
      "terms":{
        "field": "author.keyword",
        "size":10000
      },
      "aggs":{
        "sum_isfail":{
          "sum":{
            "field": "isfail"
          }
        }
      }
    }
  }
  res = client.search(index = index,query = query,size = size,aggs = aggs)
  res = json.dumps(res,default= dict) # 인코딩
  res = json.loads(res) # 디코딩
  netflix_data = res["aggregations"]["group_by_state"]["buckets"]
  failrate_avg, failrate = get_failrate(netflix_data,email)
  
  return failrate_avg,failrate

    
def lambda_handler(event, context):
  response = ''
  body=""
  otd_avg,otd,rtm_avg,rtm = 0,0,0,0
  res = ""
  user_epm,user_eps = 0,0
  failerate_avg,epm,eps,epm_avg,eps_avg,failrate = 0,0,0,0,0,0
  otd_goal = 95
  epm_goal = 0.700
  eps_goal = 0.050
  rtm_goal= 0
  failrate_goal = 2.00
  status_code = 200
  email = ""
  try:
    userJWT = event['headers']['auth'].split(' ')[1]
    #email = jwt.decode(userJWT, options={"verify_signature": False})['user']['email']
    servermode = event['headers']['mode'] 
    servertype = SERVER[servermode]
    url = servertype + '/api/pichu/auth'
    headers = {'Authorization': 'Bearer '+userJWT }
    response_api = requests.get(url, headers=headers)
    if response_api.status_code == 401:
      #토큰 유효하지 않을 경우
      status_code = 401
    else:
      email = response_api.json()['originatorEmail']
      # originatorEmail 정보가 없는 경우.
      if email == None:
        status_code = 500
      
    startDate = event['queryStringParameters']['startDate']
    endDate = event['queryStringParameters']['endDate']
    period = event['queryStringParameters']['period'] 
    startDate = datetime.strptime(startDate,'%Y-%m-%d')

    if period == 'daily': 
      # Daily인 경우에는 startdate, enddate 동일하게 들어오기 때문에 한달 더해주기
      endDate = startDate+relativedelta(months = 1)
      endDate = str(endDate).split(' ')[0]
      rtm_goal = 15
    elif period == 'weekly':
      rtm_goal = 63
    elif period == 'monthly':
      rtm_goal = 250
      
    startDate = str(startDate).split(' ')[0]
    origin_summary = elastic_query("netflix-dtt_origination_summary",startDate,endDate)
    locqc_summary = elastic_query("netflix-dtt_locqc_summary",startDate,endDate)
    origin_author, origin_otd_rtm =  get_netflix_kpi(origin_summary,email,'author',1)
    locqc_author, locqc_otd_rtm = get_netflix_kpi(locqc_summary,email,'locqcer',1)
    
    all_author =list(set(origin_author + locqc_author))
    otd_avg,rtm_avg,otd,rtm = get_otd_rtm(all_author,origin_otd_rtm,locqc_otd_rtm,email)
    failerate_avg,failrate = agg_failrate(email,startDate,endDate)
    epm_avg,eps_avg,epm,eps = agg_epm_eps(email,startDate,endDate)
    
    #locqc_result = elastic_query("netflix-dtt_locqc_result",startDate,endDate)
    #asset_qc = elastic_query("netflix-dtt_asset_qc_result",startDate,endDate)
    #epm_avg,eps_avg,epm,eps= get_netflix_kpi(locqc_result,email,'author',2)
    #failerate_avg,failrate= get_netflix_kpi(asset_qc,email,'author',3)

    response = {
      'startDate':startDate,
      'endDate':endDate,
      'logicstatusCode':status_code,
      'avg':{'otd':otd_avg,'rtm':rtm_avg,'failerate':failerate_avg,'epm':epm_avg,'eps':eps_avg},
      'otd':otd,
      'rtm':rtm,
      'epm':epm,
      'eps':eps,
      'failerate':failrate,
      'otd_goal':otd_goal,
      'epm_goal':epm_goal,
      'eps_goal':eps_goal,
      'rtm_goal':rtm_goal,
      'failrate_goal':failrate_goal
    }

    body = json.dumps(response)
    
  except Exception as e:
    body += str(e)
    
  response = {
    'statusCode': 200,
    'headers': {
        "Content-Type": "application/json"},
    'body' : body
  }
  
  return response
  
 