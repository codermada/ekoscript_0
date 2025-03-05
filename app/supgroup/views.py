import json, os

from flask import render_template, request, url_for, flash, redirect, jsonify, current_app

from flask_login import login_required, current_user

from . import supgroup
from .forms import SupgroupForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Story, Supgroup
from config import basedir

@supgroup.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SupgroupForm()
    page = request.args.get('page', 1, int)
    story_id = int(request.args.get('id'))
    story = Story.query.get(story_id)
    pagination = Supgroup.query.filter_by(story_id=story_id).order_by(Supgroup.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    supgroups = pagination.items
    if form.validate_on_submit():
        
        supgroup = Supgroup(
            name = form.name.data,
            description = form.description.data,
            story_id = story_id
        )
        db.session.add(supgroup)
        db.session.commit()
        return redirect(url_for('supgroup.index', id=story_id))
    return render_template('supgroup/index.html', story=story, form=form, pagination=pagination, supgroups=supgroups, theme=current_user.theme)

@supgroup.route('/supgroup', methods=['GET', 'POST'])
@login_required
def supgroup_():
    id = int(request.args.get('id'))
    form = SupgroupForm()
    uForm = UploadForm()
    supgroup = Supgroup.query.get(id)
    story = Story.query.filter_by(id=supgroup.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Supgroup.query.filter_by(story_id=supgroup.story_id).order_by(Supgroup.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    supgroups = pagination.items
    if form.validate_on_submit():
        supgroup.name = request.form['name']
        supgroup.description = request.form['description']
        db.session.add(supgroup)
        db.session.commit()
        return redirect(url_for('.supgroup_', id=supgroup.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_sg'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sg'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.supgroup_', id=supgroup.id))
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sg'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_sg'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sg'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            supgroup.cover = data
            db.session.add(supgroup)
            db.session.commit()
        if supgroup.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sg'+str(id)+'.png'))
            filename = 'images/supgroup.png'
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sg'+str(id)+'.png'), 'wb') as f:
            if supgroup.cover:
                f.write(supgroup.cover)
        filename = 'images/supgroup.png'    
    return render_template('supgroup/supgroup.html', form=form, uForm=uForm, story=story, supgroup=supgroup, n_groups=len(supgroup.groups.all()),supgroups=supgroups, pagination=pagination, filename=filename, theme=current_user.theme)

@supgroup.route('/delete-supgroup', methods=['GET', 'POST'])
@login_required
def delete_supgroup():
    data = json.loads(request.data)
    supgroup = Supgroup.query.get(int(data['supgroup_id']))
    story = Story.query.get(supgroup.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sg'+str(supgroup.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_sg'+str(supgroup.id)+'.png'))
    if supgroup:
        try:
            db.session.delete(supgroup)
            db.session.commit()
            flash(f'"{supgroup.name}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})