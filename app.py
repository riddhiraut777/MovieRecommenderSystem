import streamlit as st
import pickle
import pandas as pd
import requests


st.title('Movie Recommender System')

#Saving the pre-processed dataframe and similarity matrix into below variables
movies_list_df=pickle.load(open('movies.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

# Saving all the titles in form of array
movie_title_names=movies_list_df['title'].values
# print(movies_list_df['title'].values)
# print(type(movies_list_df['title'].values))
# print((movies_list_df))

selected_movie_name = st.selectbox(
    "Select The Movie Name",
    movie_title_names)

st.write("You selected:", selected_movie_name)


# Defining a recommend function that will recommend movies based on the one selected by the user
def recommend(movie):
    movie_index= movies_list_df[movies_list_df['title']== movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key= lambda x:x[1])[1:6]

    recommend_movies=[]
    recommend_movies_poster=[]
    for i in movies_list:
        movie_id=movies_list_df.iloc[i[0]].id
        # Fetch poster from API based on above movie id
        recommend_movies_poster.append(fetch_poster(movie_id))
        print(i)
        recommend_movies.append(movies_list_df.iloc[i[0]].title)
    return recommend_movies,recommend_movies_poster

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=612bbf9abecef43933faa4371cce852c'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']

# fetch_poster(65)


if st.button("Recommend"):
    titles,posters= recommend(selected_movie_name)
    # print(titles,posters)


    tab1, tab2, tab3,tab4,tab5 = st.tabs(titles)
    # print(st.tabs(titles))
    with tab1:
        st.header(titles[0])
        st.image(posters[0])

    with tab2:
        st.header(titles[1])
        st.image(posters[1])

    with tab3:
        st.header(titles[2])
        st.image(posters[2])

    with tab4:
        st.header(titles[3])
        st.image(posters[3])

    with tab5:
        st.header(titles[4])
        st.image(posters[4])