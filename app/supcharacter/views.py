import json, os

from flask import render_template, request, url_for, flash, redirect, jsonify, current_app

from flask_login import login_required, current_user

from . import supcharacter
from .forms import SupcharacterForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Story, Supcharacter
from config import basedir

@supcharacter.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SupcharacterForm()
    page = request.args.get('page', 1, int)
    story_id = int(request.args.get('id'))
    story = Story.query.get(story_id)
    pagination = Supcharacter.query.filter_by(story_id=story_id).order_by(Supcharacter.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    supcharacters = pagination.items
    if form.validate_on_submit():
    
        supcharacter = Supcharacter(
            name = form.name.data,
            description = form.description.data,
            story_id = story_id
        )
        db.session.add(supcharacter)
        db.session.commit()
    
        return redirect(url_for('supcharacter.index', id=story_id))
    return render_template('supcharacter/index.html', story=story, form=form, pagination=pagination, supcharacters=supcharacters, theme=current_user.theme)


@supcharacter.route('/supcharacter', methods=['GET', 'POST'])
@login_required
def supcharacter_():
    id = int(request.args.get('id'))
    form = SupcharacterForm()
    uForm = UploadForm()
    supcharacter = Supcharacter.query.get(id)
    story = Story.query.filter_by(id=supcharacter.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Supcharacter.query.filter_by(story_id=supcharacter.story_id).order_by(Supcharacter.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    supcharacters = pagination.items
    if form.validate_on_submit():
        supcharacter.name = request.form['name']
        supcharacter.description = request.form['description']
        db.session.add(supcharacter)
        db.session.commit()
        return redirect(url_for('.supcharacter_', id=supcharacter.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_sc'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sc'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.supcharacter_', id=supcharacter.id))
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sc'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_sc'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sc'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            supcharacter.cover = data
            db.session.add(supcharacter)
            db.session.commit()
        if supcharacter.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sc'+str(id)+'.png'))
            filename = 'images/supcharacter.png'
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sc'+str(id)+'.png'), 'wb') as f:
            if supcharacter.cover:
                f.write(supcharacter.cover)
        filename = 'images/supcharacter.png'    
    return render_template('supcharacter/supcharacter.html', form=form, uForm=uForm, story=story, supcharacter=supcharacter, supcharacters=supcharacters, pagination=pagination, filename=filename, theme=current_user.theme, n_characters=len(supcharacter.characters.all()))

@supcharacter.route('/delete-supcharacter', methods=['GET', 'POST'])
@login_required
def delete_supcharacter():
    data = json.loads(request.data)
    supcharacter = Supcharacter.query.get(int(data['supcharacter_id']))
    story = Story.query.get(supcharacter.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sc'+str(supcharacter.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sc'+str(supcharacter.id)+'.png'))
    if supcharacter:
        try:
           
            db.session.delete(supcharacter)
            db.session.commit()
            flash(f'"{supcharacter.name}" deleted successfully', category='info')
            
        except:
            pass
    return jsonify({})