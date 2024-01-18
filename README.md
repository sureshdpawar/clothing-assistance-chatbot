
## Overview of the App

This is a streamlit assistant chat bot app for clothing.

This app is developed using Streamlit and Open AI Assistance, the gpt-4-1106-preview LLM model is used.

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://clothing-assistance-chatbot-jtlcdv2fejs4ebtiuj2yrq.streamlit.app/)

### Get an OpenAI API key

The app needs an Open API key, You can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.

## Run it locally
From Linux machine root directory
```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run .\clothing-assistance.py
```
From Windows machine root directory
```sh
virtualenv .venv
.\venv\Scripts\activate
pip install -r requirements.txt
streamlit run .\clothing-assistance.py
```