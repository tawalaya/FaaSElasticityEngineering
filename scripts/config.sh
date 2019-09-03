#!/bin/sh
[[ -f "scripts/credentials.sh" ]] && source scripts/credentials.sh && echo "using credetianls"

experiment_name=test
number_of_repetitions=1
sleep_between_rounds=5m
providers=( aws gcf azure ibm )
configs=( "0,0,1" )
target_urls=( https://ab1p6nhnma.execute-api.eu-west-2.amazonaws.com/dev/benchmark https://europe-west2-reserach.cloudfunctions.net/http https://tub-elasticity-benchmark.azurewebsites.net/api/hello https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/be6628f82a926a56efa0f6953a1eaaba9a0fdb4de4df38794796ddd6936c3955/benchmark )
 #TODO!

echo "config [$experiment_name] provider[${providers[@]}] configs[${configs[@]}] reps[$number_of_repetitions] sleep[$sleep_between_rounds] urls[${target_urls[@]}]"