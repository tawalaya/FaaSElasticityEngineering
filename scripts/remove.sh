function error_exit
{
   echo "Error: ${1:-"Unknown Error"}" 1>&2
   exit 1 # This unfortunately also exits the terminal
}

. scripts/config.sh
echo "removing providers!"
for provider in "${providers[@]}"
do
   : 
   echo "removing $provider"
   cd deploymentPackage/$provider
   sls remove || error_exit "could not deploy $provider"
   cd ../..
done
