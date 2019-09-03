#!/bin/sh
experiment_name=test_m3
number_of_repetitions=5
sleep_between_rounds=30m
providers=( aws gcf azure ibm )
configs=( "0,0,1" "0,0,2" "0,0,0.5" "60,60,1" "60,60,2" "60,60,0.5" )
target_urls=(  ) #TODO!

echo "config [$experiment_name] provider[${providers[@]}] configs[${configs[@]}] reps[$number_of_repetitions] sleep[$sleep_between_rounds] urls[${target_urls[@]}]"