# web_app/routes/movie_routes.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from flask import Blueprint, render_template, request, session, current_app, jsonify, flash, redirect

from app.search_service import get_response, get_response_2, print_sr, title_except, youtube_search

from app.recommendations import combine_features, get_title_from_index, get_index_from_title, movie_recommendations

from app.to_watch_service import SpreadsheetService

movie_routes = Blueprint("movie_routes", __name__)

@movie_routes.route("/movie/search")
def movie_search():
    print("VISITED THE MOVIE SEARCH PAGE...")
    return render_template("movie_search.html")

@movie_routes.route("/movie/search-results", methods=["GET", "POST"])
def search_results():
    print("GENERATING SEARCH RESULTS...")

    if request.method == "POST":
        print("FORM DATA:", dict(request.form)) #> {'title': 'Iron Man'}
        title = request.form["title"]
    elif request.method == "GET":
        print("URL PARAMS:", dict(request.args))
    
        title = request.args["title"]
    
    parsed_response = get_response(title)
 
    sr = parsed_response["Search"] # search results

    org_list = []
    print_sr(sr, org_list)

    session["sr"] = sr
    session["org_list"] = org_list
    
    return render_template("search_results.html", title=title, org_list=org_list)


@movie_routes.route("/movie/info", methods=["GET", "POST"])
def display_info():
    print("GENERATING INFO...")

    if request.method == "POST":
        print("FORM DATA:", dict(request.form)) #> {'title_year': 'Iron Man, 2008'}
        title_year = request.form["title_year"]
    elif request.method == "GET":
        print("URL PARAMS:", dict(request.args))
    
        title_year = request.args["title_year"]

    sr = session.get("sr", None)
    org_list = session.get("org_list", None)


    articles = ['a', 'an', 'of', 'the', 'is', 'with', 'in']
    title_year = title_except(title_year, articles)

    correct_title = title_year.split(", ")
    correct_name = correct_title[0]

    if (title_year) in org_list:
        i = org_list.index(title_year) # finds the index of the title the user is looking for in org_list so it can be matched with the one in the parsed_response
        id = sr[i]["imdbID"] 

    # make another request to match ids
    parsed_response = get_response_2(id)

    session["parsed_response"] = parsed_response

    title_name = parsed_response["Title"]
    release_year = parsed_response["Year"]
    genre = parsed_response["Genre"]
    director = parsed_response["Director"]
    cast = parsed_response["Actors"]
    summary = parsed_response["Plot"]
    rating = parsed_response["Ratings"][0]["Value"]

    url = youtube_search(title_name)

    youtube_id = url.replace("https://www.youtube.com/watch?v=","")

    df = pd.read_csv("dataset.csv")
    features = ['keywords', 'cast', 'genres', 'director']
    for feature in features:
        df[feature] = df[feature].fillna('')
    df["combined_features"] = df.apply(combine_features, axis=1)
    while True:
        try:
            movie_index = get_index_from_title(df, correct_name)
            cv = CountVectorizer() 
            count_matrix = cv.fit_transform(df["combined_features"])
            cosine_sim = cosine_similarity(count_matrix)
            similar_movies = list(enumerate(cosine_sim[movie_index]))
            sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
            i=0
            get_title = []
            for element in sorted_similar_movies:
                get_title.append(get_title_from_index(df, element[0]))
                i=i+1
                if i>4:
                    print("----------------------------------")
                    break
            break
        except IndexError:
            print("Sorry, we couldn't find any recommendations for that title.")
            print("----------------------------------")
            break
    print(get_title)
    return render_template("movie_info.html", title_year=title_year, title_name=title_name, release_year=release_year, genre=genre, director=director, cast=cast, summary=summary, rating=rating, youtube_id=youtube_id, get_title=get_title)


@movie_routes.route('/movie/to-watch')
def index():

    print("VISITING THE TO-WATCH PAGE")
    ss = SpreadsheetService()
    sheet, movies = ss.get_movies()

    print(f"LISTING TITLES FROM THE '{sheet.title}' SHEET")
    for movie in movies:
        print(" + " + str(movie["ID"]) + ": " + movie["Title"])

    return render_template("to_watch.html", movies=movies, sheet_name=sheet.title, sheet_id= ss.sheet_id)


@movie_routes.route('/movie/to-watch/added', methods=["GET", "POST"])
def add():

    if request.method == "GET":
        ButtonPressed=0
        ButtonPressed += 1
        return render_template("to_watch.html", ButtonPressed = ButtonPressed)
    
    print("VISITING THE TO-WATCH PAGE")
    ss = SpreadsheetService()
    sheet, movies = ss.get_movies()

    parsed_response = session.get("parsed_response", None)
    movie_attributes = parsed_response
    response = ss.create_movie(movie_attributes)

    print("RECEIVED MOVIE ATTRIBUTES")

    print(f"... UPDATED RANGE {response['updatedRange']} ({response['updatedCells']} CELLS)")

    sheet, movies = ss.get_movies()

    print(f"LISTING TITLES FROM THE '{sheet.title}' SHEET")
    for movie in movies:
        print(" + " + str(movie["ID"]) + ": " + movie["Title"])
        
    flash(f"Title '{movie['Title']}' created successfully!", "warning")
    
    return render_template("to_watch.html", movies=movies, sheet_name=sheet.title, sheet_id= ss.sheet_id)


@movie_routes.route('/movie/to-watch/deleted', methods=["GET", "POST"])
def delete():

    # code so that it leads to this page if delete option is selected?
    if request.method == "GET":
        ButtonPressed=0
        ButtonPressed += 1
        return render_template("to_watch.html", ButtonPressed = ButtonPressed)

    print("VISITING THE TO-WATCH PAGE")
    ss = SpreadsheetService()
    sheet, movies = ss.get_movies()

    # need to ask for user to enter movie_id they wish to delete on html page, idk how to do this
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
            print("The movie associated with this id does not exist in this list. Sorry!") # also need to return an error page...?
            break

    sheet, movies = ss.get_movies()

    print(f"LISTING TITLES FROM THE '{sheet.title}' SHEET")
    for movie in movies:
        print(" + " + str(movie["ID"]) + ": " + movie["Title"])

    flash(f"Title '{movie['Title']}' deleted successfully!", "warning")
    
    return render_template("to_watch.html", movies=movies, sheet_name=sheet.title, sheet_id= ss.sheet_id)

@movie_routes.route('/movie/to-watch/listcleared', methods=["GET", "POST"])
def clear():

    # code so that it leads to this page if clear list option is selected?
    if request.method == "GET":
        ButtonPressed=0
        ButtonPressed += 1
        return render_template("to_watch.html", ButtonPressed = ButtonPressed)

    ss = SpreadsheetService()
    sheet, movies = ss.get_movies()

    doc = self.client.open_by_key(self.sheet_id)
    worksheet = doc.worksheet(self.sheet_name)
    worksheet.resize(rows=1)
    worksheet.resize(rows=30)

    sheet, movies = ss.get_movies()

    print("CLEARING LIST...")

    flash("The to-watch list has been cleared!", "warning")

    return render_template("to_watch.html", movies=movies, sheet_name=sheet.title, sheet_id=ss.sheet_id)