from app import get_db_connection
from psycopg2.extras import DictCursor

def get_all_genres():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT genre_id, name FROM genres ORDER BY name;")
    genres_data = cur.fetchall() # Renamed to avoid conflict
    cur.close()
    conn.close()
    return genres_data

def search_movies(criteria):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)

    base_query = ("SELECT DISTINCT m.movie_id, m.title, m.release_year, m.runtime, m.rank, m.votes, "
                  "STRING_AGG(DISTINCT g.name, ', ') AS genres_agg, " # Aliased to avoid conflict if 'genres' is a key in criteria
                  "STRING_AGG(DISTINCT p.name, ', ') AS actors_agg "  # Aliased
                  "FROM movies m "
                  "LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id "
                  "LEFT JOIN genres g ON mg.genre_id = g.genre_id "
                  "LEFT JOIN movie_actors ma ON m.movie_id = ma.movie_id "
                  "LEFT JOIN persons p ON ma.person_id = p.person_id")
    
    join_clauses_sql = []
    where_clauses_sql = []
    params = [] # Initialize params list

    # --- Parameters for JOIN conditions (must be added to params first if their %s appear first) ---
    if criteria.get('genres'): # list of genre_ids
        for genre_id_selected in criteria['genres']:
            alias = f"mg_filter_{genre_id_selected}"
            join_clauses_sql.append(f"JOIN movie_genres {alias} ON m.movie_id = {alias}.movie_id AND {alias}.genre_id = %s")
            params.append(int(genre_id_selected)) # Add genre_id param

    # --- Parameters for WHERE conditions (and JOINs that don't have parameters in the JOIN itself) ---
    if criteria.get('actor'):
        # These JOINs don't introduce new %s placeholders in the JOIN itself
        join_clauses_sql.append("JOIN movie_actors ma_filter ON m.movie_id = ma_filter.movie_id")
        join_clauses_sql.append("JOIN persons p_filter ON ma_filter.person_id = p_filter.person_id")
        # The %s for actor name is in the WHERE clause
        where_clauses_sql.append("p_filter.name ILIKE %s")
        params.append(f"%{criteria['actor']}%") # Add actor param
    
    if criteria.get('title'):
        where_clauses_sql.append("m.title ILIKE %s")
        params.append(f"%{criteria['title']}%") # Add title param

    # Add other WHERE clause criteria and their params
    if criteria.get('min_runtime'):
        where_clauses_sql.append("m.runtime >= %s")
        params.append(criteria['min_runtime'])
    if criteria.get('max_runtime'):
        where_clauses_sql.append("m.runtime <= %s")
        params.append(criteria['max_runtime'])
    if criteria.get('min_release_year'):
        where_clauses_sql.append("m.release_year >= %s")
        params.append(criteria['min_release_year'])
    if criteria.get('max_release_year'):
        where_clauses_sql.append("m.release_year <= %s")
        params.append(criteria['max_release_year'])
    if criteria.get('min_rank'):
        where_clauses_sql.append("m.rank >= %s")
        params.append(criteria['min_rank'])
    if criteria.get('max_rank'):
        where_clauses_sql.append("m.rank <= %s")
        params.append(criteria['max_rank'])

    # Assemble the final query
    final_query_parts = [base_query]
    if join_clauses_sql:
        final_query_parts.extend(join_clauses_sql)
    
    if where_clauses_sql:
        final_query_parts.append("WHERE " + " AND ".join(where_clauses_sql))

    final_query_parts.append("GROUP BY m.movie_id, m.title, m.release_year, m.runtime, m.rank, m.votes")
    final_query_parts.append("ORDER BY m.rank DESC, m.votes DESC, m.title")
    
    final_query = " ".join(final_query_parts)
    
    # print("SQL Query:", final_query) # For debugging
    # print("Params:", params)       # For debugging

    cur.execute(final_query, tuple(params)) # Params are now in the correct order
    movies = cur.fetchall()
    
    # Rename aggregated columns to match what template expects, if needed
    # This step is important if your template directly uses 'movie.genres' or 'movie.actors'
    processed_movies = []
    for movie_row in movies:
        movie_dict = dict(movie_row) # Convert psycopg2.extras.DictRow to a mutable dict
        if 'genres_agg' in movie_dict:
            movie_dict['genres'] = movie_dict.pop('genres_agg')
        if 'actors_agg' in movie_dict:
            movie_dict['actors'] = movie_dict.pop('actors_agg')
        processed_movies.append(movie_dict)
    
    cur.close()
    conn.close()
    return processed_movies