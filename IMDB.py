import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

url = "https://www.imdb.com/search/title/?groups=top_1000"
results = requests.get(url)
soup = BeautifulSoup(results.text, "html.parser")
titles = []
years = []
time = []
imdb_ratings = []
genre = []
votes = []

movie_div = soup.find_all("div", class_="lister-item mode-advanced")
for movieSection in movie_div:
    name = movieSection.h3.a.text
    titles.append(name)
    year = movieSection.h3.find("span", class_="lister-item-year").text
    years.append(year)
    ratings = movieSection.strong.text
    imdb_ratings.append(ratings)
    category = movieSection.find("span", class_="genre").text.strip()
    genre.append(category)
    runTime = movieSection.find("span", class_="runtime").text
    time.append(runTime)
    nv = movieSection.find_all("span", attrs={"name": "nv"})
    vote = nv[0].text
    votes.append(vote)
movies = pd.DataFrame(
    {
        "Movie": titles,
        "Year": years,
        "RunTime": time,
        "imdb": imdb_ratings,
        "Genre": genre,
        "votes": votes,
    }
)

# cleaning
movies["Year"] = movies["Year"].str.extract("(\\d+)").astype(int)
movies["RunTime"] = movies["RunTime"].str.replace("min", "minutes")
movies["votes"] = movies["votes"].str.replace(",", "").astype(int)

print(movies)
movies.to_csv(r"C:\Users\Aleti Sunil\Downloads\movies.csv", index=False, header=True)
