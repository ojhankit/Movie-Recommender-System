import streamlit as st
import pickle
import pandas as pd
import requests

'''
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=&language=en-US')

    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
'''
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=")
    
    if response.status_code != 200:
        print(f"Failed to fetch data for movie_id: {movie_id}")
        return None

    data = response.json()
    poster_path = data.get('poster_path')

    if not poster_path:
        print(f"'poster_path' not found for movie_id: {movie_id}")
        return None

    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

    
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,
                         key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = i[0]
        # get poster from api
        poster = fetch_poster(movie_id)
        title = movies.iloc[movie_id].title

        recommended_movies.append(title)
        recommended_movies_posters.append(poster)
    return recommended_movies,recommended_movies_posters

movies_list = pickle.load(open('model.pkl','rb'))
movies_dict = pickle.load(open('movies.pkl','rb'))
#similarity = pickle.load(open('similarity.pkl','rb'))

movies = pd.DataFrame(movies_dict)
movies_list = movies_list['title'].values

st.title("Movie Recommender System")

selected_movie = st.selectbox(
    'Select the Movie',
    movies_list
)

if st.button('Recommend'):
    moviename,poster = recommend(selected_movie)
    # for i in moviename:
    #     st.write(i)

    # col1,col2,col3,col4,col5 = st.columns(5)

    # with col1:
    #     st.header(moviename[0])
    #     st.image(poster[0])
    # with col1:
    #     st.header(moviename[0])
    #     st.image(poster[0])
    # with col1:
    #     st.header(moviename[0])
    #     st.image(poster[0])
    # with col1:
    #     st.header(moviename[0])
    #     st.image(poster[0])
    # with col1:
    #     st.header(moviename[0])
    #     st.image(poster[0])

    cols = st.columns(len(moviename))
    for i in range(len(moviename)):
        with cols[i]:
            st.header(moviename[i])
            st.image(poster[i])
