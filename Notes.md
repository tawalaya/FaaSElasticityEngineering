### Setup - Ubuntu
 1. `curl -o- -L https://slss.io/install | bash`
 2. `apt install python3 npm screen`
 3. `npm install -g artillery`
### Installation

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

#### IBM
 1. `curl -fsSL https://clis.ng.bluemix.net/install/linux | sh`
 2. `bmcloud login -a <REGION_API> -o <INSERT_USER_ORGANISATION> -s`
### Preperations
 1. for each provider go to `./deploymentPackage/<provider>`
 2. sls deploy

### Experimen Run

### Reproduction Log
 - set up a digital ocian vm in FRA
 - clone repo onto maschine
 - setup accounts (document was suboptimal)
 - needed to change script to python3
 - CPU limit on client-side => reduces quality