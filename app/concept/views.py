import json, os

from flask import render_template, request, url_for, flash, redirect, jsonify, current_app

from flask_login import login_required, current_user

from . import concept
from .forms import ConceptForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Story, Concept
from config import basedir


@concept.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ConceptForm()
    page = request.args.get('page', 1, int)
    story_id = int(request.args.get('id'))
    story = Story.query.get(story_id)
    pagination = Concept.query.filter_by(story_id=story_id).order_by(Concept.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    concepts = pagination.items
    if form.validate_on_submit():
        concept = Concept(
            name = form.name.data,
            description = form.description.data,
            story_id = story_id
        )
        db.session.add(concept)
        db.session.commit()
        return redirect(url_for('concept.index', id=story_id))
    return render_template('concept/index.html', story=story, form=form, pagination=pagination, concepts=concepts, theme=current_user.theme)

@concept.route('/concept', methods=['GET', 'POST'])
@login_required
def concept_():
    id = int(request.args.get('id'))
    form = ConceptForm()
    uForm = UploadForm()
    concept = Concept.query.get(id)
    story = Story.query.filter_by(id=concept.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Concept.query.filter_by(story_id=concept.story_id).order_by(Concept.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    concepts = pagination.items
    if form.validate_on_submit():
        concept.name = request.form['name']
        concept.description = request.form['description']
        
        db.session.add(concept)
        db.session.commit()
        
        return redirect(url_for('.concept_', id=concept.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_cp'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.concept_', id=concept.id))
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            concept.cover = data
            db.session.add(concept)
            db.session.commit()
        if concept.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png'))
            filename = 'images/concept.png'        
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png'), 'wb') as f:
            if concept.cover:
                f.write(concept.cover)
        filename = 'images/concept.png'    
    return render_template('concept/concept.html', form=form, uForm=uForm, story=story, concept=concept, concepts=concepts, pagination=pagination, filename=filename, theme=current_user.theme)

@concept.route('/delete-concept', methods=['GET', 'POST'])
@login_required
def delete_concept():
    data = json.loads(request.data)
    concept = Concept.query.get(int(data['concept_id']))
    story = Story.query.get(concept.story_id)

    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(concept.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(concept.id)+'.png'))
    if concept:
        try:

            db.session.delete(concept)
            db.session.commit()
            flash(f'"{concept.name}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})