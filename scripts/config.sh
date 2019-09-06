#!/bin/sh
[[ -f "scripts/credentials.sh" ]] && source scripts/credentials.sh && echo "using credetianls"

experiment_name=full
number_of_repetitions=1
sleep_between_rounds=15m
providers=( aws )# gcf azure ibm )
configs=( "0,0,1" )# "0,0,2" "0,0,0.5" "60,60,1" "60,60,2" "60,60,0.5" )
target_urls=( https://692ha1ib93.execute-api.eu-west-2.amazonaws.com/dev/benchmark ) #https://europe-west2-reserach.cloudfunctions.net/http https://tub-elasticity-benchmark.azurewebsites.net/api/hello https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/be6628f82a926a56efa0f6953a1eaaba9a0fdb4de4df38794796ddd6936c3955/benchmark  ) #TODO!

echo "config [$experiment_name] provider[${providers[@]}] configs[${configs[@]}] reps[$number_of_repetitions] sleep[$sleep_between_rounds] urls[${target_urls[@]}]"