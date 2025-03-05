import json, os

from flask import render_template, request, url_for, flash, redirect, jsonify, current_app

from flask_login import login_required, current_user

from . import group
from .forms import GroupForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Story, Group, Supgroup
from config import basedir


@group.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = GroupForm()
    page = request.args.get('page', 1, int)
    story_id = int(request.args.get('id'))
    story = Story.query.get(story_id)
    pagination = Group.query.filter_by(story_id=story_id).order_by(Group.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    groups = pagination.items
    if form.validate_on_submit():
        group = Group(
            name = form.name.data,
            description = form.description.data,
            story_id = story_id
        )
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('group.index', id=story_id))
    return render_template('group/index.html', story=story, form=form, pagination=pagination, groups=groups, theme=current_user.theme)

@group.route('/group', methods=['GET', 'POST'])
@login_required
def group_():
    id = int(request.args.get('id'))
    form = GroupForm()
    uForm = UploadForm()
    group = Group.query.get(id)
    story = Story.query.filter_by(id=group.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Group.query.filter_by(story_id=group.story_id).order_by(Group.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    groups = pagination.items
    supgroups = Supgroup.query.filter_by(story_id=story.id).all()
    if len(group.supgroups.all()) != 0:
        entered_supgroups = True
    else:
        entered_supgroups = False
    if form.validate_on_submit():
        group.name = request.form['name']
        group.description = request.form['description']
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('.group_', id=group.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_g'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_g'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.group_', id=group.id))
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_g'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_g'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_g'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            group.cover = data
            db.session.add(group)
            db.session.commit()
        if group.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_g'+str(id)+'.png'))
            filename = 'images/group.png'
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_g'+str(id)+'.png'), 'wb') as f:
            if group.cover:
                f.write(group.cover)
        filename = 'images/group.png'    
    return render_template('group/group.html', form=form, uForm=uForm, story=story, entered_supgroups=entered_supgroups, group=group, n_members=len(group.characters.all()), groups=groups, supgroups=supgroups, pagination=pagination, filename=filename, theme=current_user.theme)

@group.route('/delete-group', methods=['GET', 'POST'])
@login_required
def delete_group():
    data = json.loads(request.data)
    group = Group.query.get(int(data['group_id']))
    story = Story.query.get(group.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_g'+str(group.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_g'+str(group.id)+'.png'))
    if group:
        try:
            
            db.session.delete(group)
            db.session.commit()
            flash(f'"{group.name}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})

@group.route('/inclusion', methods=['GET', 'POST'])
@login_required
def inclusion():
    data = json.loads(request.data)
    group = Group.query.get(int(data['group_id']))
    supgroup = Supgroup.query.get(int(data['supgroup_id']))
    group.supgroups.append(supgroup)
    db.session.add(group)
    db.session.commit()
    return jsonify({})

@group.route('/exclusion', methods=['GET', 'POST'])
@login_required
def exclusion():
    data = json.loads(request.data)
    group = Group.query.get(int(data['group_id']))
    supgroup = Supgroup.query.get(int(data['supgroup_id']))
    group.supgroups.remove(supgroup)
    db.session.add(group)
    db.session.commit()
    return jsonify({})