function error_exit
{
   echo "Error: ${1:-"Unknown Error"}" 1>&2
   exit 1 # This unfortunately also exits the terminal
}

# will save mesurementes in results/experiment_name/config_name/run_number/provider.csv
. scripts/config.sh

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
            mkdir -p results/$experiment_name/$config/$run/$provider
            cd results/$experiment_name/$config/$run/$provider
            artillery run ../../../../../workloadGenerator/benchmarker/test.yml -o "$provider.json" || error_exit "could not benchmark $provider"
            #mv result* "$provider.csv"
            #mv timeout* "$provider-timeout.csv"
            cd ../../../../..
        done
        echo "sleeping for $sleep_between_rounds"
        sleep $sleep_between_rounds
    done
    echo "done with $config waiting 2m"
    sleep 2m
done
