# Structured Extraction from Semi-Structured Data with AI and ETL

## Table of Contents

- [Objective](#objective)
- [Process](#process)
- [Installation](#installation)
- [Testing](#testing)
- [Structure](#structure)

## Objective

Process a semi-structured dataset (attached JSON file) and extract key
information into a structured, canonical format. The final structured data should be exposed as a
simple RESTful API.

## Process

#### 1. Data Cleaning

- Standardize column names, fields, and formats.
- Fill in missing data, adjust date columns, and create structured fields.
- Data cleaning tasks are located in `tasks/domain`.

#### 2. Data Enrichment

- Utilize an LLM (Gemini) to extract key-value pairs from text fields.
- The data enrichment task, located in `tasks/processed`, calls the LLM agent to perform data enrichment.
- **Limitations:** Since the selected LLM is free-tier, accuracy may be limited.

#### 3. ETL

- Tasks are imported into `pipeline/pipeline.py`.
- Extracts data into a structured format, applies the LLM for enrichment, and stores the processed data in a MongoDB database.
- The ETL follows this function flow:  
  `transform_to_domain() -> enrich_data() -> ingest_to_db()`

#### 4. Endpoint Creation with Flask API

- A model is implemented to filter out unwanted fields.
- The API includes a health status endpoint.
- A caching mechanism is added with a 50 second expiration time.

## Installation

#### 1

First you must get a `GEMINI` API key, so the pipeline does not run with errors.
Go to `https://aistudio.google.com/apikey` and create your API key for the project.
Add the Key to `.env` file just like the `.env.example` shows.

#### 2

Ensure that you have `Docker` and `Docker Compose` installed on your machine.  
Once installed, you can build and start the containers by running:

```bash
docker-compose up --build -d
```

This will automatically execute the script located at `/pipeline/pipeline.py`, which will:

- Transform the file,
- Enrich it using an LLM, and
- Ingest the processed data into the database.

If the pipeline runs successfully, the Flask application will be accessible at:
`http://127.0.0.1:4001`

## Testing

If the build completes without errors, you can retrieve data from the API.

#### 1. Check API Health

Verify that the API is running by checking its health status:

```bash
curl -X GET "http://127.0.0.1:4001/health"
```

#### 2. Retrieve Program Data

Once the API is confirmed to be running, you can fetch program details using:

```bash
curl -X GET "http://127.0.0.1:5000/programs/11757"
```

## Structure

```
ROOT:
│   .env.example                # Example environment variables file
│   config.py                   # Reads settings files from `settings` and applies them to a global `config` variable
│   docker-compose.yaml          # Docker Compose configuration file
│   Dockerfile.flaskapp          # Dockerfile for the Flask application
│   Dockerfile.pipeline          # Dockerfile for the data pipeline
│   mongo-init.js                # MongoDB initialization script
│
├───agent
│       agent.py                 # Starts the LLM model
│
├───api
│   │   app.py                   # Flask application entry point
│   │   extensions.py             # Flask extensions (e.g., caching)
│   │
│   ├───db
│   │       database.py           # Database configuration
│   │
│   ├───models
│   │       program.py            # Program-related database models
│   │
│   └───routes
│           health.py             # API health check endpoint
│           programs.py           # API endpoint to retrieve programs
│
├───data
│   ├───domain
│   │       processed.json        # First transformation layer output
│   │
│   ├───processed
│   │       enriched_file.json    # AI-enriched data
│   │
│   └───raw
│           dupixent.json         # Raw untransformed data
│
├───pipeline
│       pipeline.py               # ETL pipeline script
│
├───requirements
│       api.requirements.txt      # Dependencies for the API
│       pipeline.requirements.txt # Dependencies for the pipeline
│
├───settings
│       00-data.yaml              # Data-related settings
│       10-agent.yaml             # LLM agent settings
│       20-database.yaml          # Database settings
│
└───tasks                         # Scripts for each transformation layer
    ├───domain
    │       transform_file.py      # Processes raw data into a structured format
    │
    └───processed
            enrich_file.py         # Enhances data using AI model
            ingest_to_db.py        # Loads processed data into the database
```
