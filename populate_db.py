import csv
import psycopg2
import re
import os

# --- CSV File ---
CSV_FILE_PATH = 'What_to_Watch_DB.csv'

def parse_movie_title_and_year(title_str):
    match = re.search(r'(.+?)\s*\((\d{4})\)$', title_str)
    if match:
        title = match.group(1).strip()
        year = int(match.group(2))
        return title, year
    # Fallback if year is not in title or format is different
    # Try to find year if it's part of something like (2017/I)
    match_alternative = re.search(r'\((\d{4})[/I]*\)', title_str)
    if match_alternative:
        year = int(match_alternative.group(1))
        # Remove the year part from title for cleaner title
        title = re.sub(r'\s*\(\d{4}[/I]*\)$', '', title_str).strip()
        return title, year
    return title_str.strip(), None # No year found or unable to parse

def get_or_create_genre_id(cursor, genre_name):
    genre_name = genre_name.strip()
    cursor.execute("SELECT genre_id FROM genres WHERE name = %s", (genre_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO genres (name) VALUES (%s) RETURNING genre_id", (genre_name,))
        return cursor.fetchone()[0]

def get_or_create_person_id(cursor, person_name):
    person_name = person_name.strip()
    cursor.execute("SELECT person_id FROM persons WHERE name = %s", (person_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO persons (name) VALUES (%s) RETURNING person_id", (person_name,))
        return cursor.fetchone()[0]

def main():
    conn = None
    try:
        conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
        )

        cur = conn.cursor()
        print("Successfully connected to the database.")

        with open(CSV_FILE_PATH, mode='r', encoding='utf-8-sig') as file: # utf-8-sig to handle BOM
            csv_reader = csv.DictReader(file, delimiter=';')
            for row_num, row in enumerate(csv_reader):
                try:
                    movie_db_id = int(row['ID'])
                    votes = int(row['Votes']) if row['Votes'] else None
                    rank = int(row['Rank']) if row['Rank'] else None
                    
                    original_title_field = row['Title']
                    parsed_title, release_year = parse_movie_title_and_year(original_title_field)

                    runtime_str = row['Runtime (min)']
                    runtime = int(runtime_str) if runtime_str and runtime_str.isdigit() else None
                    
                    primary_genres_str = row['Primary genre(s)']
                    main_cast_str = row['Main cast']

                    # Insert movie
                    cur.execute("""
                        INSERT INTO movies (movie_id, title, release_year, runtime, rank, votes)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (movie_id) DO NOTHING;
                    """, (movie_db_id, parsed_title, release_year, runtime, rank, votes))

                    # Insert genres and movie_genres
                    if primary_genres_str:
                        genres = [g.strip() for g in primary_genres_str.split(',') if g.strip()]
                        for genre_name in genres:
                            genre_id = get_or_create_genre_id(cur, genre_name)
                            cur.execute("""
                                INSERT INTO movie_genres (movie_id, genre_id)
                                VALUES (%s, %s) ON CONFLICT DO NOTHING;
                            """, (movie_db_id, genre_id))
                    
                    # Insert actors (persons) and movie_actors
                    if main_cast_str:
                        actors = [a.strip() for a in main_cast_str.split(';') if a.strip()] # Assuming semicolon for actors
                        for actor_name in actors:
                            person_id = get_or_create_person_id(cur, actor_name)
                            cur.execute("""
                                INSERT INTO movie_actors (movie_id, person_id)
                                VALUES (%s, %s) ON CONFLICT DO NOTHING;
                            """, (movie_db_id, person_id))
                
                except ValueError as e:
                    print(f"Skipping row {row_num + 2} due to ValueError: {e}. Data: {row}")
                    continue
                except Exception as e:
                    print(f"Error processing row {row_num + 2}: {e}. Data: {row}")
                    conn.rollback() # Rollback transaction for this row
                    continue


        conn.commit()
        print("Data loaded successfully!")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
    except FileNotFoundError:
        print(f"Error: The file {CSV_FILE_PATH} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    main()