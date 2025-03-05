import json, os

from flask import render_template, request, url_for, flash, redirect, jsonify, current_app, send_file
from itsdangerous import TimedSerializer


from flask_login import login_required, current_user

from . import division
from .forms import DivisionForm

from ..main.forms import UploadForm
from ..chapter.forms import TextForm
from .. import db, photos
from ..models import Character, Story, Chapter, Panel, Division, Text
from config import basedir


@division.route('/', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, int)
    panel_id = int(request.args.get('id'))
    form = DivisionForm()
    panel = Panel.query.get(panel_id)
    chapter = Chapter.query.get(panel.chapter_id)
    story = Story.query.get(chapter.story_id)
    pagination = Division.query.filter_by(panel_id=panel_id).order_by(Division.title).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    divisions = pagination.items
    if form.validate_on_submit():
        division = Division(
            title = form.title.data,
            description = form.description.data,
            panel_id = panel_id
        )
        db.session.add(division)
        db.session.commit()
        return redirect(url_for('.index', id=panel_id))
        
    return render_template('division/index.html', form=form, story=story, chapter=chapter, panel=panel, divisions=divisions, pagination=pagination, theme=current_user.theme)


@division.route('/division', methods=['GET', 'POST'])
@login_required
def division_():
    id = int(request.args.get('id'))
    form = DivisionForm()
    uForm = UploadForm()
    division = Division.query.get(id)
    panel = Panel.query.get(division.panel_id)
    chapter = Chapter.query.get(panel.chapter_id)
    story = Story.query.get(chapter.story_id)
    page = request.args.get('page', 1, int)
    pagination = Division.query.filter_by(panel_id=division.panel_id).order_by(Division.title).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    divisions = pagination.items
    if form.validate_on_submit():
        division.title = request.form['title']
        division.description = request.form['description']
       
        db.session.add(division)
        db.session.commit()
        return redirect(url_for('.division_', id=division.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_d'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_d'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.division_', id=division.id))
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_d'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_d'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_d'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            division.illustration = data
            db.session.add(division)
            db.session.commit()
        if division.illustration == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_d'+str(id)+'.png'))
            filename = 'images/division.png' 
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_d'+str(id)+'.png'), 'wb') as f:
            if division.illustration:
                f.write(division.illustration)
        filename = 'images/division.png'    
    return render_template('division/division.html', form=form, uForm=uForm, story=story, chapter=chapter, panel=panel, division=division, divisions=divisions, pagination=pagination, filename=filename, theme=current_user.theme) 


@division.route('/delete-division', methods=['GET', 'POST'])
@login_required
def delete_division():
    
    data = json.loads(request.data)
    division = Division.query.get(int(data['division_id']))
    panel = Panel.query.get(division.panel_id)
    chapter = Chapter.query.get(panel.chapter_id)
    story = Story.query.get(chapter.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_d'+str(division.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_d'+str(division.id)+'.png'))
    if division:
        try:
           
            db.session.delete(division)
            db.session.commit()
            flash(f'"{division.title}" deleted successfully', category='info')

        except:
            pass
    return jsonify({})

@division.route('/text', methods=['GET', 'POST'])
@login_required
def text():  
    id = request.args.get('id')
    division = Division.query.get(id)
    panel = Panel.query.get(division.panel_id)
    chapter = Chapter.query.get(panel.chapter_id)
    story = Story.query.get(chapter.story_id)
    list = ['introduction', 'action' ,'noise', 'description']
    temp = []
    for i in list:
        temp.append(i)
    characters = Character.query.filter_by(story_id=story.id).all()
    texts = Text.query.filter_by(division_id=division.id).all()
    for character in characters:
        list.append(character.name)
    form = TextForm(list)
    if form.validate_on_submit():
        header = form.header.data
        if header in temp:
            text = form.text.data
            if header == 'introduction':
                text = 'INTRO | ' + text.upper() + ' |'
            elif header == 'action':
                text = '* ' + text.lower() + ' *'
            elif header == 'noise':
                text = '( '+ text.lower() + ' )'
            elif header == 'description':
                text = 'DESC - ' + text.lower() + ' -'
            character_id = None
        else:
            text = form.text.data
            text = header + ' : ' + text
            character_id = Character.query.filter_by(name=form.header.data).first().id
        text = Text(
            text = text,
            character_id = character_id, 
            division_id = id)
        db.session.add(text)
        db.session.commit()
        return redirect(url_for('division.text', id=id))
    return render_template('division/text.html',form=form , story=story, chapter=chapter, panel=panel, division=division, texts=texts, theme=current_user.theme)

@division.route('/full-text', methods=['GET', 'POST'])
@login_required
def full_text():
    id = request.args.get('id')
    division = Division.query.get(id)
    panel = Panel.query.get(division.panel_id)
    chapter = Chapter.query.get(panel.chapter_id)
    story_id = chapter.story_id
    story = Story.query.get(story_id)
    texts = Text.query.filter_by(division_id=id).all()
    serializer =  TimedSerializer(current_app.config['SECRET_KEY'], b"full_text")
    serial = serializer.dumps({"full_text_div":str(story.id)+'_'+str(chapter.id)+'_'+str(panel.id)+'_'+str(division.id)})
    data = serializer.loads(serial) 
    new_full_text_filename = 'full_text_div_'+serial.split('}')[1]+'.txt'
    if division.serial != None:
        old_full_text_filename = 'full_text_div_'+division.serial.split('}')[1]+'.txt'
    else:
        old_full_text_filename = 'tmp.txt'
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+old_full_text_filename)):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+old_full_text_filename))
    division.serial = serial
    db.session.add(division)
    db.session.commit()
    
    with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+new_full_text_filename), 'a') as file:
        file.write(chapter.title+' '+panel.title+' '+division.title+'\n\n')
        count = 0
        for line in texts:
            if line.text == '':
                if count == 1:
                    file.write("\n")
                count += 1
            else:
                file.write(line.text)
                file.write("\n")
    return render_template('division/full-text.html', story=story, chapter=chapter, panel=panel, division=division, texts=texts, theme=current_user.theme, serial=serial)


@division.route('/download_full_text', methods=['GET', 'POST'])
@login_required
def download_full_text():
    division_id = request.args.get('id')
    serial = request.args.get('serial')
    division = Division.query.get(division_id)
    panel = Panel.query.get(division.panel_id)
    chapter = Chapter.query.get(panel.chapter_id)
    story_id = chapter.story_id
    story = Story.query.get(story_id)
    texts = Text.query.filter_by(division_id=division_id).all()
    serial = division.serial
    serializer =  TimedSerializer(current_app.config['SECRET_KEY'], b"full_text")
    data = serializer.loads(division.serial) 
    return send_file(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/full_text_div_'+serial.split('}')[1]+'.txt'), as_attachment=True, download_name='full_text'+'_'+chapter.title+'_'+panel.title+'_'+division.title+'.txt')


@division.route('/erase', methods=['GET', 'POST'])
@login_required
def erase():
    data = json.loads(request.data)
    id = data['text_id']
    text = Text.query.get(id)
    text.text = ""
    db.session.add(text)
    db.session.commit()
    return jsonify({})


@division.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    data = json.loads(request.data)
    id = data['text_id']
    text = Text.query.get(id)
    text.text = data['text']
    db.session.add(text)
    db.session.commit()
    return jsonify({})