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
python -m app.movie_lookup
```

## Web App Usage

# Locally

Although the program can be run on a command-line, you can also view it as a Flask App.

The following command should run web application locally so you can view it in a browser at localhost:5000:

```sh
# Mac:
FLASK_APP=web_app flask run

# on windows:
export FLASK_APP=web_app
flask run
```

## Deploying to Production

# Prerequisites

If you haven't yet done so, [install the Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install), and make sure you can login and list your applications.

```sh
heroku login # just a one-time thing when you use heroku for the first time

heroku apps # at this time, results might be empty-ish
```

# Server Setup

> IMPORTANT: run the following commands from the root directory of your repository!

Use the online [Heroku Dashboard](https://dashboard.heroku.com/) or the command-line (instructions below) to [create a new application server](https://dashboard.heroku.com/new-app), specifying a unique name (e.g. "movie-lookup", but yours will need to be different):

```sh
heroku create movie-lookup # choose your own unique name!
```

Verify the app has been created:

```sh
heroku apps
```

Also verify this step has associated the local repo with a remote address called "heroku":

```sh
git remote -v
```

# Server Configuration

Before we copy the source code to the remote server, we need to configure the server's environment in a similar way we configured our local environment.

Instead of using a ".env" file, we will directly configure the server's environment variables by either clicking "Reveal Config Vars" from the "Settings" tab in your application's Heroku dashboard, or from the command line (instructions below):

![a screenshot of setting env vars via the app's online dashboard](https://user-images.githubusercontent.com/1328807/54229588-f249e880-44da-11e9-920a-b11d4c210a99.png)

```sh
# or, alternatively...

# get environment variables:
heroku config # at this time, results might be empty-ish

# set environment variables:
heroku config:set APP_ENV="production" 
heroku config:set OMDB_API_KEY="142571fd"
heroku config:set YOUTUBE_API_KEY="AIzaSyAfHm3zCacK6HykMxuL8_Fs25At9oMMnT4"
heroku config:set GOOGLE_SHEET_ID="1tKt_LQucVs2jRrXAVyprh2waB19SsMr-6-MZ3blnOk4"
heroku config:set GOOGLE_SHEET_NAME="To Watch List"
```

At this point, you should be able to verify the production environment has been configured with the proper environment variable values:

```sh
heroku config
```

# Deploying

After this configuration process is complete, you are finally ready to "deploy" the application's source code to the Heroku server:

```sh
git push heroku master
```

> NOTE: any time you update your source code, you can repeat this deployment command to upload your new code onto the server

# Running the Script

Once you've deployed the source code to the Heroku server, login to the server to see the files there, and take an opportunity to test your ability to run the script that now lives on the server:

```sh
heroku run bash # login to the server
# ... whoami # see that you are not on your local computer anymore
# ... ls -al # optionally see the files, nice!
# ... python -m app.movie_lookup # see the output, nice!
# ... exit # logout

# or alternatively, run it from your computer, in "detached" mode:
heroku run "python -m app.movie_lookup"
```
```sh
git push heroku master
```

There are no scripts to be scheduled, so skip that part. Instead, you'll need to create a special file called the "Procfile" in the repo's root directory to instruct the Heroku server which command to invoke in order to run the app:

```sh
web: gunicorn "web_app:create_app()"
```

> NOTE: since we're instructing the server to use the "gunicorn" package (Heroku's preferred tool) to run the web app on production, we'll also need to add `gunicorn` to the "requirements.txt" file so it will be installed on the server during the deployment process.

Save the "Procfile" and "requirements.txt" files, and make a commit before re-attempting to deploy your app to the server.

```sh
git push heroku master
```

View the server logs and troubleshoot as necessary until you're able to see the weather forecast in the browser. Nice!

```sh
heroku logs --tail