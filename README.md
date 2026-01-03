[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_local-ml-flow&metric=alert_status&token=9d435cc3c26b9d43458fca3e4d17ed38435ef52f)](https://sonarcloud.io/summary/new_code?id=MathieuAudibert_local-ml-flow)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_local-ml-flow&metric=coverage&token=9d435cc3c26b9d43458fca3e4d17ed38435ef52f)](https://sonarcloud.io/summary/new_code?id=MathieuAudibert_local-ml-flow)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=MathieuAudibert_local-ml-flow&metric=ncloc&token=9d435cc3c26b9d43458fca3e4d17ed38435ef52f)](https://sonarcloud.io/summary/new_code?id=MathieuAudibert_local-ml-flow)

# local-ml-flow

This project is a combination of the technologies and concepts I want to understand better and improve. 

## Context

This project is a local MLOps Ecosystem designed to automate the machine learning lifecycle using FastAPI, LocalStack (AWS emulation), and a robust GitLab CI/CD pipeline. The goal is to orchestrate data retrieval, model training, and evaluation through serverless functions in a fully containerized environment.

You can find the dataset in src/config/housing.csv

## Technical Stack

- Local Stack : local AWS/Cloud computing
- Python : programming langage
- SonarQube : code quality
- GitHub Actions : CI/CD

---

Python dependencies
- FastAPI : make APIs
- PyTorch : Machine learning
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

Activate your venv & install dependencies : 
```bash
source venv/Scripts/activate or source venv\bin\activate on macos/linux
pip install -e .
```

## Contact

| GitHub | email |
| --- | --- |
| @MathieuAudibert | mathieu.audibert@edu.devinci.fr |

