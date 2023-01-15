
# SateliteForestDetection
Software used for detecting forest surfaces based on Santinel2 datasets.


## Instalation 

The Python env is created with Poetry. To install the needed libs use:

    poetry install 
 
## Configuration
Create the file: src/settings/credentials.py with contains:

    AUTH  = {"USERNAME": "<username>", "PASSWORD": "<pass>"}

where the username and pass are credentials for the SentinelAPI.

## Run

Run the Satelite.ipynb file to see some examples

## Future work

- replace manual threshold with classifier 
- create GUI for easier interactions
