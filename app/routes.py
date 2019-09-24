from flask import render_template, flash, redirect, request
from app import app
from app.forms import newArtistForm


@app.route('/')
@app.route('/index')
def index():
    greeting = "Welcome to music Shmusic!"
    description = "Find out about music in Ithaca"
    return render_template('index.html', greeting=greeting, description=description)

@app.route('/artists')
def artists():
    artistList = ["Cage the Elephant", "Muse","Tyler the Creator", "Flume"]

    return render_template('artists.html', artistList = artistList)


@app.route('/CageTheElephant', methods=['GET','POST'])
def CageTheElephant():
    name = "Cage The Elephant"
    hometown = "Bowling Green"
    bio = "Cage the Elephant is an American rock band from Bowling Green, Kentucky, that formed in 2006 and relocated to London, England, in 2008 before their first album was released. The band currently consists of lead vocalist Matt Shultz, rhythm guitarist Brad Shultz, lead guitarist Nick Bockrath, guitarist and keyboardist Matthan Minster, bassist Daniel Tichenor, and drummer Jared Champion. Lincoln Parish served as the band's lead guitarist from their formation in 2006 until December 2013, when he left on good terms to pursue a career in producing. The band's first album, Cage the Elephant, was released in 2008 to much success, spawning several successful radio singles and gained the band a large following in both the United States and the United Kingdom. It was influenced by classic rock, funk, and blues music. The band's second album, Thank You, Happy Birthday, was heavily influenced by punk rock as well as bands such as Pixies and Nirvana. The band's third album, Melophobia, was the band's concerted effort to find its own distinct musical identity. Melophobia earned the group a Grammy Award nomination in 2015 for Best Alternative Music Album. Cage the Elephant's fourth album, Tell Me I'm Pretty, produced by Dan Auerbach, was released on December 18, 2015. The album won the award for Best Rock Album at the 59th Annual Grammy Awards. The band released a live album, Unpeeled, on July 28, 2017. Their fifth studio album, Social Cues, was released on April 19, 2019."
    events = ["SEP 20 LAS VEGAS, NV", "SEP 23 LOS ANGELES, CA", "SEP 25 SANTA ANA, CA"]

    return render_template('SpecificArtist.html', name = name, hometown = hometown, bio = bio, events = events)


@app.route('/newArtist', methods=['GET', 'POST'])
def newArtist():
    form = newArtistForm()
    if form.validate_on_submit():
        flash("New Artist Created: {} ".format(form.name.data))
        return render_template('SpecificArtist.html', name=form.name.data, hometown=form.town.data, bio=form.bio.data)
    greeting = "Create a new artist"
    return render_template('newArtist.html', greeting=greeting, form=form)