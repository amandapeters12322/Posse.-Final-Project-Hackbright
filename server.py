"""Server for event planning app."""


from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
import send_sms
from jinja2 import StrictUndefined
from twilio.rest import Client
import cloudinary.uploader
import os

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUDINARY_NAME = "df2xnbdjj"



app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
#############################################################################

@app.route("/")
def homepage():
    """View homepage."""
    
    return render_template("homepage.html")

#############################################################################

@app.route("/account")
def account():
    """Takes to user account page where they can change profile photo"""
    email = session["user_email"]
    user = crud.get_user_by_email(email)

    return render_template("account.html", user=user)

#############################################################################

@app.route("/dashboard")
def dashboard():
    """User can view the profile dashboard"""
    
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    guest_event = crud.get_guest_event_invites(user.user_id) #shows events a user is invited to
    guest_attending = crud.get_guest_attending_events(user.user_id) #shows events a user is attending, RSVP is YES
    #profile_pic = crud.get_profile_pic(user)


    email = session["user_email"]
    user = crud.get_user_by_email(email)
    host_event = crud.get_hosted_events(user.user_id)
   #^^^Shows events a user is hosting

    return render_template("dashboard.html", guest_event=guest_event, host_event=host_event, user=user, guest_attending=guest_attending)

#############################################################################

@app.route("/register", methods=["POST"])
def create_account():
    """Create a new user account."""

    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    phone = request.form.get("phone")
    start_date = request.form.get("start_date")

    user = crud.get_user_by_email(email)
    if user:
        flash("We already have an account with that email, please try again.")
        return redirect("/")
    else:
        crud.create_user(email, password, fname, lname, phone, start_date)
        flash("Congratulations! Your account has been created! Please scroll down to Login")

    return redirect("/")


#############################################################################

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")  
    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("Sorry, the email or password you entered was incorrect. Please try again")
        return redirect("/")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        #print(session)
        #flash(f"Welcome back, {user.email}! We missed you!")

    return redirect("/dashboard")


#############################################################################

@app.route("/logout")
def logout():
    """User must be logged in."""
    del session["user_email"]
    #flash("Logged Out.")

    return redirect("/")
    


#############################################################################

@app.route("/show_event_details/<event_id>")
def show_event_details(event_id):
    """Show details on a particular event."""
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    event = crud.get_event_by_id(event_id)
    event_guest = crud.get_guest_by_user_and_event(user.user_id, event.event_id) #guest object
    
    comments = reversed(crud.show_all_guest_comments(event_id))
    host_comments = reversed(crud.show_all_host_comments(event_id, event.host_id))
    #event_image_file = url_for('static', filename='app_pics/' + event.event_image_file) 

    


    if event_guest == None:
        rsvp_response = None
    else:
        rsvp_response = crud.get_rsvp_response(event_guest.rsvp_attend)


    if user.user_id == event.host_id:
        is_host = True
    else:
        is_host = False
    
    if event_guest is not None and user.user_id == event_guest.user_id:
        is_guest = True
    else:
        is_guest = False 


    return render_template("event_details.html", event=event, is_host=is_host, event_guest=event_guest, rsvp_response=rsvp_response, is_guest=is_guest, comments=comments, host_comments=host_comments)


#############################################################################

@app.route("/create_event", methods=["POST"])
def create_new_event():
    """Create a new event"""

    event_name = request.form.get("event_name")
    location = request.form.get("location")
    venue = request.form.get("venue")
    event_date = request.form.get("evtdate")
    event_time = request.form.get("evttime")
    rsvp_date = request.form.get("rsvp_date")
    event_description = request.form.get("event_description")
    
    current_user = crud.get_user_from_session()
   

    new_event = crud.create_event(event_name, location, venue, event_date, event_time, rsvp_date, current_user, event_description)

    

    return redirect(f"/show_event_details/{new_event.event_id}")

   
#############################################################################

@app.route("/create_guest_list.json")
def create_new_guest():
    """Create a guest list that will populate on the event details page"""

    guest_first_name = request.args.get("fname")
    guest_last_name = request.args.get("lname")
    event_id = request.args.get("event_id")

    email = session["user_email"]
    user = crud.get_user_by_email(email)
    guest_user = crud.get_user_by_name(guest_first_name, guest_last_name)
    event = crud.get_event_by_id(event_id)
    event_guest = crud.get_guest_by_user_and_event(user.user_id, event.event_id)
    comments = reversed(crud.show_all_guest_comments(event_id))
    host_comments = reversed(crud.show_all_host_comments(event_id, event.host_id))

    
    is_guest = False
    is_host = True

    if guest_user is None:
        flash("Sorry, that is not a valid user")
    else:
        new_guest = crud.create_guest(guest_user, event, rsvp_attend="No response")
        new_guests_dict = {"first_name": guest_user.fname, "last_name": guest_user.lname, "rsvp_status": new_guest.rsvp_attend}
    
        print(new_guests_dict)
        return jsonify(new_guests_dict)

        
#############################################################################

