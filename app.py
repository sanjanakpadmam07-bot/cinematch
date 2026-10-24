import os
import html
import requests
import numpy as np
import pandas as pd
import scipy.sparse as sp
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="CineMatch", page_icon="🎬", layout="wide")

with open("style.css", encoding="utf-8") as f:
    st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)


@st.cache_resource
def load():
    titles = pd.read_csv("models/titles.csv")
    X = sp.load_npz("models/tfidf.npz")
    return titles, X


titles, X = load()
idx = pd.Series(titles.index, index=titles.title)


def get_key():
    try:
        return st.secrets["TMDB_KEY"]
    except Exception:
        return os.environ.get("TMDB_KEY")

@st.cache_data(show_spinner=False)
def poster(movie_id):
    key = get_key()
    if not key:
        return None
    try:
        r = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id),
                         params={"api_key": key}, timeout=5).json()
        p = r.get("poster_path")
        return "https://image.tmdb.org/t/p/w300" + p if p else None
    except Exception:
        return None


def recommend(picks, n=10):
    rows = [idx[t] for t in picks]
    profile = np.asarray(X[rows].mean(axis=0))
    scores = cosine_similarity(profile, X).ravel()
    for r in rows:
        scores[r] = -1
    top = scores.argsort()[::-1][:n]
    return [(i, scores[i]) for i in top]


hero = ('<div class="hero"><h1>&#127916; CineMatch</h1>'
        '<p>Pick movies you love and discover what to watch next, '
        'based on plot, genre, cast and director.</p></div>')
st.markdown(hero, unsafe_allow_html=True)

picks = st.multiselect("Pick 1 to 5 movies you like", titles.title.tolist(), max_selections=5)

if st.button("Recommend") and picks:
    st.subheader("Recommended for you")
    recs = recommend(picks)
    for start in range(0, len(recs), 5):
        cols = st.columns(5)
        for col, (i, s) in zip(cols, recs[start:start + 5]):
            img = poster(int(titles.id[i]))
            if img:
                visual = '<img src="' + img + '">'
            else:
                visual = '<div class="placeholder">&#127916;</div>'
            title = html.escape(titles.title[i])
            card = ('<div class="card">' + visual + '<div class="info">'
                    '<div class="title">' + title + '</div>'
                    '<span class="match">' + format(s, ".0%") + ' match</span>'
                    '</div></div>')
            col.markdown(card, unsafe_allow_html=True)

footer = ('<div class="footer">This product uses the TMDB API '
          'but is not endorsed or certified by TMDB.</div>')
st.markdown(footer, unsafe_allow_html=True)