import streamlit as st 
import pickle
import requests
import streamlit.components.v1 as components
import pandas as pd
import os

api_key = os.getenv("api_key")


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        data = requests.get(url)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path')
        if not poster_path:
            return None
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None

movies = pickle.load(open("/Users/vinay_j1548/Desktop/ai-movie-suggestor/movies_list.pkl" , 'rb'))
similar = pickle.load(open("/Users/vinay_j1548/Desktop/ai-movie-suggestor/similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
]

imageCarouselComponent(imageUrls=imageUrls, height=200)
select_value = st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in the dataset.")
        return [], []
    
    # Debugging: Print the index and check if it is valid
    st.write(f"Movie index: {index}")
    
    if index >= len(similar):
        st.error("Index out of range in similarity matrix.")
        return [], []
    
    distance = sorted(list(enumerate(similar[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(select_value)
    if movie_name and movie_poster:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(movie_name[0])
            st.image(movie_poster[0])
        with col2:
            st.text(movie_name[1])
            st.image(movie_poster[1])
        with col3:
            st.text(movie_name[2])
            st.image(movie_poster[2])
        with col4:
            st.text(movie_name[3])
            st.image(movie_poster[3])
        with col5:
            st.text(movie_name[4])
            st.image(movie_poster[4])