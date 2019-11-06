from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import newArtistForm, LoginForm, RegistrationForm, newVenueForm, newEventForm
from app.models import Artist
from app.models import Event
from app.models import Venue
from app.models import ArtistToEvent
from app.models import User
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse




@app.route('/')
@app.route('/index')
def index():
    greeting = "Welcome to music Shmusic!"
    description = "Find out about music in Ithaca"
    return render_template('index.html', greeting=greeting, description=description)

@app.route('/artists')
def artists():
    artistList = Artist.query.order_by(Artist.name).all()

    return render_template('artists.html', artistList=artistList)


@app.route('/artists/<name>', methods=['GET', 'POST'])
def artist(name):
    my_artist = Artist.query.filter_by(name=name).first()
    events = my_artist.events

    return render_template('SpecificArtist.html', artist=my_artist, events=events)


@app.route('/newArtist', methods=['GET', 'POST'])
def newArtist():
    form = newArtistForm()
    if form.validate_on_submit():
        flash("New Artist Created: {} ".format(form.name.data))
        new_artist = Artist(name=form.name.data, hometown=form.town.data, bio=form.bio.data)
        db.session.add(new_artist)
        db.session.commit()
        return redirect(url_for('artists'))
    greeting = "Create a new artist"
    return render_template('newArtist.html', greeting=greeting, form=form)

@app.route('/reset_db')
def reset_db():
   flash("Resetting database: deleting old data and repopulating with dummy data")
   # clear all data from all tables
   meta = db.metadata
   for table in reversed(meta.sorted_tables):
       print('Clear table {}'.format(table))
       db.session.execute(table.delete())

   artist1 = Artist(id=1, name='Cage The Elephant', hometown='Bowling Green', bio='Great alternative Rock band that have released many hits')
   db.session.add(artist1)
   venue1 = Venue(id=1,name='The State Theater',address='107 W State St')
   db.session.add(venue1)
   event1 = Event(id=1, name='The night', when=datetime(2019, 5, 23, 8, 30), venueID=1)
   db.session.add(event1)
   a2e1 = ArtistToEvent(id=1,artistID=1,eventID=1)
   db.session.add(a2e1)
   artist2 = Artist(id=2, name='Green Day', hometown='Rodeo',bio='Legendary punk band that is known everywhere and will be known until the end of music')
   db.session.add(artist2)
   venue2 = Venue(id=2, name='The Haunt', address='702 Willow Ave')
   db.session.add(venue2)
   event2 = Event(id=2, name='The Day', when=datetime(2019, 5, 23, 1, 30), venueID=2)
   db.session.add(event2)
   a2e2 = ArtistToEvent(id=2, artistID=2, eventID=2)
   db.session.add(a2e2)
   artist3 = Artist(id=3, name='Muse', hometown='Teignmouth', bio='Amazing alt rock band that have many influences from queen to 1984')
   db.session.add(artist3)
   venue3 = Venue(id=3, name='SPAC', address='108 Avenue of the Pines')
   db.session.add(venue3)
   event3 = Event(id=3, name='Light years away', when=datetime(2019, 12, 16, 6), venueID=3)
   db.session.add(event3)
   a2e3 = ArtistToEvent(id=3, artistID=3, eventID=3)
   db.session.add(a2e3)
   event4 = Event(id=4, name='Apples to Oranges', when=datetime(2019, 1, 23, 10), venueID=2)
   db.session.add(event4)
   a2e4 = ArtistToEvent(id=4, artistID=1, eventID=4)
   db.session.add(a2e4)
   event5 = Event(id=5, name='Music mania', when=datetime(2019, 2, 14, 7, 30), venueID=2)
   a2e5 = ArtistToEvent(id=5, artistID=3, eventID=5)
   db.session.add(a2e5)
   db.session.add(event5)
   db.session.commit()

   return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/newVenue', methods=['GET', 'POST'])
def newVenue():
    form = newVenueForm()
    if form.validate_on_submit():
        new_venue = Venue(name=form.name.data, address=form.address.data)
        db.session.add(new_venue)
        db.session.commit()
        flash("New Venue Created: {} ".format(form.name.data))
        return redirect(url_for('index'))
    greeting = "Create a new venue"
    return render_template('newVenue.html', greeting=greeting, form=form)


@app.route('/newEvent', methods=['GET', 'POST'])
def newEvent():
    form = newEventForm()
    form.venue.choices = [(venue.id, venue.name) for venue in Venue.query.order_by('name')]
    form.artists.choices = [(artist.id, artist.name) for artist in Artist.query.order_by('name')]
    if form.validate_on_submit():

        new_event = Event(name=form.name.data, when=form.when.data, venueID=form.venue.data)
        db.session.add(new_event)
        db.session.commit()
        for i in form.artists.data:
            artist = Artist.query.get(i)
            new_artist_to_event = ArtistToEvent(eventID=new_event.id, artistID=artist.id)
            db.session.add(new_artist_to_event)
            db.session.commit()
        flash("New Event Created: {} ".format(form.name.data))
        return redirect(url_for('index'))
    greeting = "Create a new Event"
    return render_template('newEvent.html', greeting=greeting, form=form)
