### Getting started

0. Navigate to the carbon_chain directory

1. Create a python virtual environment and activate it and install requirements

```
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

2. Download all 4 excel files and put it in a folder called data <br>
   a. Make directory called data

```
mkdir data
```

b. Download the files below from <a href="https://mrv.emsa.europa.eu/#public/emission-report">The MRV system</a>
![Alt Files to be downloaded](data_source.png 'Optional title')

c. Move the files downloaded to the `data` folder created above

### Option A: Data Analysis & Visualization

Check the notebook named DataAnalysisAndVisualization.ipynb in the root module

### Option B: Build an API

The APIs are defined in the backend/ folder. To run the code, we need to download both docker and docker-compose.

3. Run initialization script

```
bash initialize.sh
```

4. Build and start containers

```
docker-compose up -d --build
```

5. To Check the logs, run

```
docker-compose logs -f
```

6. Navigate to the following url to see <a href="http://localhost:8000/docs#/default">the Endpoints</a>