@app.route("/host")
def show_host_events():
    """Show event by hosted by a particular user"""
    
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    host_event = crud.get_hosted_events(user.user_id)
    
   

    return render_template("host.html", host_event=host_event)
    

#############################################################################

@app.route("/rsvp_update.json") #for AJAX with RSVP form. Need '.json' and jsonify for AJAX
def update_guest_rsvp():
    """Update a guest RSVP from "No response to YES or NO"""

    email = session["user_email"]
    user = crud.get_user_by_email(email)
    event_id = request.args.get("event_id")
    event = crud.get_event_by_id(event_id)
    event_guest = crud.get_guest_by_user_and_event(user.user_id, event.event_id)


    if event_guest is not None:
        is_guest = True
        # print(is_guest)
        crud.update_rsvp(event_guest, request.args.get("rsvp_attend"))#taking guest and rsvp response from form and using crud function to update rsvp_attend in database
        rsvp_values = {"rsvp_status": event_guest.rsvp_attend} #creating dictionary of rsvp responses 
        #key - rsvp status, value - yes or no
        return jsonify(rsvp_values)
    

    return {}


#############################################################################

@app.route("/create_guest_comment.json") 
def create_guest_comment():
    """Create a new guest comment"""

    #guest_comment = request.args.get("guest_post")
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    event_id = request.args.get("event_id")
    event = crud.get_event_by_id(event_id)
    event_guest = crud.get_guest_by_user_and_event(user.user_id, event.event_id)
    

    crud.create_guest_post(request.args.get("guest_comment"), event_guest)
    guest_post = {"guest_post": request.args.get("guest_comment")}

    send_sms.send_event_update(event_id) #sends SMS update to guests who RSVP yes

    return jsonify(guest_post)

#############################################################################

@app.route("/create_host_comment.json") 
def create_host_comment():
    """Create a new guest comment"""

    #host_comment = request.args.get("host_post")
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    event_id = request.args.get("event_id")
    event = crud.get_event_by_id(event_id)
    event_host = crud.get_host_by_host_id_and_event(event.host_id, event.event_id)


    crud.create_host_post(request.args.get("host_comment"), event)
    host_post = {"host_post": request.args.get("host_comment")}

    send_sms.send_event_update(event_id) #sends SMS update to guests who RSVP yes


    return jsonify(host_post)

#############################################################################

@app.route("/upload-profile-pic", methods=["POST"])
def upload_profile_pic():
    """Grabs the user's uploaded image and uploads it to Cloudinary API.
    Saves Cloudinary profile picture URL to User table in DB.
    Sends user back to profile picture where new profile picture is displayed."""

    # Grabbing profile picture from user input
    user_image = request.files['profile-img']

    # Uploading profile picture using Cloudinary API
    result = cloudinary.uploader.upload(user_image, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUDINARY_NAME)

    # Grabbing image URL from Cloudinary API and saving to variable
    img_url = result['secure_url']

    #Grabs user using user email in session
    user = crud.get_user_by_email(session["user_email"])

    # Adds profile pic to user's row in User DB
    user.user_image = img_url
    db.session.commit()

    # Sends user to same page where new profile pic is displayed
    return redirect(request.referrer)

##############################################################################

@app.route("/get-profile-pic", methods=["POST"])
def get_profile_pic():
    """Checks to see if the user has a profile picture URL in the DB
    Returns the profile picture URL or a string if it does not exist"""

    # Grab user using the user ID in session
    user = crud.get_user_by_email(session["user_email"])

    # Grabs the profile picture URL from user's DB entry
    img_url = user.user_image

    # If the profile picture exists
    if img_url:
        return img_url
    # If the profile picture doesn't exist
    else:
        return "False"

##############################################################################

@app.route("/upload-event-pic/<event_id>", methods=["POST"])
def upload_event_pic(event_id):
    """Grabs the user's uploaded image and uploads it to Cloudinary API.
    Saves Cloudinary event picture URL to EVENT table in DB.
    Sends user back to event picture where new event picture is displayed."""

    # Grabbing profile picture from user input
    event_image = request.files['event-img']

    # Uploading profile picture using Cloudinary API
    result = cloudinary.uploader.upload(event_image, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUDINARY_NAME)

    # Grabbing image URL from Cloudinary API and saving to variable
    event_img_url = result['secure_url']

    #Grabs event using event_id 
    event = crud.get_event_by_id(event_id)

    # Adds profile pic to user's row in User DB
    event.event_image = event_img_url
    db.session.commit()

    # Sends user to same page where new profile pic is displayed
    return redirect(request.referrer)

##############################################################################

@app.route("/get-event-pic/<event_id>", methods=["POST"])
def get_event_pic(event_id):
    """Checks to see if the user has a profile picture URL in the DB
    Returns the profile picture URL or a string if it does not exist"""
    
    #Grabs event using event_id in session

    event = crud.get_event_by_id(event_id)

    # Grabs the profile picture URL from user's DB entry
    event_img_url = event.event_image

    # If the profile picture exists
    if event_img_url:
        return event_img_url
    # If the profile picture doesn't exist
    else:
        return "False"







if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


    
