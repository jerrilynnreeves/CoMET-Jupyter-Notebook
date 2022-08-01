# CoMET Jupyter Notebook
A Jupyter Notebook that demonstrates NCEI's CoMET API
- Pull this repo
- install jupyter lab with ```pip install jupyterlab```
- from shell change directory to the notebook location and run jupter with command ```jupyter-lab```

Or you can run a live interactive session here; your changes will not be saved between sessions. 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jerrilynnreeves/CoMET-Jupyter-Notebook.git/HEAD)

Notes:
- You must have a CoMET User account and be assigned a record group to use these APIs.
- User accounts are limited to those with a noaa.gov email

Which notebook to use:
- CoMET API Notebook Standalone code is all self contained within the Notebook. All code is visible for each API call. You can share just this file with others
- Comet APIs Notebook is dependent on comet_api.py and the uploads and exports folder. This notebook hides the actual code running the API calls.

References:
- About NCEI metadata: https://www.ncei.noaa.gov/resources/metadata
- NCEI's Metadata Template: https://data.noaa.gov/waf/templates/iso/
- CoMET UI: https://data.noaa.gov/cedit/
