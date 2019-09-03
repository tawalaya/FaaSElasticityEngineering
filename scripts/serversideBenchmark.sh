function error_exit
{
   echo "Error: ${1:-"Unknown Error"}" 1>&2
   exit 1 # This unfortunately also exits the terminal
}

# will save mesurementes in results/experiment_name/config_name/run_number/provider.csv
experiment_name=test_m3
number_of_repetitions=5
sleep_between_rounds=30m
providers=( aws gcf azure ibm )
configs=( "0,0,1" "0,0,2" "0,0,0.5" "60,60,1" "60,60,2" "60,60,0.5" )
target_urls=(  ) #TODO!

echo "starting benchmarks!"
for config in "${configs[@]}"
do
    :
    python workloadGenerator/generate_config.py $config > workloadGenerator/benchmarker/test.yml 
    echo "generated new bench for $config"
     
    for run in `seq 1 $number_of_repetitions`;
    do
        :
        echo "starting run $run"
        i=0
        for provider in "${providers[@]}"
        do
            : 
            echo "benchmarking $provider"
            export target_url=${target_urls[$i]}
            i=$i+1
                
            echo "url of service: $target_url"
            mkdir -p results/$experiment_name/$config/$run
            cd results/$experiment_name/$config/$run
            #artillery run ../../../benchmarker/test.yml || error_exit "could not benchmark $provider"
            mv result* "$provider.csv"
            cd ../../../..
        done
        echo "sleeping for $sleep_between_rounds"
        sleep $sleep_between_rounds
    done
    echo "done with $config waiting 2m"
    sleep 2m
done