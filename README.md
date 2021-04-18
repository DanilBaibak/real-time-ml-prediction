# Machine Learning Service for Real-Time Predictions

This is an example of Machine Learning REST API application for online prediction. It covers topics such as:
* How to cache model, and when it might be useful to use asynchronous code;
* How to organize a pipeline updates without redeployment;
* How to improve the health check endpoint for a Machine Learning service;
* How to split and organize production and local development;

You can find the full article on Medium.

## Installation
* Run `make init`;
* Edit the `.env` file and set the database credentials;
* Run `make up`;
* Open in browser `127.0.0.1/health`. Server status and database connection should be active.
* You can find the API documentation by link `127.0.0.1/docs`.

## The project structure:
    |--docker
    |--src
        |--ml_pipelines
        |--models
        |--scripts
            |--train.py
        |--sql
            |--migrations
        |--tests
            |--unit_tests
            |--integration_tests
        |--utils
    |--server.py

* The `server.py` file is entry point for our REST API service.
* We will save the ML artifacts in the `ml_pipelines` folder.
* The `models` folder is for storage Pydantic schemas. It defines the properties and types to validate some data.
* The script `scripts/train.py` trains the ML model.


## How to use
* `make restart` will stop running containers, remove them and start application.
* `make bash` will create a new bash session in the container.

## Model training
Before you can start making any predictions, you need to train the Machine Learning model.
* Run `make up` and start application;
* In a new tab in the project folder run: `make bash`;
* Now you are inside the Docker container and can trigger the script to train the new model: `python scripts/training.py`;
* The ML pipeline is ready. Open the documentation `127.0.0.1/docs` and try to make a prediction.

## Database
* You can find training history of the model in the `ml_pipeline` table;
* All predictions are stored in the `predictions` table;
