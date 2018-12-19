# this script imports new data from the movies metadata CSV into the master database.
from csv import *
import ast
import sys

def parse_lousy_json(str, key):
    '''
    Json encoding in the CSV is sometimes bad, this routine tries to hide this
    :param str:
    :return:
    '''
    try:
        if str is not None:
            return ast.literal_eval(str)
    except SyntaxError:
        print("Bad JSON encountered in {}: {}",key, str, file=sys.stderr)
        return None

movies = []
genres = {}
production_companies = {}
movie_genres = []
movie_pcs = []
with open('./data/movies_metadata.csv') as csvfile:
    r = DictReader(csvfile, delimiter=',')
    for row in r:
        movie = {}
        columns = ['id','revenue','title','status','release_date','popularity','budget']
        for col in columns:
            movie[col] = row[col]
        mg = parse_lousy_json(row['genres'],row['id'])
        if mg:
            genres.update(dict((x['id'], x['name']) for x in mg))
            movie_genres.extend([(movie['id'],m['id']) for m in mg])

        mp = parse_lousy_json(row['production_companies'],row['id'])
        if mp:
            production_companies.update(dict((x['id'], x['name']) for x in mp))
            movie_pcs.extend([(movie['id'],x['id']) for x in mp])

        if movie['release_date'] is not None:
            movie['release_year'] = movie['release_date'][0:4]
            movies.append(movie)
        else:
            print("No release date indicated for movie " + movie['id'], file=sys.stderr)
            # we can't really key without a release date / year, so pass on this movie

# now we have a trimmed down dataset, output the INSERTs to recreate as RDBMS

# TODO: lazy string escaping, fix
for m in movies:
    print("INSERT INTO movies (id,revenue,title,status,release_year,popularity,budget) VALUES ('{id}',{revenue},'{title}','{status}','{release_year}',{popularity},{budget});".format(**m))

for id,name in genres.items():
    print(f"INSERT INTO genres (id,name) VALUES ({id},'{name})'")

for id, name in production_companies.items():
   print(f"INSERT INTO production_companies (id,name) VALUES ({id},'{name}')")

for movie_id, genre_id in movie_genres:
    print(f"INSERT INTO movie_genres (movie_id,genre_id) VALUES ({movie_id},{genre_id})")

for movie_id, pc_id in movie_pcs:
    print(f"INSERT INTO movie_production_companies (movie_id,pc_id) VALUES ({movie_id},{pc_id})")