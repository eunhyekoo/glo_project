def get_netflix_kpi(data,user,col,idx):
    netflix_list = []
    author = []
    netflix_kpi_data = []
    epm_avg = 0
    eps_avg = 0
    epm_sum = 0
    eps_sum = 0
    epm = 0
    eps = 0
    # 작업자 계정 중복되지 않게 담기.
    for i in data:
        netflix_list.append(i['_source'])
        for j in i['_source']:
            if j == col:
                if i['_source'][col] not in author:
                    author.append(i['_source'][j])

    for i in author:
        prj_cnt = 0
        ontime_cnt = 0
        runtime_min = 0
        for j in range(0,len(data)):
            if netflix_list[j][col] ==i:
                prj_cnt += 1 #전체 작업 개수
                runtime_min += netflix_list[j]['runtimeminutes']
                if netflix_list[j]['isontime']== True:
                    ontime_cnt += 1 # isontime = True 개수
        netflix_kpi_data.append([i,ontime_cnt,prj_cnt,runtime_min])
    #print('전체 개수:',netflix_kpi_data)
    return author,netflix_kpi_data



def get_otd_rtm(all_author,origin_otd_rtm,locqc_otd_rtm,user):
    otd_rtm_data = []
    otd_avg = 0
    rtm_avg = 0
    otd_sum = 0
    rtm_sum = 0
    rtm = 0
    otd = 0
    for i in all_author:
        origin_ontime,origin_prj,origin_rutime= 0,0,0
        locqc_ontime,locqc_prj,locqc_runtime = 0,0,0
        for j in origin_otd_rtm:
            if i == j[0]:
                origin_ontime = j[1] # ontime
                origin_prj = j[2] # prj
                origin_rutime = j[3]
                   
        for z in locqc_otd_rtm:
            if i == z[0]:
                locqc_ontime = z[1]
                locqc_prj = z[2]
                locqc_runtime = z[3]
    
        ontime = origin_ontime+locqc_ontime
        all_prj = origin_prj+locqc_prj
        all_runtime = origin_rutime+locqc_runtime
        try:
            otd_rtm_data.append([i,(ontime/all_prj)*100,all_runtime])
        except ZeroDivisionError as e:
            otd_rtm_data.append([i,0,all_runtime])
        
    # OTD 전체 평균, 유저 OTD 구하기
    for i in range(0,len(otd_rtm_data)):
        if otd_rtm_data[i][0] == user:          
            otd = round(otd_rtm_data[i][1],2) # otd
            rtm = round(otd_rtm_data[i][2],2) # rtm
        otd_sum += otd_rtm_data[i][1]       
        rtm_sum += otd_rtm_data[i][2]
    otd_avg = round(otd_sum/len(otd_rtm_data),2)
    rtm_avg = round(rtm_sum/len(otd_rtm_data),2)
    return otd_avg,rtm_avg,otd,rtm
    
def get_epm_eps(data,email):
    epm_sum = 0
    eps_sum = 0
    user_epm = 0
    user_eps = 0
    epm_avg = 0
    eps_avg = 0
    for i in data:
        user = i["key"]
        subtitleevent = i["sum_subtitle"]["value"]
        objerror = i["sum_objective"]["value"]
        runtime = i["sum_runtime"]["value"]
        error = i["sum_error"]["value"]
        
        try:
          epm = error/runtime
        except ZeroDivisionError as e:
          epm = 0
        eps = objerror/ subtitleevent
        if user == email:
          user_epm = round(epm,3)
          user_eps = round(eps,3)
        epm_sum += epm
        eps_sum += eps
        
    epm_avg = round(epm_sum/len(data),3)
    eps_avg = round(eps_sum/len(data),3)
    
    return epm_avg,eps_avg,user_epm,user_eps
    

def get_failrate(data,email):
    failrate_sum = 0
    user_failrate = 0
    for i in data:
        user = i["key"]
        prj_cnt = i["doc_count"]
        isfail = i["sum_isfail"]["value"]
        
        failrate = (isfail/prj_cnt)*100
        if user == email:
            user_failrate = failrate
        failrate_sum += failrate
    
    failrate_avg =round(failrate_sum/ len(data),2)
    return failrate_avg,user_failrate
     