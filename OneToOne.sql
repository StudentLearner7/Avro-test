CREATE TABLE user (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);


CREATE TABLE user_profile (
    profile_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    bio TEXT,
    user_id INT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
