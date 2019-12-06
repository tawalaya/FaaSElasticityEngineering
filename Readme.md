[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tawalaya/FaaSElasticityEngineering/master?filepath=SW-Analysis.ipynb)
# Prerequisits
- jupyter
- pandas
- seaborn
- ...

# Experiment Setup

 1. Setup Serverless Framework 
    `sudo npm install -g serverless --allow-root --unsafe-perm=true`
 2. Setup Accounts:
    - [AWS](https://serverless.com/framework/docs/providers/aws/guide/credentials/)
    - [Azure](https://serverless.com/framework/docs/providers/azure/guide/credentials/)
    - [Google](https://serverless.com/framework/docs/providers/google/guide/credentials/)
    - [IBM](https://serverless.com/framework/docs/providers/openwhisk/guide/credentials/)
 3. Setup [Terrafrom](https://learn.hashicorp.com/terraform/getting-started/install.html)

# Deployment Packages

 ### Usage
 To edit the function or mesurement points you only need to edit files in `deploymentPackage/logic`.
 Afterwards, apply your changes by running `deploymentPackage/copylogic.sh`.
 
 ### Settings
| Provider | Data-Center  | Location | Memory |
|----------|--------------|----------|--------|
| AWS      | eu-west-2    | London   | 1024   |
| MAF      | UK South     | London   | N.A.   |
| GCF      | europe-west2 | London   | 1024   |
| ICF      | UK South     | London   | 1024   |

The Benchmark-Server is located at digitalocean.com also in **London**.


 # Perform Experiment
 1. configure scripts/config.sh
 5. run `scripts/deploy.sh`
 6. run `scripts/serversideBenchmark.sh`
 7. run `scripts/remove.sh`

 # Generating reports
 1. `jupyter nbconvert --to notebook --execute Analysis.ipynb` 
