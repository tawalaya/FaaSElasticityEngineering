#! /usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import glob
sns.set()


#constants
experiment_phase = {'p0':60000, 'p1':60000, 'p2':180000}
experiment_phase_labels = [*experiment_phase]

def cleanBrokenLines(file,fileds=14,threshold=0.5):
    removed = 0
    lines = 0
    with open(file,"r") as s:
        with open(file+".tmp","w") as d:
            for line in s:
                lines+=1
                if line.count(",") >= fileds:
                    d.write(line)
                else:
                    removed+=1
        if (removed/lines) > threshold:
            print(file,"quality below threshold",removed,lines)
            raise ValueError
    
    return file+".tmp"
        
costs = {
    "aws":  {"EVar":16.67,"EFix":0.2},
    "gcf":  {"EVar":16.50,"EFix":0.4},
    "ibm":{"EVar":17.0,"EFix":0.0},
    "azure":  {"EVar":16.0,"EFix":0.2}
}
def load(experiment_name,providers,configs,num_repetitions=1,read_timeouts=True):
    knownIds = {}
    def isNewContainer(containerId):
        if containerId in knownIds:
            return "Reused"
        knownIds[containerId] = True
        return "New"

    
    all = None
    timeouts = None
    for config in configs:
        for provider in providers:
            for run_num in range(1, num_repetitions+1):
                startTime = None
                run = None
                #print("reading",config,provider,run_num)
                for file in glob.glob('results/'+experiment_name+'/'+config+'/'+str(run_num)+'/'+provider+'/result*.csv'):
                    clean_file = None
                    try:
                        if provider == "azure":
                            clean_file = cleanBrokenLines(file,4)
                        else:
                            clean_file = cleanBrokenLines(file)
                    except ValueError:
                        print("results broken for",provider,config,run,file)
                        continue
                    try:
                        df = pd.read_csv(clean_file, skiprows = 0,error_bad_lines=False)
                        #df.dropna(inplace=True,subset=['executionStartTime'])
                        
                        df['provider'] = provider
                        df['run'] = run_num
                        df['soruce'] = file
                        df['config'] = config
                        
                        if startTime is None:
                            startTime = df['requestTime'].min() 
                            if config[0] == "0":
                                startTime-=experiment_phase['p0']
                            
                        else:
                            if config[0] == "0":
                                startTime = min(startTime,df['requestTime'].min() - experiment_phase['p0'] )
                                
                            else:
                                startTime = min(startTime,df['requestTime'].min()  )
                        
                        df['m1'] = df['requestTime']
                        
                        faults = False
                        
                        if 'executionStartTime' in df.columns:
                            df['m2'] = df['executionStartTime']
                            faults = True
                        else:
                            df['m2'] = float('nan')
                        
                        if 'executionEndTime' in df.columns:
                            df['m3'] = df['executionEndTime']
                            faults = True
                        else:
                            df['m3'] = float('nan')
                        
                        if 'responseTime' in df.columns:
                            df['m4'] = df['responseTime']
                            faults = True
                        else:
                            df['m4'] = float('nan')
                        
                        df['deliveryLatency']= (df['m2']-df['m1']) / 1000
                        df['responseLatency']= (df['m4']-df['m3']) / 1000
                        df['requestResponseLatency'] = df['requestResponseLatency'] / 1000
                        


                        
                        if 'executionLatency' in df.columns:
                            df['executionLatency'] = df['executionLatency'] / 1000  
                            df['cost'] = costs[provider]['EVar']*df['executionLatency']+costs[provider]['EFix']
                            df['nonExecutionLatency'] = df['requestResponseLatency'] - df['executionLatency']
                        
                        if 'containerId' in df.columns:
                            df['newContainer'] = df['containerId'].apply(isNewContainer)
                        df['failed'] = df['statusCode'] > 200
                        df['success'] = df['statusCode'] == 200
                        if (run is None):
                            run = df
                        else:
                            run = pd.concat([run, df], sort=True)
                    except OSError as e:
                        print("Failed to read file for",provider,config,run)
                
                
                run['m1'] -= startTime
                run['m2'] -= startTime
                run['m3'] -= startTime
                run['m4'] -= startTime
                if 'containerStartTime' in df.columns:
                    run['containerStartTime'] -= startTime
                
                
                run['label'] = 'none'
                interval_start = 0
                for name in experiment_phase_labels:
                    interval_lenght = experiment_phase[name]
                    run.loc[run['m1'].between(interval_start,interval_start+interval_lenght),'label'] =name
                    interval_start += interval_lenght
         
                if (all is None):
                    all = run
                else:
                    all = pd.concat([all, run], sort=True)
                if read_timeouts:
                    for file in glob.glob('results/'+experiment_name+'/'+config+'/'+str(run_num)+'/'+provider+'/timeout*.csv'):
                        try:
        
                            df = pd.read_csv(file, skiprows = 0)
                            
                            df['provider'] = provider
                            df['run'] = run_num
                            df['soruce'] = file
                            df['config'] = config
                            
                            df['m1'] = df['requestTime']-startTime
                            df['responseTime'] = df['requestTime']+30000
                            df['m4'] = df['responseTime']-startTime

                            df['label'] = 'none'
                            interval_start = 0
                            for name in experiment_phase_labels:
                                interval_lenght = experiment_phase[name]
                                df.loc[df['m1'].between(interval_start,interval_start+interval_lenght),'label'] =name
                                interval_start += interval_lenght




                            df['failed'] = True
                            df['success'] = False
                            df['statusCode'] = 408



                            if (timeouts is None):
                                timeouts = df
                            else:
                                timeouts = pd.concat([timeouts, df], sort=True)
                        except OSError as e:
                            print("Failed to read file for",provider,config,run)
    result = None
    if read_timeouts:
        result = all.set_index('requestId').combine_first(timeouts.set_index('requestId'))
        result = result.reset_index() 
    else:
        result = all
    
    #remove faulty entries
    result = result[result['requestId'].apply(lambda x:len(str(x))) == 9]
    #remove unnasseary columns
    columns_to_keep = ['cost','requestId','config','containerId','containerStartTime','deliveryLatency','responseLatency','executionLatency','failed','success','label','m1','m2','m3','m4','newContainer','nodeVersion','nonExecutionLatency','osType','primeNumber','provider','result','run','soruce','statusCode','vmId','requestResponseLatency','newContainer']
    columns_filter = []
    for column in result.columns:
        if column in columns_to_keep:
            columns_filter.append(column)
    #cleaning schema
    result = result[columns_filter]
    result.rename(columns={
        'requestId':"RId",
        'config':"WL", 
        'containerId':"CId", 
        'containerStartTime':"CStart", 
        'deliveryLatency':"DLat",
        'responseLatency':"BLat",
        'executionLatency':"ELat", 
        'success':"RSuccessed", 
        'failed':"RFailed",
        'cost':"ECost",
        'label':"Phase",
        'm1':"RStart",
        'm2':"EStart",
        'm3':"EEnd",
        'm4':"REnd",
        'newContainer':"CFirstRun",
        'nodeVersion':"CPlat",
        'nonExecutionLatency':"TLat",
        'osType':"COs",
        'primeNumber':"RInput",
        'provider':"Provider",
        'requestResponseLatency':"RLat",
        'result':"RResult",
        'run':"run", 
        'soruce':"sourceFile",
        'statusCode':"RCode",
        'vmId':"HId",
        'newContainer':"CNew"
    }, inplace=True)
    return result