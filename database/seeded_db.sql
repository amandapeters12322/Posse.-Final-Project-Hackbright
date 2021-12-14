CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    fname VARCHAR(25) NOT NULL,
    lname VARCHAR(25) NOT NULL,
    email VARCHAR(50) UNIQUE,
    phone VARCHAR(12) NOT NULL,
    password VARCHAR(20) NOT NULL,
    start_date VARCHAR(11)
);

INSERT INTO users (fname, lname, email, phone, password, start_date) VALUES ('Amanda','Peters','amanda.nielsen@me.com','715-450-4230','crosby1024','11/01/2021');
INSERT INTO users (fname, lname, email, phone, password, start_date) VALUES ('Ryan','Peters','ryan_d_peters@yahoo.com','610-955-5429','ryan123','11/01/2021');
INSERT INTO users (fname, lname, email, phone, password, start_date) VALUES ('Jasmine', 'Debugger','jdebugs@hotmail.com', '320-887-9901', 'jasmine123', '11/04/2021');
INSERT INTO users (fname, lname, email, phone, password, start_date) VALUES ('John', 'Doe','john_doe@gmail.com','345-664-2210','john123','11/12/2021');
INSERT INTO users (fname, lname, email, phone, password, start_date) VALUES ('Jane','Hacks','jhacks@gmail.com', '555-443-9987', 'jane123', '11/03/2021');



CREATE TABLE guests(
    guest_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    event_id INTEGER REFERENCES events,
    rsvp_attend VARCHAR(12) NOT NULL
);

INSERT INTO guests (guest_id, user_id, event_id, rsvp_attend) VALUES (1, 1, "No response");
INSERT INTO guests (guest_id, user_id, event_id, rsvp_attend) VALUES (2, 2, "No response");
INSERT INTO guests (guest_id, user_id, event_id, rsvp_attend) VALUES (3, 3, "No response");
INSERT INTO guests (guest_id, user_id, event_id, rsvp_attend) VALUES (4, 4, "No response");
INSERT INTO guests (guest_id, user_id, event_id, rsvp_attend) VALUES (5, 5, "No response");




CREATE TABLE events(
    event_id SERIAL PRIMARY KEY,
    host_id INTEGER REFERENCES users,
    event_name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    venue VARCHAR(50) NOT NULL,
    evtdate VARCHAR(10) NOT NULL,
    evttime VARCHAR(9) NOT NULL,
    rsvp_date VARCHAR(10) NOT NULL
);

INSERT INTO events (event_id, host_id, event_name, location, venue, evtdate, evttime, rsvp_date) VALUES (1, 'Christmas Party', '16102 73rd Pl N, Maple Grove, MN', 'Our Home', '12/24/2021', '05:30 PM', '12/12/2021');
INSERT INTO events (event_id, host_id, event_name, location, venue, evtdate, evttime, rsvp_date) VALUES (2, 'New Years Celbration', '2323 Vine Ln, Minneapolis, MN', '134 Place', '12/31/2021', '09:00 PM', '12/10/2021');
INSERT INTO events (event_id, host_id, event_name, location, venue, evtdate, evttime, rsvp_date) VALUES (3, 'My 40th Birthday Party Bash!', '106 Greenfield Rd, Rochester, MN', 'My House', '02/23/2022', '01/30/2022');
INSERT INTO events (event_id, host_id, event_name, location, venue, evtdate, evttime, rsvp_date) VALUES (4, 'Holiday Party', '1225 Candycane Ln, Somewhere in Antarctica', 'North Pole', '12/25/2021', '11/25/2021' );
INSERT INTO events (event_id, host_id, event_name, location, venue, evtdate, evttime, rsvp_date) VALUES (5, 'Thanksgiving', '4872 Shoreview Dr, Maplewood, MN', 'My Parents Home', '11/24/2021', '11/16/2021');



CREATE TABLE guest_posts(
    guest_post_id SERIAL PRIMARY KEY,
    guest_post VARCHAR(500),
    guest_id INTEGER REFERENCES guests
);

INSERT INTO guest_posts (guest_post_id, guest_post, guest_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');
INSERT INTO guest_posts (guest_post_id, guest_post, guest_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');
INSERT INTO guest_posts (guest_post_id, guest_post, guest_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');
INSERT INTO guest_posts (guest_post_id, guest_post, guest_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');
INSERT INTO guest_posts (guest_post_id, guest_post, guest_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');



CREATE TABLE host_posts(
    host_post_id SERIAL PRIMARY KEY,
    host_post VARCHAR(500),
    event_id INTEGER REFERENCES events
);

INSERT INTO host_posts (host_post_id, host_post, event_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');
INSERT INTO host_posts (host_post_id, host_post, event_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');
INSERT INTO host_posts (host_post_id, host_post, event_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');
INSERT INTO host_posts (host_post_id, host_post, event_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');
INSERT INTO host_posts (host_post_id, host_post, event_id) VALUES ('Bob', 'Personne','bpersonne@yahoo.com');
