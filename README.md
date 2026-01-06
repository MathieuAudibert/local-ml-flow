[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_local-ml-flow&metric=alert_status&token=9d435cc3c26b9d43458fca3e4d17ed38435ef52f)](https://sonarcloud.io/summary/new_code?id=MathieuAudibert_local-ml-flow)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_local-ml-flow&metric=coverage&token=9d435cc3c26b9d43458fca3e4d17ed38435ef52f)](https://sonarcloud.io/summary/new_code?id=MathieuAudibert_local-ml-flow)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_local-ml-flow&metric=ncloc&token=9d435cc3c26b9d43458fca3e4d17ed38435ef52f)](https://sonarcloud.io/summary/new_code?id=MathieuAudibert_local-ml-flow)

# local-ml-flow

This project is a combination of the technologies and concepts I want to understand better and improve. 

## Context

This project is a local MLOps Ecosystem designed to automate the machine learning lifecycle using FastAPI, LocalStack (AWS emulation), and a robust GitLab CI/CD pipeline. The goal is to orchestrate data retrieval, model training, and evaluation through serverless functions in a fully containerized environment.

You can find the dataset in `src/config/housing.csv` or on [Kaggle](https://www.kaggle.com/datasets/chandanashwath/housing-dataset?resource=download)

## Requirements 

- [Python](https://www.python.org/downloads/) $`\geq`$ 3.10
- [Docker engine](https://docs.docker.com/engine/install/)
- [Terraform](https://www.it-connect.fr/chapitres/terraform-installation-linux-windows-macos/)

## Technical Stack

- Local Stack : local AWS/Cloud computing
- Python : programming langage
- SonarQube : code quality
- GitHub Actions : CI/CD

---

Python dependencies
- FastAPI : make APIs
- Scikit-learn : Machine learning
- Boto3 : handle cloud computing

## Setup

Clone the repository first : 

```bash
git clone https://github.com/MathieuAudibert/local-ml-flow.git
```

```bash
git clone git@github.com:MathieuAudibert/local-ml-flow.git
```

Create your Python virtual env : 

```bash
python -m venv venv
```

You will need then to create the build files required to have the lambdas (will take some time) :
```bash
./bin/create_layers.sh
```

You can setup and launch locally with the script in bin/start_all.sh (you will need to create a .env in the root, help yourself w/ .env.example): 
```bash
./bin/start_all.sh
```

You can then open the endpoint running on (localhost:8080)[http://localhost:8080] and navigate throught the endpoints 🚀

## DevOps 

The project follows this simple workflow : 

![DevOps workflow](/.github/images/devops.png)

## Machine learning

This project uses a simple dataset. So we will use simple [linear regression](https://en.wikipedia.org/wiki/Linear_regression)

The basic linear regression formula is : $`y = \beta_0 + \beta_1x_1 + \beta_2x_2 + \dots + \beta_nx_n + \epsilon`$

Now transposed to my project : $`Price = \beta_0 + \beta_1(area) + \beta_2(bedrooms) + \dots + \beta_n(furnishing) + \epsilon(error)`$

Where error is the difference between the predicted price and the actual price

Then, we check the accuracy with the determination coefficient nammed $`R²`$ wich formula is : 

$`R² = 1 - \frac{\sum( y_a - y_p )²}{\sum( y_a - \bar{y} )²}`$ 

Where : 
- $`y_a`$ (y actual) is the real value of the target variable and $`y_p`$ (y predicted) is predicted by the model
- $`\bar{y}`$ is the mean of the real values

This ratio gives us the % fof the variance explained by the model

Here is the workflow scheme : 

![workflow scheme, based of off (https://docs.localstack.cloud/aws/tutorials/reproducible-machine-learning-cloud-pods/)](/.github/images/workflow.png)

## Miscellaneous

* The setup can take some time, I tried optimizing it but the project's dependencies AND the lambdas are quite heavy
* some files will be created in the filetree with localstack, this is annoying while going throught filetree so create .vscode/settings.json file in the root w/ these values
```json
"files.exclude": {
    "localstack_data": true,
    
    This is not necessary, but it's quite practical
    "/pycache": true,
    ".pytest_cache": true,
    "**.egg-info/": true,
    "**/__pycache__/": true
}
```
* make sure to modify the scripts in /bin based on your distribution (replace powershell with zip etc...)
* If something breaks w/ the lambdas you can find the log in [terraform/logs/output.txt](terraform/logs/)

## Future

In the future I would like to : 
* Implement a deeper ML/DL algorithm w/ more parameters
* Find a better solutions for lambdas, decompressing and recompressing through powershell is SLOW
* Go deeper w/ localstack
* Implement K8S & ArgoCD

## Contact

| GitHub | email |
| --- | --- |
| @MathieuAudibert | mathieu.audibert@edu.devinci.fr |

