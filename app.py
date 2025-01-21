from flask import Flask, render_template, request
import pickle
import pandas as pd
import difflib

# Load the pickled model and vectorizer
with open('movie_similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Load movie data
data = pd.read_csv('movies.csv')

# Create a list of movie titles for similarity matching
title_list = data['title'].tolist()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the movie name from the form
    movie_name = request.form['movie_name']
    
    # Find closest match to the movie name
    close_matches = difflib.get_close_matches(movie_name, title_list)
    if not close_matches:
        return render_template('index.html', error="No matching movie found. Try again!")
    
    single_match = close_matches[0]
    index_of_movie = data[data.title == single_match]['index'].values[0]

    # Get similarity scores
    similarity_score = list(enumerate(similarity[index_of_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    # Get top 10 recommendations
    recommended_movies = []
    i = 1
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = data[data.index == index]['title'].values[0]
        if i < 11:  # Top 10 recommendations
            recommended_movies.append(f"{i}. {title_from_index}")
            i += 1
        else:
            break

    return render_template('index.html', movie_name=movie_name, recommended_movies=recommended_movies)

if __name__ == '__main__':
    app.run(debug=True)
