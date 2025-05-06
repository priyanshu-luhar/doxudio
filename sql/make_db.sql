create table if not exists person (
    userID integer primary key autoincrement,
    email text not null,
    hash text not null,
    fname text not null default "Secretariat",
    lname text,
    dob date not null
);


create table if not exists document (
    docID integer primary key autoincrement,
    addedBy integer,
    filetype text not null,
    filepath text not null,
    sizeofdoc integer,
    bookmark integer,
    created datetime default CURRENT_TIMESTAMP,
    modified datetime default CURRENT_TIMESTAMP
);


create table if not exists book (
    bookID integer primary key autoincrement,
    title text not null,
    author text not null,
    published integer not null,
    isbn text not null,
    docID integer    
);


create table if not exists genre (
    genreID integer primary key autoincrement,
    genre text unique
);


