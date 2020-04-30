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

After obtaining an API Key, update the contents of the ".env" file to specify your real API Key in an enviornment variable:

    YOUTUBE_API_KEY="abc123"

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