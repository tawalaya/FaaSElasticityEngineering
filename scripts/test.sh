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
   echo "testing $provider"
   cd deploymentPackage/$provider
   sls invoke local -f hello || error_exit "could not test $provider"
   cd ../..
done
