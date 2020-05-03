# app/seach_service.py

import os
import json

from dotenv import load_dotenv
import requests

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import webbrowser

load_dotenv()

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
YOUTUBE_API_SERVICE_NAME='youtube'
YOUTUBE_API_VERSION='v3'

def get_response(title):
    """
    Issues a request and parses response

    Param: (movie or tv show) title (str) like "Iron Man" or "Game of Thrones"

    Example: get_response("Iron Man")

    Returns: parsed_response # dictionary representing the original JSON response
    """
    # how to replace whitespaces (source): https://stackoverflow.com/questions/1007481/how-do-i-replace-whitespaces-with-underscore-and-vice-versa
    title.replace(" ","+") # transforms the user input so that it is suitable for the request url later

    request_url = f"https://omdbapi.com/?s={title}&apikey={OMDB_API_KEY}"
    response = requests.get(request_url)

    # validating user's input
    if "\"Response\":\"False\"" in response.text:
        print("Oops, couldn't find that movie. Please try again.")
        exit()

    parsed_response = json.loads(response.text)
    return parsed_response

# finds YouTube trailer
def youtube_search(options):
    """
    Searches for YouTube video 
    
    Source: https://github.com/youtube/api-samples/blob/master/python/search.py

    Param: options (str) like "Iron Man"

    Example: youtube_search("Iron Man")

    Returns: url link to trailer
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=YOUTUBE_API_KEY)

    # Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(
        q=options + " trailer",
        part='id,snippet',
        maxResults=1
    ).execute()

    # Add each result to the appropriate list, and then display the lists of matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':                 
            #print ('YouTube Trailer:\n', search_result['snippet']['title'])
            #print(' ' + 'https://www.youtube.com/watch?v=' + search_result['id']['videoId'])
            trailer_url = f"https://www.youtube.com/watch?v=" + search_result['id']['videoId']
            print("----------------------------------")
            return trailer_url
        else:
            print('Sorry, a trailer could not be found for this movie.')
            print("----------------------------------")

if __name__ == "__main__":

    #
    # INFO INPUTS
    #
    
    title = input("Please enter a movie or tv show title (i.e. 'Iron Man' or 'Game of Thrones'): ") # accept user input

    parsed_response = get_response(title)

    sr = parsed_response["Search"] # search results


    # if there is more than one result, then the program will have the user choose the title they were looking for
    # from a list; otherwise, the program will go ahead and display the information of the one found result
    if int(parsed_response["totalResults"]) > 1:
        
        org_list = []

        for t in sr:
            org_list.append(t["Title"] + ", " + t["Year"])
            print(t["Title"] + " (" + t["Year"] +")") # prints a list of the search results' title and release year

        print("----------------------------------")
        
        correct_search = input("From the list above, what title were you looking for? Please write in the format of Title, Year (i.e. The Avengers, 1998): ")
        
        correct_title = correct_search.split(", ")
        correct_name = correct_title[0]

        if (correct_search) in org_list:
            i = org_list.index(correct_search) # finds the index of the title the user is looking for in org_list so it can be matched with the one in the parsed_response
            id = sr[i]["imdbID"] 
        else:
            print("That's not an option from the list above. Please try again.")
    else:
        id = sr[0]["imdbID"]
        correct_name = title
        correct_search = title


    # make another request to match ids
    request_url = f"https://omdbapi.com/?i={id}&apikey={OMDB_API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    title_name = parsed_response["Title"]
    release_year = parsed_response["Year"]
    genre = parsed_response["Genre"]
    director = parsed_response["Director"]
    cast = parsed_response["Actors"]
    summary = parsed_response["Plot"]

    # rating preference on Rotten Tomatoes, but will resort to IMDb's rating if non-existent
    if "Rotten Tomatoes" in parsed_response["Ratings"][1]["Source"]:
        rating = "ROTTEN TOMATOES RATING: " + parsed_response["Ratings"][1]["Value"]
    else:
        rating = "IMDb RATING: " + parsed_response["Ratings"][0]["Value"]

    #
    # INFO OUTPUTS
    #

    print("----------------------------------")
    print(f"TITLE: {title_name} ({release_year})")
    print("----------------------------------")

    print(f"GENRE: {genre}")
    print(f"DIRECTOR: {director}")
    print(f"MAIN CAST: {cast}")
    print(f"SUMMARY: {summary}")
    print(rating)
    print("----------------------------------")




    # YouTube search    
    while True:
        youtube = input(f"Would you like to see a trailer for {title_name}? Enter 'Yes' or 'No': ")
        if youtube.lower() == "yes":
            print("Okay, pulling up trailer now...")
            url = youtube_search(correct_search)
            webbrowser.open(url)
            break
        elif youtube.lower() == "no":
            print("Okay, you opted not to watch the trailer.")
            print("----------------------------------")
            youtube_search(correct_search)
            break
        elif youtube.lower() == "no":
            print("Okay, you opted not to watch the trailer.")
            print("----------------------------------")