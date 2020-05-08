# app/to_watch_service.py
# Adapted from the code available here: https://github.com/prof-rossetti/web-app-starter-flask-sheets
 
import json
import os
 
from dotenv import load_dotenv
import gspread
from gspread.exceptions import SpreadsheetNotFound
from oauth2client.service_account import ServiceAccountCredentials
 
load_dotenv()
 
DOCUMENT_KEY = os.environ.get("GOOGLE_SHEET_ID", "OOPS: Please get the spreadsheet identifier from its URL.")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", default="To Watch List")
 
CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "app", "..", "spreadsheet_credentials.json")
AUTH_SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
 
class SpreadsheetService():
    def __init__(self):
        """
        Initializes and sets up the spreadsheet service.
        """
        print("INITIALIZING NEW SPREADSHEET SERVICE...")
        
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
        self.client = gspread.authorize(self.credentials)
        self.sheet_id = DOCUMENT_KEY
        self.sheet_name = SHEET_NAME
        self.sheet = None
        self.movies = None

    def get_movies(self):
        """
        Opens the selected spreadsheet and retrieves all the data from the spreadsheet.
        Example: self.getmovies()
        Returns: the selected sheet and the data in it
        """
        #print("GETTING MOVIES FROM THE SPREADSHEET...")
        doc = self.client.open_by_key(self.sheet_id)
        self.sheet = doc.worksheet(self.sheet_name)
        self.movies = self.sheet.get_all_records()
        return self.sheet, self.movies

    def create_movie(self, movie_attributes): 
        """
        Creates a new movie in the spreadsheet with the specified attributes.
        Param: movie_attributes (dict) like parsed_response
        Example: ss.create_movie(parsed_response)
        Returns: the new row
        """
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
        Will raise IndexError if movie identifier is not found in the list.
        Otherwise will return the movie as a dictionary.
        Param: movie_id (int)
        Example: ss.get_movie(movie_id)
        Returns: Movie as a dictionary
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

    def destroy_movie(self, movie_id):
        """
        Deletes all the information pertaining to a specified movie in the spreadsheet if available.
        Param: movie_id (int)
        Example: ss.destroy_movie(movie_id)
        """
        if not (self.sheet and self.movies): self.get_movies()
        matching_movies = [m for m in self.movies if str(m["ID"]) == str(movie_id)]
        while True:
            try:
                matching_movie_title = matching_movies[0]["Title"]
                doc = self.client.open_by_key(self.sheet_id)
                worksheet = doc.worksheet(self.sheet_name)
                cell = worksheet.find(matching_movie_title)
                row = cell.row
                worksheet.delete_rows(row)
                print(f"{matching_movie_title} has been deleted from your watch list.")
                break
            except (IndexError, gspread.exceptions.CellNotFound):
                print("The movie associated with this id does not exist in this list. Sorry!")
                break

    def clear_list(self):
        """
        Clears the entire list except the headers.
        """
        if not (self.sheet and self.movies): self.get_movies()
        doc = self.client.open_by_key(self.sheet_id)
        worksheet = doc.worksheet(self.sheet_name)
        worksheet.resize(rows=1)
        worksheet.resize(rows=30)
        return "CLEARING LIST..."

# provides an option menu for the user to either retrieve a movie, delete a movie, clear the list, or exit the program
def user_options(option, ss):
    """
    Param: option (str) like "1"
    Example: user_options("1")
    """
    while True:
        if option == "1":
            print("----------------------------------")
            movie_id = input("Which movie would you like to get? Please enter its id (e.g. 2): ")
            print("GETTING MOVIE:", movie_id)
            print(ss.get_movie(movie_id))
            break
        elif option == "2":
            print("----------------------------------")
            movie_id = input("Which movie would you like to delete? Please enter its id (e.g. 2): ")
            print("DELETING MOVIE:", movie_id)
            ss.destroy_movie(movie_id)
            break
        elif option == "3":
            print("----------------------------------")
            ss.clear_list()#
            print("The to-watch list has been cleared.")
            break
        elif option == "4":
            print("Thank you for using the spreadsheet service!")
            exit()
        else:
            print("Sorry, that wasn't an option. Please input 1, 2, 3, or 4.")
            break

if __name__ == "__main__":

    ss = SpreadsheetService()

    sheet, movies = ss.get_movies()
    print("----------------------------------")
    print(f"LISTING MOVIES FROM THE '{sheet.title}' SHEET")

    for movie in movies:
        print(" + " + str(movie["ID"]) + ": " + movie["Title"])

    movie_attributes = parsed_response
    
    response = ss.create_movie(movie_attributes)
    print("----------------------------------")
    print("CREATING A MOVIE...")
    print("ADDED NEW MOVIE: " + movie_attributes["Title"])

    print("----------------------------------")
    print(f"... UPDATED RANGE {response['updatedRange']} ({response['updatedCells']} CELLS)")
    
    while True:
        print("----------------------------------")
        sheet, movies = ss.get_movies()

        option = input("Would you like to: 1. Get a movie; 2. Delete a movie; 3. Clear list; 4. Exit? Please enter 1, 2, 3, or 4: ")
        user_options(option,ss)