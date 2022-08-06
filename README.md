# CoMET Jupyter Notebooks

## Use

- Pull this repo
- install jupyter lab with ```pip install jupyterlab```
- look at the requirements.txt for required python libraries -- pip install any that you do not have
- from shell change directory to the notebook location and run jupter with command ```jupyter-lab```

Or you can run a live interactive session here; your changes will not be saved between sessions. 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jerrilynnreeves/CoMET-Jupyter-Notebook.git/HEAD)

## CoMET API Helper

- comet_api_helper.ipynb

Code blocks for using API endpoints: create, delete, update, search, validate

Notes:
- You must have a CoMET User account and be assigned a record group to use these APIs.
- User accounts are limited to those with a noaa.gov email

A Sample ISO 19115-2 file has been included in this repo (eample-iso.xaml). It is NCEI Metadata Template v1.2.

## WAF Support

- waf_support.ipynb

Tool to help analize RWAF Pipeline results by processing the generated PublishReport found on the publically available source: https://data.noaa.gov/waf/

## References:
- About NCEI metadata: https://www.ncei.noaa.gov/resources/metadata
- NCEI's Metadata Template: https://data.noaa.gov/waf/templates/iso/xml/ncei_template-clean.xml
- CoMET UI: https://data.noaa.gov/cedit/
- API Documentation: https://data.noaa.gov/cedit/openApiDoc
