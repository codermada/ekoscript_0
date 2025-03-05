
import json, os

from flask import render_template, redirect, url_for, request, flash, jsonify, current_app, send_file
from itsdangerous import TimedSerializer

from flask_login import login_required, current_user

from . import chapter
from .forms import ChapterForm, TextForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Character, Line, Story, Chapter
from config import basedir



@chapter.route('/', methods=['GET', 'POST'])
@login_required
def index():
    story_id = int(request.args.get('id'))
    story = Story.query.get(story_id)
    form = ChapterForm()
    page = request.args.get('page', 1, type=int)
    pagination = Chapter.query.filter_by(story_id=story_id).order_by(Chapter.title).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    chapters = pagination.items
    if form.validate_on_submit():
      
        chapter = Chapter(title=form.title.data,
                    description=form.description.data,
                    story_id=story_id)
        db.session.add(chapter)
        db.session.commit()
        return redirect(url_for('chapter.index', id=story_id))
    return render_template('chapter/index.html', story=story, form=form, pagination=pagination, chapters=chapters, theme=current_user.theme)



@chapter.route('/chapter', methods=['GET', 'POST'])
@login_required
def chapter_():
    id = int(request.args.get('id'))
    form = ChapterForm()
    uForm = UploadForm()
    chapter = Chapter.query.get(id)
    story = Story.query.filter_by(id=chapter.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Chapter.query.filter_by(story_id=chapter.story_id).order_by(Chapter.title).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    chapters = pagination.items
    
    if form.validate_on_submit():
        chapter.title = request.form['title']
        chapter.description = request.form['description']
        db.session.add(chapter)
        db.session.commit()
        return redirect(url_for('.chapter_', id=chapter.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_cp'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.chapter_', id=chapter.id))
    
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            chapter.cover = data
            db.session.add(chapter)
            db.session.commit()
        if chapter.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png')) 
            filename = 'images/chapter.png' 
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(id)+'.png'), 'wb') as f:
            if chapter.cover:
                f.write(chapter.cover)
        filename = 'images/chapter.png'    
    return render_template('chapter/chapter.html', form=form, uForm=uForm, story=story, chapter=chapter, chapters=chapters, pagination=pagination, filename=filename, theme=current_user.theme)



@chapter.route('/delete-chapter', methods=['GET', 'POST'])
@login_required
def delete_chapter():
    data = json.loads(request.data)
    chapter = Chapter.query.get(int(data['chapter_id']))
    story = Story.query.get(chapter.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(chapter.id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_cp'+str(chapter.id)+'.png'))
    if chapter:
        try:
            db.session.delete(chapter)
            db.session.commit()
            flash(f'"{chapter.title}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})


@chapter.route('/text', methods=['GET', 'POST'])
@login_required
def text():  
    chapter_id = request.args.get('id')
    chapter = Chapter.query.get(chapter_id)
    story_id = chapter.story_id
    story = Story.query.get(story_id)
    list = ['introduction', 'action' ,'noise', 'description']
    temp = []
    for i in list:
        temp.append(i)
    characters = Character.query.filter_by(story_id=story_id).all()
    lines = Line.query.filter_by(chapter_id=chapter_id).all()
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
        line = Line(
            text = text,
            character_id = character_id, 
            chapter_id = chapter_id)
        db.session.add(line)
        db.session.commit()
        return redirect(url_for('chapter.text', id=chapter_id))
    return render_template('chapter/text.html', story=story, chapter=chapter, form=form, lines=lines, theme=current_user.theme)


@chapter.route('/full-text', methods=['GET', 'POST'])
@login_required
def full_text():
    chapter_id = request.args.get('id')
    chapter = Chapter.query.get(chapter_id)
    story_id = chapter.story_id
    story = Story.query.get(story_id)
    lines = Line.query.filter_by(chapter_id=chapter_id).all()
    serializer =  TimedSerializer(current_app.config['SECRET_KEY'], b"full_text")
    serial = serializer.dumps({"full_text":str(story.id)+'_cp'+str(chapter.id)})
    data = serializer.loads(serial) 
    new_full_text_filename = 'full_text_'+serial.split('}')[1]+'.txt'
    
    if chapter.serial != None:
        old_full_text_filename = 'full_text_'+chapter.serial.split('}')[1]+'.txt'
    else:
        old_full_text_filename = 'tmp.txt'
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+old_full_text_filename)):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+old_full_text_filename))
    chapter.serial = serial
    db.session.add(chapter)
    db.session.commit()
    
    with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+new_full_text_filename), 'a') as file:
        file.write(chapter.title+'\n\n')
        count = 0
        for line in lines:
            if line.text == '':
                if count == 1:
                    file.write("\n")
                count += 1
            else:
                if line.text:
                    file.write(line.text)
                    file.write("\n")
    return render_template('chapter/full-text.html', story=story, chapter=chapter, lines=lines, theme=current_user.theme, serial=serial)

@chapter.route('/download_full_text', methods=['GET', 'POST'])
@login_required
def download_full_text():
    chapter_id = request.args.get('id')
    serial = request.args.get('serial')
    chapter = Chapter.query.get(chapter_id)
    story_id = chapter.story_id
    story = Story.query.get(story_id)
    lines = Line.query.filter_by(chapter_id=chapter_id).all()
    serializer =  TimedSerializer(current_app.config['SECRET_KEY'], b"full_text")
    data = serializer.loads(chapter.serial) 
    return send_file(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/full_text_'+serial.split('}')[1]+'.txt'), as_attachment=True, download_name='full_text'+'_cp'+chapter.title+'.txt')


@chapter.route('/erase', methods=['GET', 'POST'])
@login_required
def erase():
    data = json.loads(request.data)
    id = int(data['line_id'])
    line = Line.query.get(id)
    line.text = ""
    db.session.add(line)
    db.session.commit()
    return jsonify({})


@chapter.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    data = json.loads(request.data)
    id = int(data['line_id'])
    line = Line.query.get(id)
    line.text = data['text']
    db.session.add(line)
    db.session.commit()
    return jsonify({})
