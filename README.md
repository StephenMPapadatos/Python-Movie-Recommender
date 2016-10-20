# Python-Movie-Recommender
Python program that recommends movies to you using Collaborative Filtering and Pearson Coefficient.

A project for Info Retrieval and Web Search. We created a movie recommender program and used both the <a href="https://www.omdbapi.com/">OMDB</a> API and <a href="https://movielens.org/">Movie Lens</a>. 

OMDB allowed us to acquire formatted names for each movie as it pairs the IMDB movie ID and real movie title together.

With movie lens, we parsed two files. The first file gave us user ratings which allowed us to use them as a database to compare to our current user. The database contains 718 unique users, and 100235 movie ratings in total. Since there are so many movie ratings, most movies that the user rates will be compared with many other users. The second file linked the ratings to the movie, using the imdb movie ID as explained above. 

In order to recommend movies to the user we implemented Pearson Similarity Correlation to compute the similarity score between the current user and the users in the database. We then took all users who have positive similarity scores and applied the User-Based Collaborative Filtering method in order to calculate the predicted ratings for movies that the user has not seen yet. If the predicted rating is higher than 4, it will be recommended to the user.
