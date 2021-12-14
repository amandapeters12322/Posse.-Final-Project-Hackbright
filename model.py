"""Models for event planning app"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


#  A NULL value is a special marker used in SQL to indicate that a data value does not exist in the database. 
# In other words, it is just a placeholder to denote values that are missing or that we do not know.


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.String(11))
    user_image = db.Column(db.String(100))

    def __repr__(self): #for debugging puproses only - helps you identify without needing specific ID
        return f"<User user_id={self.user_id} email={self.email} fname={self.fname} lname={self.lname} password={self.password}>"



class Guest(db.Model):
    """A guest."""

    __tablename__ = "guests"

    guest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    rsvp_attend = db.Column(db.String(12), nullable=False, default="No response")
    
    
    event_rel = db.relationship("Event", backref="evtguests")
    user_rel = db.relationship("User", backref="usrguest") # gives me all events the user is invited to as a guest
#If my_event is an Event object, then you would do my_event.evtguests
#If you have that on your Guest class, then event.evtguests will be all the guests for that event

    def __repr__(self): #for debugging puproses only - helps you identify without needing specific ID
        return f"<Guest guest_id={self.guest_id} user_id={self.user_id}>"

    

class Event(db.Model):
    """An event."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) #host_id is the same as their user_id
    event_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    venue = db.Column(db.String(50), nullable=False)
    evtdate = db.Column(db.String(10), nullable=False)
    evttime = db.Column(db.String(9), nullable=False)
    rsvp_date = db.Column(db.String(10), nullable=False)
    event_description = db.Column(db.String(300), nullable=False)
    event_image = db.Column(db.String(100))

    
    host_rel = db.relationship("User", backref="hosted_events")
    #User.hosted_events gets me the events hosted by a particular user

    def __repr__(self): #for debugging puproses only - helps you identify without needing specific ID
        return f"<Event event_id={self.event_id} event_name={self.event_name}>"



class Guest_post(db.Model):
    """Stored posts from guests on event feed"""

    __tablename__="guest_posts"

    guest_post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    guest_post = db.Column(db.String(1200))
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.guest_id"))

    guest_rel = db.relationship("Guest", backref="guest_user_posts") #if in Guest use the backref, if in Guest_post, use the variable
    #Guest.guest_user_posts gets me the comments posted by a particular guest

    def __repr__(self): #for debugging puproses only - helps you identify without needing specific ID
        return f"<Guest_post guest_post_id={self.guest_post_id}>"



class Host_post(db.Model):
    """Stores posts from hosts on event feed"""

    __tablename__="host_posts"

    host_post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    host_post = db.Column(db.String(1200))
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    
    event_rel2 = db.relationship("Event", backref="host_event_posts")
    #Event.host_event_posts gets me the comments posted from a host for particular event


    def __repr__(self): #for debugging puproses only - helps you identify without needing specific ID
        return f"<Host_post host_post_id={self.host_post_id}>"



#database name = event_planning_app

def connect_to_db(flask_app, db_uri="postgresql:///event_planning_app", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
