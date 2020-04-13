## Show information about a movie using omdb api ##

import requests
import argparse

def how_to_use():
    scriptName = __file__.split("/")[-1]
    usage = "python %s" % (scriptName + " [MOVIE_NAME]\n")
    return usage

def main():
    parser = argparse.ArgumentParser(description="show movie information", usage=how_to_use())
    parser.add_argument("movieName", nargs="*", help=argparse.SUPPRESS)

    args = parser.parse_args()
    movieName = args.movieName

    if (movieName == None):
        print("usage: ", how_to_use())
        exit()

    api_key = "YOUR_API_KEY"
    api_url = "http://www.omdbapi.com/?apikey=%s&t=%s" % (api_key, movieName)

    try:
        req = requests.get(url=api_url).json()

        title = req["Title"]
        year = req["Year"]
        duration = req["Runtime"]
        genre = req["Genre"]
        director = req["Director"]
        actors = req["Actors"]
        plot = req["Plot"]
        imdbScore = req["Ratings"][0]["Value"]

        print("\nTitle: %s\nYear: %s\nDuration: %s\nGenre: %s\nDirector: %s\nActors: %s\nPlot: %s\nIMDB Rating: %s\n" % (title, year, duration, genre, director, actors, plot, imdbScore))

    except:
        print("Could not find the movie")
        exit()


if (__name__ == "__main__"):
    main()