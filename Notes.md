### Setup - Ubuntu
 1. `curl -o- -L https://slss.io/install | bash`
 2. `apt install python3 npm screen`
 3. `npm install -g artillery`
### Installation
 1. in `workloadGenerator/benchmarker` npm install
 2. 
### Account Setup

#### AWS
 1. `serverless config credentials --provider aws --key ... --secret ..`

#### Azure
 1. `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`
 2. `apt update`
 3. `apt-get install ca-certificates curl apt-transport-https lsb-release gnupg`
 4. `curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null`
 5. `AZ_REPO=$(lsb_release -cs)`
 6. `echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" |  sudo tee /etc/apt/sources.list.d/azure-cli.list`
 7. `sudo apt-get update`
 8. `sudo apt-get install azure-cli`
 9. `az login`
 10. `az ad sp create-for-rbac`
 11. `edit the scripts/credentials.sh`

#### GCF
 1. follow the instructions at `https://www.serverless.com/framework/docs/providers/google/guide/credentials/`
 2. edit `~/.gcloud/keyfile.json`
 3. edit the serverless.yml file in `./deploymentPackage/gcf` with your projectid.

#### IBM
 1. `curl -fsSL https://clis.ng.bluemix.net/install/linux | sh`
 2. `bmcloud login -a <REGION_API> -o <INSERT_USER_ORGANISATION> -s`
### Preperations
 0. in `./deploymentPackage` run copyLogic.sh
 1. for each provider go to `./deploymentPackage/<provider>`
 2. npm install (if a package.json is present)
 3. sls deploy
 4. note down the function url
 5. create config.sh using the template, host must be an ssh-able address

### Performing the Experiment
 1. use deploy_server.sh to copy the experiment to a linux server
 2. on the server us ./scripts/servisideBenchmark.sh to perform the benchmarks
 3. after all is done use copy_data.sh to collect all results

### Experimen Log
- AWS, 7.7.2020 11:08, "0,0,1" "0,0,0.5" "60,60,1"  "60,60,0.5"  "60,60,0" 
- GCF, 7.7.2020 14:00, "0,0,1" "0,0,0.5" "60,60,1"  "60,60,0.5"  "60,60,0" 
- GCF, 7.7.2020 20:00, "0,0,1" "0,0,0.5" "60,60,1"  "60,60,0.5"  "60,60,0" 
- MAF, 8.7.2020 09:15, "0,0,1" "0,0,0.5" "60,60,1"  "60,60,0.5"  "60,60,0" 
- IBM, 13.7.2020 11:00,"0,0,1" "0,0,0.5" "60,60,1"  "60,60,0.5"  "60,60,0" 
### Reproduction Log
 - get a mashine with sufficent single core
 - setup your config.sh
 - setup accounts (document was suboptimal)
 - needed to change script to python3
 - CPU limit on client-side => reduces quality; use mashine with sufficent single core perf.
 - increase ulimt on system to 64k
 - atillery is not ideal for this experiment. We should consider a better work load generator.
 - For GCF you need to enable public access to the function unsing the Cloud Console [https://cloud.google.com/run/docs/authenticating/public](https://cloud.google.com/run/docs/authenticating/public)