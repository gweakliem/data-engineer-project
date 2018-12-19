create database movies_metadata if not exists;

create table movies_metadata.movies as
  (id int,
  revenue integer,
  title varchar,
  status varchar,
  release_year varchar ,
  popularity double,
  budget varchar );

create table movies_metadata.genres as
  (id int,
   name varchar);

create table movies_metadata.production_companies as
  (id int,
   name varchar);

create table movies_metadata.movie_genres as
  (movie_id int,
   genre_id int);

create table movies_metadata.movie_production_companies as
  (movie_id int,
   pc_id varchar);