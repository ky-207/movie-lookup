# app/seach_service.py

import os
import json

from dotenv import load_dotenv
import requests
import re

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

# title lookup results from search
def print_sr(search_results, readable_list):
    """
    Prints results of movie lookup (movie/tv show title and release year)
    Param: search_results (list) like sr and readable_list (str) like org_list
    Example: print_sr(sr, org_list)
    Returns: None
    """

    for title in search_results:
            readable_list.append(title["Title"] + ", " + title["Year"].replace("–","-"))
            print(title["Title"] + " (" + title["Year"] +")") # prints a list of the search results' title and release year

    return None

# Titlecase string
def title_except(s, exceptions):
    """
    Transforms string so that it will capitalize the first letter in each word, with some exceptions
    Source: https://stackoverflow.com/questions/3728655/titlecasing-a-string-with-exceptions/3729060
    Param: s (str) like "Hi, my name is john smith" and exceptions (list of str) like ["a", "an", "is"]
    Example: title_except("Hi, my name is john smith", ["a", "an", "is"])
    Returns: "Hi, My Name is John Smith"
    """
    word_list = re.split(' ', s)       # re.split behaves as expected
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)

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

        print_sr(sr, org_list)
        print("----------------------------------")

        while True:
            correct_search = input("From the list above, what title were you looking for? Please write in the format of Title, Year (i.e. The Avengers, 1998): ")
            
            articles = ['a', 'an', 'of', 'the', 'is', 'with', 'in']
            correct_search = title_except(correct_search, articles)

            if (correct_search) in org_list:
                i = org_list.index(correct_search) # finds the index of the title the user is looking for in org_list so it can be matched with the one in the parsed_response
                id = sr[i]["imdbID"] 
                break
            else:
                print("Sorry, there was no match to the list above. Please try again and make sure you're writing in the correct format.")
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
    rating = parsed_response["Ratings"][0]["Value"]

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
    print(f"IMDb RATING: {rating}")
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
            break
        else:
            print("Sorry, that was not a valid choice, please try again and enter 'Yes' or 'No'.")