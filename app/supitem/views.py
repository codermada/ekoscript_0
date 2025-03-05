import json, os

from flask import render_template, request, url_for, flash, redirect, jsonify, current_app

from flask_login import login_required, current_user

from . import supitem
from .forms import SupitemForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Story, Supitem
from config import basedir

@supitem.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SupitemForm()
    page = request.args.get('page', 1, int)
    story_id = int(request.args.get('id'))
    story = Story.query.get(story_id)
    pagination = Supitem.query.filter_by(story_id=story_id).order_by(Supitem.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    supitems = pagination.items
    if form.validate_on_submit():
        supitem = Supitem(
            name = form.name.data,
            description = form.description.data,
            story_id = story_id
        )
        
        db.session.add(supitem)
        db.session.commit()
        
        return redirect(url_for('supitem.index', id=story_id))
    return render_template('supitem/index.html', story=story, form=form, pagination=pagination, supitems=supitems, theme=current_user.theme)

@supitem.route('/supitem', methods=['GET', 'POST'])
@login_required
def supitem_():
    id = int(request.args.get('id'))
    form = SupitemForm()
    uForm = UploadForm()
    supitem = Supitem.query.get(id)
    story = Story.query.filter_by(id=supitem.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Supitem.query.filter_by(story_id=supitem.story_id).order_by(Supitem.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    supitems = pagination.items
    if form.validate_on_submit():
        supitem.name = request.form['name']
        supitem.description = request.form['description']
        db.session.add(supitem)
        db.session.commit()
        
        return redirect(url_for('.supitem_', id=supitem.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_si'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_si'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.supitem_', id=supitem.id))
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_si'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_si'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_si'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            supitem.cover = data
            db.session.add(supitem)
            db.session.commit()
        if supitem.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_si'+str(id)+'.png'))
            filename = 'images/character.png'
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_si'+str(id)+'.png'), 'wb') as f:
            if supitem.cover:
                f.write(supitem.cover)
        filename = 'images/supitem.png'    
    return render_template('supitem/supitem.html', form=form, uForm=uForm, story=story, supitem=supitem, supitems=supitems, n_items = len(supitem.items.all()), pagination=pagination, filename=filename, theme=current_user.theme)

@supitem.route('/delete-supitem', methods=['GET', 'POST'])
@login_required
def delete_supitem():
    data = json.loads(request.data)
    supitem = Supitem.query.get(int(data['supitem_id']))
    story = Story.query.get(supitem.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_si'+str(supitem.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_si'+str(supitem.id)+'.png'))
    if supitem:
        try:
           
            db.session.delete(supitem)
            db.session.commit()
            flash(f'"{supitem.name}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})