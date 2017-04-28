"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, jsonify, make_response,session, flash, g
from flask_login import login_user, logout_user, current_user, login_required
from bs4 import BeautifulSoup
from functools import wraps
import jwt
import base64
import os
import smtplib
import requests
import urlparse
import random
from forms import *
from models import *
from image_getter import *

    
# JWT @requires_auth decorator
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, app.config['SECRET_KEY'])

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    

## API Routes

@app.route("/api/users/register", methods=["POST"])
def register():

    first_name = request.get_json()["first_name"]
    last_name = request.get_json()["last_name"]
    username = request.get_json()["username"]
    password = request.get_json()["password"]

    uid = genId(first_name,last_name,random.randint(1,100))

    new_user = UserProfile(userid=uid, username=username, first_name=first_name, last_name=last_name, password=password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"Success":"True"})

@app.route("/api/users/<int:userid>/wishlist", methods=["GET","POST"])
@requires_auth
def wishlist(userid):

    if request.method == "GET":
        wishlist = WishListItem.query.filter_by(userid=userid).all()
        
        wishes = []
        
        for wish in wishlist:
            wish = wish.__dict__
            del wish['_sa_instance_state']
            wishes.append(wish)
            
        return jsonify(wishes)

    elif request.method == "POST":
        
        userid = session["userid"]
        title = request.get_json()["title"]
        description = request.get_json()["description"]
        website = request.get_json()["website"]
        thumbnail = request.get_json()["thumbnail"]

        itemid = genId(title,website,random.randint(1,100))

        witem = WishListItem(itemid=itemid,userid=userid,title=title,description=description,website=website,thumbnail=thumbnail)

        db.session.add(witem)
        db.session.commit()

        return jsonify({"Success":"True"})

@app.route('/api/thumbnails', methods=["GET"])
@requires_auth
def thumbnails():
    """API for thumbnails"""

    # pass url in query string
    url = request.args.get("url")

    if request.method == "GET":
        res = {"error": "null", "message": "success", "thumbnails": getImages(url)}
        return jsonify(res)

@app.route("/api/users/<int:userid>/wishlist/<int:itemid>", methods=["DELETE"])
@requires_auth
def deleteitem(userid,itemid):
    witem = WishListItem.query.filter_by(userid=userid,itemid=itemid).first()

    db.session.delete(witem)
    db.session.commit()

    return jsonify({"success":"True"})

@app.route("/api/users/login", methods=["POST"])
def login():

    uname = request.get_json()["username"]
    pword = request.get_json()["password"]

    user = UserProfile.query.filter_by(username=uname, password=pword).first()

    if user is not None:
        login_user(user)
        session["logged_in"] = True
        session["userid"] = user.userid
        payload = {'sub': user.userid , 'name': user.first_name + " " + user.last_name}
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify(error=None, data={'token': token}, message={"Success":"True"})

## Normal Routes
            
@app.route("/login", methods=["GET"])
def loginpage():
    form = LoginForm()
    return render_template("login.html", form=form)
    
@app.route("/register", methods=["GET"])
def registerpage():
    form = SignUpForm()
    return render_template("register.html",form=form)
    
@app.route("/add-wish", methods=["GET"])
def addwish():
    form = WishListForm()
    return render_template("addwish.html",form=form)

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('userid', None)
    session.pop('logged_in', None)
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))

@app.route("/share/<int:userid>", methods=["GET"])
def sharewishlist(userid):
    user = UserProfile.query.filter_by(userid = userid).first().first_name
    wishlist = WishListItem.query.filter_by(userid=userid).all()
    
    wishes = []
    
    for wish in wishlist:
        wish = wish.__dict__
        del wish['_sa_instance_state']
        wishes.append(wish)
        
    return render_template('wishlist.html', wishes=wishes, name = user)

@app.route("/send", methods=["POST"])
@requires_auth
def send():
    uid = request.get_json()["uid"]
    name = request.get_json()["name"]
    email = request.get_json()["email"]
    user = UserProfile.query.filter_by(userid = uid).first()
    msg = "Click the link to view " + user.first_name + "'s WishList.  http://info3180-project2-jhanelle.c9users.io:8080/share/" + uid
    send_email(name, email, user.first_name, user.email, msg)
    return jsonify({"success":"True"})
    
    
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
    
def genId(fname, lname, num):
    nid = []
    for x in fname:
        nid.append(str(ord(x)))
    for x in lname:
        nid.append(str(ord(x)))
    nid.append(str(num))

    random.shuffle(nid)

    nid = "".join(nid)

    return nid[:7]
    
def send_email(to_name, to_addr, from_name, from_addr, msg):
    subject = "WishList"
    message = """From: {} <{}> To: {} <{}> Subject: {} {} """
    message_to_send = message.format(from_name, from_addr, to_name, to_addr, subject, msg)
    
    # Credentials (if needed)
    username = '@gmail.com'
    password = ''
    
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addr, message_to_send)
    server.quit()

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
