''' Objective:To create a movie recommendation system which asks the user for their
favourite movie name and recommend similar movies (content based system) 
Dataset used: moviedata.csv '''
#Data collection
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
data=pd.read_csv('D:/bittorrent downloads/moviedata.csv')

#Data interpretation
#Check first 5(default) values in dataset
print(data.head())

#Now we have to choose the features that would help us to recommend similar movies.
features = ['keywords','cast','genres','director','tagline']

#Data cleaning
#In some columns from the list features, there NaN values so we fill them with empty string
for column in features:
    data[column]=data[column].fillna('')

''' Now our task is to combine these features into a single column or in other words
we have to combine the strings all of these columns for a particular row and put it 
in a new column called combined_features '''
def combine_feature(row):
    return row['keywords']+' '+row['cast']+' '+row['genres']+' '+row['director']+' '+row['tagline']

data['combined_features']=data.apply(combine_feature,axis=1) #column creation

''' Now we define two helping functions. One of the functions returns the title of a movie given the 
index and the other function does the opposite. When the title is entered by the user,
they might make spelling mistakes. So, we make use of the functions provided in difflib
library in order to get close matches '''

def title_from_index(index):
    return data[data.index == index]["title"].values[0]
def index_from_title(title):
    title_list = data['title'].tolist()
    common = difflib.get_close_matches(title, title_list, 1)
    titlesim = common[0]
    return data[data.title == titlesim]["index"].values[0]

''' In order to compare the movies based on combined_features column first we create 
a cosine similarity with a count matrix. Then we ask user for his favourite movie and use the
index_from_title function to get the index. Using this index we take out the corresponding
row from the cosine_sim and enumerate it and make it a list. We then sort this list of tuples
based on the value of the second element in each tuple. (The second element gives a measure
of how similar a movie x is to a movie y) and at the last we make use of the indexes present
as the first element in each tuple to print the titles of 50 movies which are similar to 
the movie entered by the user'''

#object of CountVectorizer class
cv=CountVectorizer()
count_matrix=cv.fit_transform(data['combined_features'])
cosine_sim=cosine_similarity(count_matrix)

user_movie=input('Enter your facvourite movie:')
movie_index=index_from_title(user_movie)

similar_movies=list(enumerate(cosine_sim[movie_index]))
similar_movies_sorted=sorted(similar_movies,key=lambda x:x[1],reverse=True)
i=1
print("Other movies you might be interested in:-")
for element in similar_movies_sorted:
    print(f'{i}. {title_from_index(element[0])}')
    i=i+1
    if(i>50):
        break