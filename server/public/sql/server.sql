-- **************************************************************************************
-- SQLITE3 file for Doxudio Server Side
-- Spring 2025
-- AUTH: Luhar, Priyanshu pluhar@csub.edu
-- DATE: May 12, 2025

-- **************************************************************************************
-- TABLES

create table if not exists person (
    user_id integer primary key autoincrement,
    uname text not null unique,    
    fname text not null,
    lname text not null,
    hash text not null
);

create table if not exists book (
    book_id integer primary key autoincrement,
    title text not null,
    author text not null,
    published date not null,
    abstract text not null,
    isbn10 text not null,
    isbn13 text not null,
    coverpath text
);

create table if not exists shared (
    transaction_id integer primary key autoincrement,
    book_id integer,
    sender_id integer,
    receiver_id integer,
    temp_filepath text not null,
    time timestamp default current_timestamp,
    foreign key (book_id) references book(book_id) on update cascade on delete set null,
    foreign key (sender_id) references person(user_id) on update cascade on delete set null,
    foreign key (receiver_id) references person(user_id) on update cascade on delete set null
);

create table if not exists review (
    review_id integer primary key autoincrement,
    book_id integer,
    reviewer_id integer,
    rating integer not null,
    content text not null,
    foreign key (book_id) references book(book_id) on update cascade on delete set null,
    foreign key (reviewer_id) references person(user_id) on update cascade on delete set null
);

create table if not exists library (
    library_id integer primary key autoincrement,
    name text not null,
    creator_id integer not null,
    num_books integer default 0,
    started timestamp default current_timestamp,
    foreign key (creator_id) references person(user_id) on update cascade on delete set null
);

create table if not exists belongs (
    library_id integer,
    book_id integer,
    added_on date,
    foreign key (library_id) references library(library_id) on update cascade on delete set null,
    foreign key (book_id) references book(book_id) on update cascade on delete set null
);
