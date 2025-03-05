import json, os

from flask import render_template, redirect, url_for, request, flash, jsonify, current_app

from flask_login import current_user, login_required

from . import main
from .forms import StoryForm, UploadForm

from .. import db, photos
from ..models import Story, User
from config import basedir

@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        form = StoryForm()
        page = request.args.get('page', 1, type=int)
        pagination = Story.query.order_by(Story.title).filter_by(user_id=current_user.id).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
        stories = pagination.items
        if form.validate_on_submit():
        
            story = Story(title=form.title.data,
                        description=form.description.data,
                        user_id=current_user.id)
            db.session.add(story)
            db.session.commit()
        
            return redirect(url_for('.index'))
        return render_template('main/index.html', form=form, pagination=pagination, stories=stories, theme=current_user.theme)
    else:
        return redirect(url_for('auth.index'))

@main.route('/story', methods=['GET', 'POST'])
@login_required
def story():
    
    form = StoryForm()
    uForm = UploadForm()
    id = int(request.args.get('id'))
    story = Story.query.get(id)
    page = request.args.get('page', 1, int)
    pagination = Story.query.order_by(Story.title).filter_by(user_id=current_user.id).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    stories = pagination.items
    if form.validate_on_submit() and story.user_id == current_user.id:
        story.title = request.form['title']
        story.description = request.form['description']
        db.session.add(story)
        db.session.commit()
        
        return redirect(url_for('.story', id=story.id))
    if uForm.validate_on_submit() and story.user_id == current_user.id:
        file = request.files['file']
        file.filename = str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.story', id=story.id))
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            story.cover = data
            db.session.add(story)
            db.session.commit()
        if story.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(id)+'.png'))
            filename = 'images/story.png' 
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(id)+'.png'), 'wb') as f:
            if story.cover:
                f.write(story.cover)
        filename = 'images/story.png'    
    return render_template('main/story.html', form=form, uForm=uForm, story=story, stories=stories, pagination=pagination, filename=filename, theme=current_user.theme)

@main.route('/delete-story', methods=['GET', 'POST'])
@login_required
def delete_story():
    data = json.loads(request.data)
    story = Story.query.get(int(data['story_id']))

    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'.png'))
    if story and story.user_id == current_user.id:
        try:          
            db.session.delete(story)
            db.session.commit()
            flash(f'"{story.title}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})

