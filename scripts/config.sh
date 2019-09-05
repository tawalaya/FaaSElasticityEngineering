#!/bin/sh
[[ -f "scripts/credentials.sh" ]] && source scripts/credentials.sh && echo "using credetianls"

experiment_name=test_180_azure_2
number_of_repetitions=1
sleep_between_rounds=5m
providers=( azure )
configs=( "0,0,1" )
target_urls=( https://tub-elasticity-benchmark.azurewebsites.net/api/hello )

echo "config [$experiment_name] provider[${providers[@]}] configs[${configs[@]}] reps[$number_of_repetitions] sleep[$sleep_between_rounds] urls[${target_urls[@]}]"