import omdb
import json
import csv
import math
from operator import itemgetter
from collections import OrderedDict
import random

#Row[0] is userID, Row[1] is movieID, Row[2] is Rating
movie_user_read = csv.reader(open("ratings.csv","rb"))
#Row[0] is movieID, Row[1] is imdbID which we use
movie_imdb_links = csv.reader(open("links.csv","rb"))
#Create dictionary with movieID as key, and userIDs as values and ratings
movieid_dict = dict()
#Create dictionary with imdbID as key, and movieID as values
movie_imdb_ids = dict()
#Create dictionary with movie ID as key, and imdbID as values
movie_id_ids = dict()
#Create dictionary with userIDs as keys and movieID and Ratings as values
user_movies_rated = dict()
#Create dictionary with movies the user rated as the key, and rating as the values
my_movies_rated = dict()
#Create dictionary with user ID as key, and the numerator as value
key_numerator_pair = dict()
#Create dictionary with user ID as key, and denom as value
key_denom_pair = dict()
#Create dictionary with user ID as key, and similarity as value
key_sim_value = dict()

#Traverse the CSV Ratings file and build movie_user_read dictionary
#Also builds the user_movies_rated dictionary at the same time to save speed
for row in movie_user_read:
    if row[1] in movieid_dict:
        #Append the userID to the current list of IDs if the movie has been rated
        movieid_dict[row[1]].append(row[0] + ":" + row[2])
    else:
        #Create new entry for this movie
        movieid_dict[row[1]] = [row[0] + ":" + row[2]]
    if row[0] in user_movies_rated:
        #Appends the movies the user rated to the ones they previously rated
        user_movies_rated[row[0]].append(row[1] + ":" + row[2])
    else:
        #Creates new entry for this user
        user_movies_rated[row[0]] = [row[1] + ":" + row[2]]
        
#Traverse the ratings file and build movie_imdb_links
for row in movie_imdb_links:
    movie_imdb_ids[row[1]] = row[0]
    movie_id_ids[row[0]] = row[1]


#Test while loop
searching = True
other_user_list = []
my_total_rating = 0
movie_list = random.sample(movie_id_ids, 500)
i = 0
j = 0
while(searching):
    i += 1
    #Ask user for which movie they'd like to search
    current_id = "tt" + movie_id_ids[movie_list[i]]
    res = omdb.request(i=current_id)
    json_content = res.content
    parsed_json = json.loads(json_content)
    movie_title = parsed_json['Title']
    movie_id = movie_list[i]
    print movie_title
    
    #Ask user for the rating on the movie they rated
    movie_rating = raw_input('Rating for the movie(1-5 decimals are ok 0 if you have not watched the movie)')
    if movie_rating == '0':
        print "Well give you another movie now"
    else:
        my_total_rating += float(movie_rating)
        j += 1
        #Prints movie Rating
        print movie_rating
        my_movies_rated[movie_id] = movie_rating
    #if they don't exit the while loop
    if(j == 10):
        searching = False
        
#Print the my_movies_rated dictionary, contains movie id and ratings for this user
i = 0
for key in my_movies_rated:
    i += 1
    #Get the users who rated the movie
    users_rating_movie = movieid_dict.get(key)
    #Goes through each user who rated the movie
    for user in users_rating_movie:
        #split the user into a user and a rating
        user_rating_split = user.split(':')
        #print the user, movie title and the rating for the specific movie for every user
        if user_rating_split[0] in other_user_list:
            print "No duplicates"
        else:
            other_user_list.append(user_rating_split[0])
            

#Prints each movie:rating one by one for each individual user that has rated the movie searched
for individual_user in other_user_list:
    same_movies_rated = dict()
    my_average = 0
    amount_of_movies_rated = 0
    user_average = 0
    user_split_movies = user_movies_rated[individual_user]
    my_denom = 0
    their_denom = 0
    for movie in user_split_movies:
        movie_rating_split = movie.split(':')
        if movie_rating_split[0] in my_movies_rated:
            amount_of_movies_rated += 1
            user_average += float(movie_rating_split[1])
            same_movies_rated[movie_rating_split[0]] = movie_rating_split[1]
    for key in same_movies_rated:
        their_total_average = float(user_average/len(same_movies_rated))
        my_total_average = float(my_total_rating/len(my_movies_rated))
        my_a = float(my_movies_rated[key])
        their_a = float(same_movies_rated[key])
        my_denom += math.pow((my_a - my_total_average) ,2)
        their_denom += math.pow((their_a - their_total_average) ,2)
        if their_denom == 0:
            their_denom = 1
        if my_denom == 0:
            my_denom = 1
        key_denom_pair[individual_user] = (my_denom * their_denom)
        if individual_user in key_numerator_pair:
            key_numerator_pair[individual_user] += ((my_a - my_total_rating)*(their_a - their_total_average))
        else:
            key_numerator_pair[individual_user] = ((my_a - my_total_rating)*(their_a - their_total_average))

for key in key_numerator_pair:
    key_sim_value[key] = (key_numerator_pair[key] / math.sqrt(float(key_denom_pair[key])))
for key in key_sim_value:
    print key + " " + str(key_sim_value[key])
sorted_sim_values = OrderedDict(sorted(key_sim_value.items(), key=itemgetter(1)))

print "Test start here"
for key in sorted_sim_values:
    print key + " " + str(sorted_sim_values[key])


intersection = []
people = []
prediction = dict()
user_mult = 0.0
count = 0
# 1/(sum of all user scores above .5)
for key in sorted_sim_values:
        if (sorted_sim_values[key] > 0):
                people.append(key)
                this_user = user_movies_rated[key]
                for t in this_user:
                    ta = t.split(':')
                    if (ta[0] in intersection):
                        print count
                        count += 1
                    else:
                        intersection.append(ta[0])


predict_two = 0


for movie in intersection:
        for person in people:
                for each in user_movies_rated[person]:
                        e = each.split(':')
                        if e[0] == movie:
                                user_mult += float(sorted_sim_values[person])
                                predict_two += (float(sorted_sim_values[person]) * float(e[1]))
        predict_one = 1/user_mult
        prediction[movie] = predict_two * predict_one
        predict_two = 0
        user_mult = 0


for p in prediction:
    if prediction[p] > 4.0:
        valid_imdb_id = "tt" + movie_id_ids[p]
        res = omdb.request(i = valid_imdb_id)
        json_content = res.content
        parsed_json = json.loads(json_content)
        final_title = parsed_json['Title']
        print final_title + " Recommended Rating " + str(prediction[p])

#important_individual = user_movies_rated[sorted_sim_values.keys()[-1]]
#print "Movies you might like"
#for important_individuals_movies in important_individual:
#    important_individual_split = important_individuals_movies.split(':')
#    if float(important_individual_split[1]) > 4.0:
#        valid_imdb_id = "tt" + movie_id_ids[important_individual_split[0]]
 #       res = omdb.request(i = valid_imdb_id)
  #      json_content = res.content
   #     parsed_json = json.loads(json_content)
    #    final_title = parsed_json['Title']
     #   print final_title
        

        
#Need to get the all of the users who rated the same movies as User 1, this is done      above but all needs to be done in a loop
#Then get all of the movies that each of these users rated, using user_movies_rate()     dictionary
#Calculate the similarity between User 1 and every other user with every movie they have rated together.


