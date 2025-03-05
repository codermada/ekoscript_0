import json, os

from flask import render_template, redirect, url_for, request, flash, jsonify, current_app

from flask_login import login_required, current_user

from . import album
from .forms import AlbumForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Album, Photo, Story
from config import basedir


@album.route('/', methods=['GET', 'POST'])
@login_required
def index():
    story_id = int(request.args.get('id'))
    story = Story.query.get(story_id)
    form = AlbumForm()
    page = request.args.get('page', 1, type=int)
    pagination = Album.query.filter_by(story_id=story_id).order_by(Album.title).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    albums = pagination.items
    if form.validate_on_submit():
        album = Album(title=form.title.data,
                    description=form.description.data,
                    story_id=story_id)
        db.session.add(album)
        db.session.commit()
        return redirect(url_for('album.index', id=story_id))
    return render_template("album/index.html", story=story, form=form, pagination=pagination, albums=albums, theme=current_user.theme)

@album.route('/album', methods=['GET', 'POST'])
@login_required
def album_():
    id = int(request.args.get('id'))
    form = AlbumForm()
    uForm = UploadForm()
    album = Album.query.get(id)
    story = Story.query.filter_by(id=album.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Album.query.filter_by(story_id=album.story_id).order_by(Album.title).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    albums = pagination.items
    
    if form.validate_on_submit():
        album.title = request.form['title']
        album.description = request.form['description']
        db.session.add(album)
        db.session.commit()
        return redirect(url_for('.album_', id=album.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_al'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_al'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.album_', id=album.id))
    
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_al'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_al'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_al'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            album.cover = data
            db.session.add(album)
            db.session.commit()
        if album.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_al'+str(id)+'.png')) 
            filename = 'images/album.png' 
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_al'+str(id)+'.png'), 'wb') as f:
            if album.cover:
                f.write(album.cover)
        filename = 'images/album.png'    
    return render_template('album/album.html', form=form, uForm=uForm, story=story, album=album, albums=albums, pagination=pagination, filename=filename, theme=current_user.theme)



@album.route('/delete-album', methods=['GET', 'POST'])
@login_required
def delete_album():
    data = json.loads(request.data)
    album = Album.query.get(int(data['album_id']))
    story = Story.query.get(album.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_al'+str(album.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_al'+str(album.id)+'.png'))
    if album:
        try:
            db.session.delete(album)
            db.session.commit()
            flash(f'"{album.title}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})