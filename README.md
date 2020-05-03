# movie-lookup

## Installation

Clone or download from [Github Source](https://github.com/kristyyip/movie-lookup) onto your computer, choosing a familiar download location like the Desktop.

Then navigate into the project repository from the command-line:

```sh
cd ~/Desktop/movie-lookup
```

## Environment Variable Setup

### OMDb API Key
Before using or developing this application, take a moment to [obtain an OMDb API Key](https://www.omdbapi.com/apikey.aspx) (e.g. "abc123").

After obtaining an API Key, create a new file in this repository called ".env" (hidden by the .gitignore file), and update the contents of the ".env" file to specify your real API Key in an enviornment variable:

    OMDB_API_KEY="abc123"

### YouTube API Key
Before using or developing this application, take a moment to obtain a YouTube API Key by [following these instructions](https://developers.google.com/youtube/v3/getting-started) (e.g. "abc123").

After obtaining an API Key, update the contents of the ".env" file to specify your real API Key in an environment variable:

    YOUTUBE_API_KEY="abc123"

## Google Sheets Setup

### Downloading API Credentials 
Using the same project you created for the YouTube API Key in the [Google Developer Console](https://console.developers.google.com/cloud-resource-manager), search for "Google Sheets API" and "Google Drive API" and enable both. 

From the [API Credentials Page](https://console.developers.google.com/apis/credentials), follow a process to create and download credentials to use the APIs. Fill in the form as follows:

* API: "Google Sheets API"
* Calling From: "Web Server"
* Accessing: "Application Data"
* Using Engines: "No"

The suggested credentials will be for a service account. Follow the prompt to create a new service account with a role of: "Project" > "Editor", and create credentials for that service account. Download the resulting .json file and store it in this repo as "spreadsheet_credentials.json".

Make sure to store the credentials in an environment variable.

```sh
export GOOGLE_API_CREDENTIALS="$(< spreadsheet_credentials.json)"
echo $GOOGLE_API_CREDENTIALS #> { "type": "service_account" ... }
```

### Configuring a Google Sheet Datastore
Create a [Google Sheet document](https://docs.google.com/spreadsheets/u/0/). Rename the first sheet as "To Watch List" with column headers 'ID', 'Title', 'Year', 'Genre', 'Director', 'Actors', and 'Plot'. 

Make sure you share the document and grant edit privileges to the "client email" address located in the "spreadsheet_credentials.json" file.

From the URL, obtain the document's unique identifier and store it in an environment variable:

    GOOGLE_SHEET_ID="abc123"

Name the document and store it in an environment variable as well:

    GOOGLE_SHEET_NAME="To Watch List"

## Virtual Environment Setup

Create and activate a new Anaconda virtual environment from the command-line:
```sh
conda create -n movie-env python=3.7
conda activate movie-env
```

From inside the virtual environment, install package dependencies:
```sh
pip install -r requirements.txt
```

## Usage
Run the program:
```sh
python app/movie_lookup.py
```