#!/bin/sh
[[ -f "scripts/credentials.sh" ]] && source scripts/credentials.sh && echo "using credetianls"
host=basti@kbl
experiment_name=low
number_of_repetitions=1
sleep_between_rounds=5m
providers=( azure ) # gcf azure ibm )
configs=( "5,5,0" "15,15,0" "0,0,1" "60,60,0" ) #"0,0,2" "60,60,2"
target_urls=( https://sls-uks-dev-tub-elasticity-benchmark.azurewebsites.net/api/hello ) #https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/51ba75c787dfa78656ccf74881c03cd2762d1060f6c4cd36bd0ce83fdeeab5c0/benchmark ) #http://sls-uks-dev-tub-elasticity-benchmark.azurewebsites.net/api/hello ) 
#https://europe-west2-benchimarki.cloudfunctions.net/test-service-dev-hello ) #https://t2s3ot65m9.execute-api.eu-west-2.amazonaws.com/dev/benchmark ) #https://europe-west2-reserach.cloudfunctions.net/http https://tub-elasticity-benchmark.azurewebsites.net/api/hello https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/be6628f82a926a56efa0f6953a1eaaba9a0fdb4de4df38794796ddd6936c3955/benchmark  ) #TODO!

echo "config [$experiment_name] provider[${providers[@]}] configs[${configs[@]}] reps[$number_of_repetitions] sleep[$sleep_between_rounds] urls[${target_urls[@]}]"
