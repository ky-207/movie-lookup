# web_app/routes/movie_routes.py

from flask import Blueprint, render_template, request, session

from app.search_service import get_response, get_response_2, print_sr, title_except, youtube_search


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

    title_name = parsed_response["Title"]
    release_year = parsed_response["Year"]
    genre = parsed_response["Genre"]
    director = parsed_response["Director"]
    cast = parsed_response["Actors"]
    summary = parsed_response["Plot"]
    rating = parsed_response["Ratings"][0]["Value"]

    url = youtube_search(title_name)

    youtube_id = url.replace("https://www.youtube.com/watch?v=","")

    return render_template("movie_info.html", title_year=title_year, title_name=title_name, 
    release_year=release_year, genre=genre, director=director, cast=cast, summary=summary, rating=rating, youtube_id=youtube_id)