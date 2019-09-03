function error_exit
{
   echo "Error: ${1:-"Unknown Error"}" 1>&2
   exit 1 # This unfortunately also exits the terminal
}

. scripts/config.sh
echo "deploying providers!"
for provider in "${providers[@]}"
do
   : 
   echo "deploying $provider"
   cd deploymentPackage/$provider
   sls deploy || error_exit "could not deploy $provider"
   cd ../..
done

result="("
for provider in "${providers[@]}"
do
   : 
   cd deploymentPackage/$provider
   target_url=$(sls info | egrep -o 'https?://[^ ]+' | head -1)
   if [ "$provider" = "azure" ]; then
      #TODO: fix this!
      target_url=https://elasticity-benchmark.azurewebsites.net/api/hello
   fi
   result="$result $target_url"
   cd ../..
done
echo "$result )"