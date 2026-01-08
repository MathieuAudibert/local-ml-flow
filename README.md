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

You can setup and launch locally with the script in bin/start_all.sh (you will need to create a .env in the root, help yourself w/ .env.example): 
```bash
./bin/start_all.sh
```

You can then open the endpoint running on <u>http://localhost:8000</u> and navigate throught the endpoints 🚀

## DevOps 

The project follows this simple CI/CD workflow : 

```mermaid
graph TB;
    A[Push/PR Event] --> B{Branch Check};
    B -->|Any Branch| C[Sonar Task];
    C --> D[Code Quality Analysis];
    D --> E[Build Task];
    E --> F[Set up Docker Buildx];
    F --> G[Build Docker Image];
    G --> H{On Main Branch?};
    H -->|Yes| I[Promote Task];
    H -->|No| Z[End];
    I --> J[GitHub Container Registry Login];
    J --> K[Build & Push to ghcr.io];
    K --> Z[End];

    style A fill:#e1f5ff;
    style C fill:#fff4e1;
    style E fill:#fff4e1;
    style I fill:#e8f5e9;
    style Z fill:#f3f3f3;
```

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

```mermaid
graph TB
    Start([API Request]) --> Invoke1[Invoke Ingestion Lambda]
    
    subgraph Ingestion["Ingestion Lambda"]
        I1[Get housing.csv from S3]
        I2[Clean Dataset<br/>yes/no → 1/0]
        I3[Train/Test Split]
        I4[Train ML Model<br/>Linear Regression]
        I5[Save model.joblib to S3]
        I6[Save x_test.joblib to S3]
        I7[Save y_test.joblib to S3]
        
        I1 --> I2 --> I3 --> I4 --> I5
        I4 --> I6 --> I7
    end
    
    Invoke1 --> I1
    I7 --> Invoke2[Invoke Inference Lambda]
    
    subgraph Inference["Inference Lambda"]
        IN1[Get model.joblib from S3]
        IN2[Get x_test.joblib from S3]
        IN3[Get y_test.joblib from S3]
        IN4[Make Predictions]
        IN5[Calculate R² Score]
        IN6[Save score.txt to S3]
        
        IN1 --> IN4
        IN2 --> IN4
        IN3 --> IN4
        IN4 --> IN5 --> IN6
    end
    
    Invoke2 --> IN1
    IN6 --> API[FastAPI Endpoints]
    
    subgraph FastAPI["FastAPI Server"]
        EP1["/bucket/get-all-models"]
        EP2["/result/local-ml-flow-data"]
        EP3["/bucket/dataset"]
        EP4["/lambda/get-all-lambdas"]
    end
    
    API --> FastAPI
    
    subgraph S3["S3 Buckets"]
        B1[(local-ml-flow-data<br/>housing.csv<br/>x_test.joblib<br/>y_test.joblib<br/>score.txt)]
        B2[(local-ml-flow-models<br/>model.joblib)]
    end
    
    I1 -.read.- B1
    I5 -.write.- B2
    I6 -.write.- B1
    I7 -.write.- B1
    IN1 -.read.- B2
    IN2 -.read.- B1
    IN3 -.read.- B1
    IN6 -.write.- B1
    FastAPI -.read.- B1
    FastAPI -.read.- B2

    style Start fill:#e1f5ff
    style Ingestion fill:#fff4e1
    style Inference fill:#e8f5e9
    style FastAPI fill:#f3e5f5
    style S3 fill:#fce4ec
```

And here is the *complete* workflow :

```mermaid
graph TB
    User[User/Developer] -->|git push| GH[GitHub Repository]
    
    subgraph CI/CD["GitHub Actions Pipeline"]
        GH --> Sonar[SonarCloud Analysis]
        Sonar --> Build[Build Docker Image]
        Build --> Promote{Main Branch?}
        Promote -->|Yes| GHCR[Push to ghcr.io]
        Promote -->|No| End1[Skip Promote]
    end
    
    Dev[Local Development] -->|docker compose up| LS[LocalStack Container]
    
    subgraph LocalEnv["Local Environment"]
        LS --> TF[Terraform Init]
        TF --> S3Buckets[Create S3 Buckets]
        TF --> LambdaDeploy[Deploy Lambdas]
        TF --> Upload[Upload housing.csv]
        
        LambdaDeploy --> L1[Ingestion Lambda]
        LambdaDeploy --> L2[Inference Lambda]
        
        Upload --> S3Data[(S3: local-ml-flow-data)]
        L1 -->|train & save| S3Models[(S3: local-ml-flow-models)]
        L1 -->|save test data| S3Data
        L2 -->|read model| S3Models
        L2 -->|read test data| S3Data
        L2 -->|save score| S3Data
        
        FastAPI[FastAPI Server:8000] -->|read| S3Data
        FastAPI -->|read| S3Models
        FastAPI -->|invoke| L1
        FastAPI -->|invoke| L2
    end
    
    User -->|http://localhost:8000| FastAPI

    style CI/CD fill:#e3f2fd
    style LocalEnv fill:#f1f8e9
    style User fill:#fce4ec
    style FastAPI fill:#f3e5f5
```

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
* make sure to modify the scripts in /bin based on your distribution
* If something breaks w/ the lambdas you can find the log in [terraform/logs/output.txt](terraform/logs/)
* the determination coefficient is ridiculously low (35%)

## Future

In the future I would like to : 
* Implement a deeper ML/DL algorithm w/ more parameters
* Find a better solutions for lambdas
* Making a dockerfile for lambdas is a disgusting way to bypass the file limit
* Go deeper w/ localstack
* Implement K8S & ArgoCD

## Contact

| GitHub | email |
| --- | --- |
| @MathieuAudibert | mathieu.audibert@edu.devinci.fr |

