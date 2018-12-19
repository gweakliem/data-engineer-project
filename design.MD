# System Design

Overall system design for the movie stats database is built around the following assumptions: 
* New data files are received monthly
* The system should be scalable

## Data Transformation

The program provided in `import_movies.py` represents the import process. The output of this process is a series of SQL 
`INSERT` statements that populate the database with the new dataset.

Given that data is received monthly, it's undefined whether the data represent a full update or an incremental update. Given 
the size of the data, in the event of a full update, I'd recommend a blue/green deployment scheme where the new data is 
loaded to a secondary database and then the new data set is taken live once it is checked out. 

## Data Storage

I decided to use a relational model for the movie database. While aspects of the data lend themselves to a denormalized 
store, the data is not that large, well within the capacity of the available RDBMS systems, even given a large growth 
rate.  

## Data Serving

The projections proposed will be served via an HTTP REST API as HTTP GET requests. Regarding the design concern about 
scalability, I see 2 issues with scaling; the size of the data being maniuplated and request volume. Given that we have an 
existing dataset of ~ 46000 rows, even at 10x growth the data is on the order of a half-million rows, well within the limits 
of a medium sized dataset. 

We should also consider the size of the projection; however this is not large given that the representation is over 
a list of production companies over a range of dates - neither number is extremely large and while the potential matrix 
is large, many production companies produce movies over a limited range of years, so the matrix is actually sparse.  

This turns our attention to request volume. I believe that volume needs could be accomodated using caching, where these 
projections are computed on-demand and cached. Given that the data is updated monthly, I do not believe that the compute 
cycles required would be excessive. Essentially, we have 2 projections (Production Company Details and Movie Genre Details) 
and these could be computed in a timely manner on-demand, or precomputed as part of the ingestion process described above.