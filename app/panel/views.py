import os, json

from flask import render_template, request, redirect, url_for, flash, jsonify, current_app

from flask_login import login_required, current_user

from . import panel
from .forms import PanelForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Chapter, Panel, Story
from config import basedir

@panel.route('/', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, int)
    chapter_id = int(request.args.get('id'))
    form = PanelForm()
    chapter = Chapter.query.get(chapter_id)
    story = Story.query.get(chapter.story_id)
    pagination = Panel.query.filter_by(chapter_id=chapter_id).order_by(Panel.title).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    panels = pagination.items
    if form.validate_on_submit():
        panel = Panel(
            title = form.title.data,
            description = form.description.data,
            chapter_id = chapter_id
        )
        db.session.add(panel)
        db.session.commit()
        return redirect(url_for('.index', id=chapter_id))
        
    return render_template('panel/index.html', form=form, story=story, chapter=chapter, panels=panels, pagination=pagination, theme=current_user.theme)


@panel.route('/panel', methods=['GET', 'POST'])
@login_required
def panel_():
    id = int(request.args.get('id'))
    form = PanelForm()
    uForm = UploadForm()
    panel = Panel.query.get(id)
    chapter = Chapter.query.get(panel.chapter_id)
    story = Story.query.filter_by(id=chapter.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Panel.query.filter_by(chapter_id=panel.chapter_id).order_by(Panel.title).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    panels = pagination.items
    uForm = UploadForm()
    if form.validate_on_submit():
        panel.title = request.form['title']
        panel.description = request.form['description']
        db.session.add(panel)
        db.session.commit()
        return redirect(url_for('.panel_', id=panel.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_p'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_p'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.panel_', id=panel.id))
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_p'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_p'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_p'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            panel.illustration = data
            db.session.add(panel)
            db.session.commit()
        if panel.illustration == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_p'+str(id)+'.png'))
            filename = 'images/panel.png'
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_p'+str(id)+'.png'), 'wb') as f:
            if panel.illustration:
                f.write(panel.illustration)
        filename = 'images/panel.png'    
    return render_template('panel/panel.html', form=form, uForm=uForm, story=story, chapter=chapter, panel=panel, panels=panels, pagination=pagination ,filename=filename, theme=current_user.theme)

@panel.route('/delete-panel', methods=['GET', 'POST'])
@login_required
def delete_panel():
    data = json.loads(request.data)
    panel = Panel.query.get(int(data['panel_id']))
    chapter = Chapter.query.get(panel.chapter_id)
    story = Story.query.get(chapter.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_p'+str(panel.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_p'+str(panel.id)+'.png'))
    if chapter:
        try: 
            db.session.delete(panel)
            db.session.commit()
            flash(f'"{panel.title}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})