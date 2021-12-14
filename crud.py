"""CRUD operations."""

from model import db, User, Guest, Event, Guest_post, Host_post, connect_to_db
from flask import session

#############################################################################

def create_user(email, password, fname, lname, phone, start_date):
    """Create and return a new user."""

    user = User(email=email, password=password, fname=fname, lname=lname, phone=phone, start_date=start_date)

    db.session.add(user)
    db.session.commit()

    return user

#############################################################################

def get_users():
    """Return all users."""

    return User.query.all()

#############################################################################

def get_user_by_id(user_id):
    """Return a user info by primary key."""

    return User.query.get(user_id)

#############################################################################

def get_user_by_email(email):
    """Return a user info by email."""

    return User.query.filter(User.email == email).first()


#############################################################################

def get_user_phone_number(phone):
    """gets a user phone number"""

    return User.query.filter(User.phone == phone).first()

#############################################################################

def get_user_by_name(first_name, last_name):
    """Return a user by name."""

    return User.query.filter((User.fname == first_name) & (User.lname == last_name)).first()

#############################################################################

def get_rsvp_response(rsvp_attend):

    return Guest.query.filter(Guest.rsvp_attend == rsvp_attend).first()

#############################################################################

def get_event_by_id(event_id):
    """Return a event by primary key."""

    return Event.query.get(event_id)

#############################################################################

def get_guest_by_id(guest_id):
    """get guest by guest_id"""

    return Guest.query.get(guest_id)

#############################################################################

def get_guest_by_user_and_event(user_id, event_id):
    """Gets the guest for an event by user_id and event_id"""
    
    return Guest.query.filter_by(event_id=event_id, user_id=user_id).first()

#############################################################################

def get_host_by_host_id_and_event(host_id, event_id): 
    """Gets the host for a particular event by user_id and event_id"""

    return Event.query.filter((Event.host_id==host_id) & (Event.event_id==event_id)).all()


#############################################################################

def get_event_by_name(event_name):
    """Return event by event name"""

    event_name = Event.query.filter(event_name).all() 
    return event_name  

#############################################################################

def get_guest_event_invites(user_id):
    """Gets the events a particular user is invited to"""
    guest_event_list = []
    user_guest_event = Guest.query.filter(Guest.user_id==user_id).all() #list of guest objects (user_guest_events)
    for user_guest in user_guest_event: #looping through each guest object, for each guest in guest object list
        if user_guest.rsvp_attend == "No response":
            guest_event_list.append(user_guest.event_rel) #take event from each guest object and add it guest_event_list
    
    return guest_event_list

#############################################################################

def get_guest_attending_events(user_id):
    """Get events a guest RSVP YES to attending"""
    guest_attend_list = []
    user_guest_event = Guest.query.filter(Guest.user_id==user_id).all() #list of guest objects (user_guest_events)
    for user_guest in user_guest_event: #looping through each guest object, for each guest in guest object list
        if user_guest.rsvp_attend == "YES":
            guest_attend_list.append(user_guest.event_rel) #take event from each guest object and add it guest_event_list
    
    return guest_attend_list

#############################################################################

def get_hosted_events(host_id):
    """Gets the events hosted by a particular user via host_id"""

    return Event.query.filter(Event.host_id==host_id).all()

#############################################################################

def get_user_from_session():
    """Getting user from session via email"""

    user_email = session['user_email']

    user = User.query.filter_by(email=user_email).first()
    
    return user

#############################################################################

def create_event(event_name, location, venue, event_date, event_time, rsvp_date, host, event_description):
    """Create and return a new event."""

    event = Event(
        host_rel=host,
        event_name=event_name,
        location=location,
        venue=venue,
        evtdate=event_date,
        evttime=event_time,
        rsvp_date=rsvp_date,
        event_description=event_description)


    db.session.add(event)
    db.session.commit()

    return event

#############################################################################

def create_guest(guest_user, event_details, rsvp_attend):
    """Create and return a new guest."""

    repeat_guest = Guest.query.filter_by(user_rel=guest_user, event_rel=event_details).all()

    if repeat_guest:
        return None
    else:
        new_guest = Guest(user_rel=guest_user, event_rel=event_details, rsvp_attend=rsvp_attend)


    db.session.add(new_guest)
    db.session.commit()

    return new_guest

#############################################################################

def update_rsvp(guest, rsvp_status):
    """Updating guest rsvp status in database"""
    
    guest.rsvp_attend = rsvp_status
    db.session.commit()


#############################################################################

def get_guest_comments_for_event(guest_post_id):
    """Gets the comments posted by a particular guest via guest_post_id"""
    
    return Guest_post.query.get(guest_post_id)

#############################################################################

def get_host_comment_by_id(host_post_id):
    """Gets comments posted by a host for an event"""

    return Host_post.query.get(host_post_id)

#############################################################################

def create_guest_post(guest_post, guest):
    """Creates and returns a posting made by a guest for a particular event"""

    guest_comment = Guest_post(guest_post=guest_post, guest_rel=guest) #guest_rel connects the guest post to the guest object

    db.session.add(guest_comment)
    db.session.commit()

    return guest_comment

#############################################################################

def create_host_post(host_post, event): #Do I need to do anything with HOST ID?
    """Create and return a posting made by a host for a particular event"""

    host_comment = Host_post(host_post=host_post, event_rel2=event)

    db.session.add(host_comment)
    db.session.commit()

    return host_comment 

#############################################################################

def get_guests_for_event(event_id): 
    """Gets all guests for an event"""

    guest_list = []
   
    guest = Guest.query.filter((Guest.event_id==event_id) & (Guest.rsvp_attend == "YES")).all() #guest objects for an event where RSVP is YES
    print(guest)

    return guest 

#############################################################################

def get_guest_phone_numbers(event_id):
    """Loops through all guests for an event and gets the phone numbers for all of them"""
    guest_phone_numbers = [] #only adds phone numbers for RSVP of 'YES'
    event_guests = get_guests_for_event(event_id)

    for guest in event_guests:
        guest_phone_numbers.append(guest.user_rel.phone)

    return guest_phone_numbers #returns a list of phone numbers for guests attending a particular event

#############################################################################

#@Amanda P you need to show the preexisting comments in your HTML. 
#It would probably be a Jinja for loop that displays all the guest comments for that event. 
#Guest comments don't have a direct relationship to event, so you probably need a new crud 
#function that loops through all guests for an event and gets the comments for all of them.

def show_all_guest_comments(event_id):
    """Loops through all guests for an event and gets the comments for all of them"""
    
    guest_attend_comments = []
    event_guests = get_guests_for_event(event_id) #guests for an event

    for guest in event_guests: #getting a guest out of the guest list
        guest_attend_comments.extend(guest.guest_user_posts) #adding the comments to the list
        
        
    return guest_attend_comments #return list of guest comments

#############################################################################

def show_all_host_comments(event_id, host_id):

    host_comments = []
    event_host = get_host_by_host_id_and_event(host_id, event_id)
    hosted_events = get_hosted_events(host_id)
    print(event_host)
    for event_host in hosted_events:
        host_comments.extend(event_host.host_event_posts)

    return host_comments

#############################################################################

def get_profile_pic(user_image):
    """Grabs user's profile picture from DB and returns it"""

    # Getting the provided user's profile picture from DB
    profile_pic = user.user_image

    # Returns profile picture URL
    return profile_pic

#############################################################################

def event_page_pic(event):
    """Get's the image uploaded for the event page"""

    event_pic = event.event_image

    return event_pic

#############################################################################


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
