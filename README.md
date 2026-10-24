# CineMatch 
CineMatch is a movie recommendation web app. Pick up to 5 movies you like, and it suggests similar movies based on plot, genre, cast and director.

## Features
- Content-based movie recommendations
- Match percentage for each suggestion
- Movie posters fetched from the TMDB API
- Simple web interface built with Streamlit

## How it works
- Movie details (plot, genre, cast, director) are converted into numbers using **TF-IDF**.
- **Cosine similarity** finds the movies closest to your picks.

## Tech used
Python, Pandas, NumPy, SciPy, scikit-learn, Streamlit, TMDB API

## Run it on your computer
1. Install the requirements: `pip install -r requirements.txt`
2. Create a file `.streamlit/secrets.toml` and add your TMDB API key:
   `TMDB_KEY = "your_api_key"`
3. Start the app: `streamlit run app.py`

## Credit
This product uses the TMDB API but is not endorsed or certified by TMDB.
