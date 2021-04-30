DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    artist TEXT NOT NULL, 
    song TEXT NOT NULL,  
    duration TEXT NOT NULL, 
    album TEXT NOT NULL,
    year INTEGER NOT NULL, 
    label TEXT NOT NULL,
    genre TEXT NOT NULL,
    cover TEXT
);
