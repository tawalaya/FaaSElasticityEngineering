#!/bin/sh
[[ -f "scripts/credentials.sh" ]] && source scripts/credentials.sh && echo "using credetianls"

experiment_name=test_validation
number_of_repetitions=1
sleep_between_rounds=5m
providers=( aws  gcf azure ibm )
configs=( "60,60,1" )
target_urls=( http://localhost )

echo "config [$experiment_name] provider[${providers[@]}] configs[${configs[@]}] reps[$number_of_repetitions] sleep[$sleep_between_rounds] urls[${target_urls[@]}]"
