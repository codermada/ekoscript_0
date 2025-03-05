import os

from flask import render_template, url_for, request, redirect, json, jsonify, flash

from flask_login import login_required, current_user

from app.models import Character, Illustration, Story

from . import illustration
from .forms import IllustrationForm

from .. import db, photos
from config import basedir

@illustration.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = IllustrationForm()
    id = request.args.get('id')
    character = Character.query.get(id)
    filenames = []
    illustrations = Illustration.query.filter_by(character_id=character.id).order_by(Illustration.id.desc()).all()
    story = Story.query.get(character.story_id)
    if len(illustrations) != 0:
        for illustr in illustrations:
            if illustr.image is not None:
                with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_il'+str(character.id)+str(illustr.id)+'.png'), 'wb') as file:
                    file.write(illustr.image) 
            filenames.append((illustr.id,'tmp/'+str(current_user.id)+'/'+str(story.id)+'_il'+str(character.id)+str(illustr.id)+'.png'))
    if form.validate_on_submit():
       
        illustr = Illustration(
            description = form.description.data,
            character_id=character.id
        )
        file = request.files['file']
        file.filename = str(story.id)+'_il'+str(character.id)+str(illustr.id)+'.png'
        photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_il'+str(character.id)+str(illustr.id)+'.png'), 'rb') as file:
            data = file.read()
        illustr.image = data
        db.session.add(illustr)
        db.session.commit()
        return redirect(url_for('.index', id=character.id))
    return render_template('illustration/index.html', uForm=form, story=story, character=character, filenames=filenames, theme=current_user.theme)

@illustration.route('/illustration', methods=['GET', 'POST'])
@login_required
def illustration_():
    id = request.args.get('id')
    illustr = Illustration.query.get(id)
    character = Character.query.get(illustr.character_id)
    story = Story.query.get(character.story_id)
    filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_il'+str(character.id)+str(illustr.id)+'.png'
    return render_template('illustration/illustration.html', illustr=illustr, story=story, character=character, filename = filename, theme=current_user.theme)

@illustration.route('/delete-illustration', methods=['GET', 'POST'])
@login_required
def delete_il():
    data = json.loads(request.data)
    illustr = Illustration.query.get(int(data['illustration_id']))
    character = Character.query.get(illustr.character_id)
    story = Story.query.get(character.story_id)
    filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_il'+str(character.id)+str(illustr.id)+'.png'
    if os.path.exists(os.path.join(basedir, 'app/static/'+filename)):
        os.remove(os.path.join(basedir, 'app/static/'+filename))
    if illustr:
        try:
            db.session.delete(illustr)
            db.session.commit()
            flash(f'[{illustr.description[0:5]}...] deleted successfully', category='info')
        except:
            pass
    return jsonify({})

@illustration.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    data = json.loads(request.data)
    id = int(data['illustration_id'])
    illustration = Illustration.query.get(id)
    illustration.description = data['desc']
    db.session.add(illustration)
    db.session.commit()
    return jsonify({})