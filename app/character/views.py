import json, os

from flask import render_template, request, url_for, flash, redirect, jsonify, current_app

from flask_login import login_required, current_user

from . import character
from .forms import CharacterForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Story, Character, Group, Supcharacter
from config import basedir

@character.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CharacterForm()
    page = request.args.get('page', 1, int)
    story_id = int(request.args.get('id'))
    story = Story.query.get(story_id)
    pagination = Character.query.filter_by(story_id=story_id).order_by(Character.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    characters = pagination.items
    if form.validate_on_submit():
       
        character = Character(
            name = form.name.data,
            birthday = form.birthday.data,
            description = form.description.data,
            story_id = story_id
        )
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('character.index', id=story_id))
    return render_template('character/index.html', story=story, form=form, pagination=pagination, characters=characters, theme=current_user.theme)

@character.route('/character', methods=['GET', 'POST'])
@login_required
def character_():
    id = int(request.args.get('id'))
    form = CharacterForm()
    uForm = UploadForm()
    character = Character.query.get(id)
    story = Story.query.filter_by(id=character.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Character.query.filter_by(story_id=character.story_id).order_by(Character.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    characters = pagination.items
    if len(character.groups.all()) != 0:
        entered_groups = True
    else:
        entered_groups = False
    if len(character.supcharacters.all()) != 0:
        into_supcharacters = True
    else:
        into_supcharacters = False
    groups = Group.query.filter_by(story_id=character.story_id).all()
    supcharacters = Supcharacter.query.filter_by(story_id=character.story_id).all()
    if form.validate_on_submit():
        character.name = request.form['name']
        character.description = request.form['description']
        db.session.add(character)
        db.session.commit()
      
        return redirect(url_for('.character_', id=character.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_cr'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cr'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.character_', id=character.id))
    
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cr'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_cr'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cr'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            character.cover = data
            db.session.add(character)
            db.session.commit()
        if character.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cr'+str(id)+'.png')) 
            filename = 'images/character.png'
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cr'+str(id)+'.png'), 'wb') as f:
            if character.cover:
                f.write(character.cover)
        filename = 'images/character.png'    
    return render_template('character/character.html', form=form, uForm=uForm, story=story, into_supcharacters=into_supcharacters, supcharacters=supcharacters, character=character, entered_groups=entered_groups, characters=characters, pagination=pagination, groups=groups, filename=filename, theme=current_user.theme)


@character.route('/delete-character', methods=['GET', 'POST'])
@login_required
def delete_character():
    data = json.loads(request.data)
    character = Character.query.get(int(data['character_id']))
    story = Story.query.get(character.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cr'+str(character.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cr'+str(character.id)+'.png'))
    if character:
        try:
            db.session.delete(character)
            db.session.commit()
            flash(f'"{character.name}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})


@character.route('/inclusion', methods=['GET', 'POST'])
@login_required
def inclusion():
    data = json.loads(request.data)
    character = Character.query.get(int(data['character_id']))
    group = Group.query.get(int(data['group_id']))
    character.groups.append(group)
    db.session.add(character)
    db.session.commit()
    return jsonify({})


@character.route('/exclusion', methods=['GET', 'POST'])
@login_required
def exclusion():
    data = json.loads(request.data)
    character = Character.query.get(int(data['character_id']))
    group = Group.query.get(int(data['group_id']))
    character.groups.remove(group)
    db.session.add(character)
    db.session.commit()
    return jsonify({})

@character.route('/inclusion2', methods=['GET', 'POST'])
@login_required
def inclusion2():
    data = json.loads(request.data)
    character = Character.query.get(int(data['character_id']))
    supcharacter = Supcharacter.query.get(int(data['supcharacter_id']))
    character.supcharacters.append(supcharacter)
    db.session.add(character)
    db.session.commit()
    return jsonify({})

@character.route('/exclusion2', methods=['GET', 'POST'])
@login_required
def exclusion2():
    data = json.loads(request.data)
    character = Character.query.get(int(data['character_id']))
    supcharacter = Supcharacter.query.get(int(data['supcharacter_id']))
    character.supcharacters.remove(supcharacter)
    db.session.add(character)
    db.session.commit()
    return jsonify({})