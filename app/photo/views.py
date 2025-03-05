import os

from flask import render_template, url_for, request, redirect, json, jsonify, flash

from flask_login import login_required, current_user

from app.models import Album, Photo, Story

from . import photo
from .forms import PhotoForm

from .. import db
from .. import photos as ph
from config import basedir

@photo.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PhotoForm()
    id = request.args.get('id')
    album = Album.query.get(id)
    filenames = []
    photos = Photo.query.filter_by(album_id=album.id).order_by(Photo.id.desc()).all()
    story = Story.query.get(album.story_id)
    if len(photos) != 0:
        for photo in photos:
            if photo.image is not None:
                with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_ph'+str(album.id)+str(photo.id)+'.png'), 'wb') as file:
                    file.write(photo.image) 
            filenames.append((photo.id,'tmp/'+str(current_user.id)+'/'+str(story.id)+'_ph'+str(album.id)+str(photo.id)+'.png'))
    if form.validate_on_submit():
       
        photo = Photo(
            description = form.description.data,
            album_id=album.id
        )
        file = request.files['file']
        file.filename = str(story.id)+'_ph'+str(album.id)+str(photo.id)+'.png'
        ph.save(storage=file, name=file.filename, folder=str(current_user.id))
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_ph'+str(album.id)+str(photo.id)+'.png'), 'rb') as file:
            data = file.read()
        photo.image = data
        db.session.add(photo)
        db.session.commit()
        return redirect(url_for('.index', id=album.id))
    return render_template('photo/index.html', form=form, story=story, album=album, filenames=filenames, theme=current_user.theme)

@photo.route('/photo', methods=['GET', 'POST'])
@login_required
def photo_():
    id = request.args.get('id')
    photo = Photo.query.get(id)
    album = Album.query.get(photo.album_id)
    story = Story.query.get(album.story_id)
    filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_ph'+str(album.id)+str(photo.id)+'.png'
    return render_template('photo/photo.html', photo=photo, story=story, album=album, filename = filename, theme=current_user.theme)

@photo.route('/delete-photo', methods=['GET', 'POST'])
@login_required
def delete_ph():
    data = json.loads(request.data)
    photo = Photo.query.get(int(data['photo_id']))
    album = Album.query.get(photo.album_id)
    story = Story.query.get(album.story_id)
    filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_ph'+str(album.id)+str(photo.id)+'.png'
    if os.path.exists(os.path.join(basedir, 'app/static/'+filename)):
        os.remove(os.path.join(basedir, 'app/static/'+filename))
    if photo:
        try:
            db.session.delete(photo)
            db.session.commit()
            flash(f'[{photo.description[0:5]}...] deleted successfully', category='info')
        except:
            pass
    return jsonify({})

@photo.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    data = json.loads(request.data)
    id = int(data['photo_id'])
    photo = Photo.query.get(id)
    photo.description = data['desc']
    db.session.add(photo)
    db.session.commit()
    return jsonify({})