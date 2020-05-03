# app/seach_service.py

import os
import json

from dotenv import load_dotenv
import requests

load_dotenv()

if __name__ == "__main__":

    #
    # INFO INPUTS
    #

    title = input("Please enter a movie or tv show title (i.e. 'Iron Man' or 'Game of Thrones'): ") # accept user input

    # how to replace whitespaces (source): https://stackoverflow.com/questions/1007481/how-do-i-replace-whitespaces-with-underscore-and-vice-versa
    title.replace(" ","+") # transforms the user input so that it is suitable for the request url later

    OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
    request_url = f"https://omdbapi.com/?s={title}&apikey={OMDB_API_KEY}"
    response = requests.get(request_url)

    # validating user's input
    if "\"Response\":\"False\"" in response.text:
        print("Oops, couldn't find that movie. Please try again.")
        exit()

    parsed_response = json.loads(response.text)

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

    # app/to_watch_service.py

import gspread
from gspread.exceptions import SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

DOCUMENT_KEY = os.environ.get("GOOGLE_SHEET_ID", "OOPS: Please get the spreadsheet identifier from its URL.")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", default="To Watch List")

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "spreadsheet_credentials.json")
AUTH_SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

class SpreadsheetService():
    def __init__(self):
        print("INITIALIZING NEW SPREADSHEET SERVICE...")
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
        self.client = gspread.authorize(self.credentials)
        self.sheet_id = DOCUMENT_KEY
        self.sheet_name = SHEET_NAME
        self.sheet = None
        self.movies = None

    def get_movies(self):
        print("GETTING MOVIES FROM THE SPREADSHEET...")
        doc = self.client.open_by_key(self.sheet_id)
        self.sheet = doc.worksheet(self.sheet_name)
        self.movies = self.sheet.get_all_records()
        return self.sheet, self.movies

    def create_movie(self, movie_attributes): 
        self.get_movies()
        if len(self.movies) == 1:
            print(f"DETECTED {len(self.movies)} EXISTING MOVIE")
        else:
            print(f"DETECTED {len(self.movies)} EXISTING MOVIES")
        next_row_number = len(self.movies) + 2
        if len(self.movies) == 0:
            next_id = 1
        else:
            next_id = max([int(m["ID"]) for m in self.movies]) + 1
        movie = {
            "ID": next_id,
            "Title": movie_attributes["Title"],
            "Year": movie_attributes["Year"],
            "Genre": movie_attributes["Genre"],
            "Director": movie_attributes["Director"],
            "Actors": movie_attributes["Actors"],
            "Plot": movie_attributes["Plot"]
        }
        next_row = list(movie.values())
        response = self.sheet.insert_row(next_row, next_row_number)
        return response

    def get_movie(self, movie_id):
        """
        Will raise IndexError if movie identifier is not found in the list
        Otherwise will return the movie as a dictionary
        """
        if not (self.sheet and self.movies): self.get_movies()
        matching_movies = [m for m in self.movies if str(m["ID"]) == str(movie_id)]
        while True:
            try:
                return matching_movies[0]["Title"]
                break
            except IndexError:
                return "The movie associated with this id does not exist in this list. Sorry!"
                break
    def update_movie(self, movie_attributes):
        return True

    def destroy_movie(self, movie_id):
        if not (self.sheet and self.movies): self.get_movies()
        matching_movies = [m for m in self.movies if str(m["ID"]) == str(movie_id)]
        while True:
            try:
                matching_movie_title = matching_movies[0]["Title"]
                print(f"{matching_movie_title} has been deleted from your watch list.")
                doc = self.client.open_by_key(self.sheet_id)
                worksheet = doc.worksheet(self.sheet_name)
                cell = worksheet.find(matching_movie_title)
                row = cell.row
                worksheet.delete_rows(row)
                break
            except IndexError:
                print("The movie associated with this id does not exist in this list. Sorry!")
                break

    def clear_list(self):
        if not (self.sheet and self.movies): self.get_movies()
        doc = self.client.open_by_key(self.sheet_id)
        worksheet = doc.worksheet(self.sheet_name)
        worksheet.resize(rows=1)
        worksheet.resize(rows=30)
        return "CLEARING LIST..."

if __name__ == "__main__":

    ss = SpreadsheetService()

    sheet, movies = ss.get_movies()
    print("----------------------------------")
    print(f"LISTING MOVIES FROM THE '{sheet.title}' SHEET")

    for movie in movies:
        print(" + " + str(movie["ID"]) + ": " + movie["Title"])

    print("----------------------------------")
    print("CREATING A MOVIE...")
    movie_attributes = parsed_response

    response = ss.create_movie(movie_attributes)
    print("----------------------------------")
    print(f"... UPDATED RANGE {response['updatedRange']} ({response['updatedCells']} CELLS)")
    
    print("----------------------------------")
    while True:
        x = input("Would you like to get a movie? [Y/N] ")
        if x.lower() == "y":
            movie_id = input("Which movie would you like to get? Please enter its id (e.g. 2): ")
            print("GETTING MOVIE:", movie_id)
            print(ss.get_movie(movie_id))
        elif x.lower() == "n":
            break
        else:
            print("Please input either Y or N.")

    print("----------------------------------")
    while True:
        x = input("Would you like to delete a movie? [Y/N] ")
        if x.lower() == "y":
            movie_id = input("Which movie would you like to delete? Please enter its id (e.g. 2): ")
            print("DELETING MOVIE:", movie_id)
            ss.destroy_movie(movie_id)
        elif x.lower() == "n":
            break
        else:
            print("Please input either Y or N.")

    print("----------------------------------")
    while True:
        x = input("Would you like to clear the list? [Y/N] ")
        if x.lower() == "y":
            ss.clear_list()
            break
        elif x.lower() == "n":
            break
        else:
            print("Please input either Y or N.")

