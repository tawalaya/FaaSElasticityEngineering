#! /bin/sh


function error_exit
{
   echo "Error: ${1:-"Unknown Error"}" 1>&2
   exit 1 # This unfortunately also exits the terminal
}

# will save mesurementes in results/experiment_name/config_name/run_number/provider.csv
. scripts/config.sh

cd workloadGenerator/server

#remove an generate new keys
rm .ssh/*
ssh-keygen -f .ssh/server -t rsa -C "werner@tu-berlin.de" -b 2048 -q -N ""
chmod 600 .ssh/server
chmod 644 .ssh/server.pub

#TODO: Auto Accept

terraform apply --var do_token=${do_token} -auto-approve 

instance_ip=${terraform output digitalocean_droplet.benchmarker.ip}

scp -i .ssh/server prepare.sh root@$instance_ip:/tmp/prepare.sh
ssh -i .ssh/server root@$instance_ip -c "sh /tmp/prepare.sh"

#TODO: copy over config.sh
scp -i .ssh/server ../../scripts/config.sh root@$instance_ip:/FaaSElasticityEngineering/scripts/config.sh
scp -i .ssh/server run.sh root@$instance_ip:/FaaSElasticityEngineering/scripts/run.sh
ssh -i .ssh/server root@$instance_ip -c "sh /FaaSElasticityEngineering/scripts/run.sh" 
#TODO: run ssh script in screen
scp -i .ssh/server root@$instance_ip:/FaaSElasticityEngineering/results ../../results/


terraform destory --var do_token=${do_token}

