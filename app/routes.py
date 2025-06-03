from flask import render_template, request, redirect, url_for, flash
from app import app
from app.forms import MovieSearchForm
from app.models import search_movies, get_all_genres

@app.route('/', methods=['GET', 'POST'])
def home():
    form = MovieSearchForm()
    db_genres = get_all_genres()
    form.genres.choices = [(g['genre_id'], g['name']) for g in db_genres]
    
    movies = []
    if form.validate_on_submit():
        criteria = {
            'title': form.title.data,
            'actor': form.actor.data, 
            'genres': form.genres.data,
            'min_runtime': form.min_runtime.data,
            'max_runtime': form.max_runtime.data,
            'min_release_year': form.min_release_year.data,
            'max_release_year': form.max_release_year.data,
            'min_rank': form.min_rank.data,
            'max_rank': form.max_rank.data,
        }
        # Filter out None or empty string values to avoid issues in the query
        active_criteria = {k: v for k, v in criteria.items() if v}
        
        movies = search_movies(active_criteria)
        if not movies:
            flash('No movies found matching your criteria.', 'info')
        return render_template('results.html', movies=movies, title="Search Results")
        
    return render_template('home.html', title='What to Watch - Search', form=form)

# You might want a separate route for results if the home page gets too complex
# @app.route('/results')
# def results():
#     # This would be called by redirecting from home after search
#     # You'd need to pass search results, perhaps via session or query params (less ideal for complex criteria)
#     movies_data = [] # Get this from somewhere
#     return render_template('results.html', movies=movies_data, title="Search Results")