import json, os

from flask import render_template, request, url_for, flash, redirect, jsonify, current_app

from flask_login import login_required, current_user

from . import item
from .forms import ItemForm
from app.main.forms import UploadForm

from .. import db, photos
from ..models import Story, Item, Supitem
from config import basedir

@item.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ItemForm()
    page = request.args.get('page', 1, int)
    story_id = int(request.args.get('id'))
    story = Story.query.get(story_id)
    pagination = Item.query.filter_by(story_id=story_id).order_by(Item.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    items = pagination.items
    if form.validate_on_submit():
        item = Item(
            name = form.name.data,
            description = form.description.data,
            story_id = story_id
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('item.index', id=story_id))
    return render_template('item/index.html', story=story, form=form, pagination=pagination, items=items, theme=current_user.theme)

@item.route('/item', methods=['GET', 'POST'])
@login_required
def item_():
    id = int(request.args.get('id'))
    form = ItemForm()
    uForm = UploadForm()
    item = Item.query.get(id)
    story = Story.query.filter_by(id=item.story_id).first()
    page = request.args.get('page', 1, int)
    pagination = Item.query.filter_by(story_id=item.story_id).order_by(Item.name).paginate(page=page, per_page=current_app.config['PER_PAGE'], error_out=False)
    items = pagination.items
    supitems = Supitem.query.filter_by(story_id=story.id).all()
    if len(item.supitems.all()) != 0:
        entered_supitems = True
    else:
        entered_supitems = False
    if form.validate_on_submit():
        item.name = request.form['name']
        item.description = request.form['description']
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('.item_', id=item.id))
    if uForm.validate_on_submit():
        file = request.files['file']
        file.filename = str(story.id)+'_i'+str(id)+'.png'
        try:
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_i'+str(id)+'.png')) 
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        except:
            photos.save(storage=file, name=file.filename, folder=str(current_user.id))
        return redirect(url_for('.item_', id=item.id))
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_i'+str(id)+'.png')):
        filename = 'tmp/'+str(current_user.id)+'/'+str(story.id)+'_i'+str(id)+'.png'
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_i'+str(id)+'.png'), 'rb') as f:
            data = f.read()
            item.cover = data
            db.session.add(item)
            db.session.commit()
        if item.cover == b'':
            os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_i'+str(id)+'.png'))
            filename = 'images/item.png' 
    else:
        with open(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_i'+str(id)+'.png'), 'wb') as f:
            if item.cover:
                f.write(item.cover)
        filename = 'images/item.png'    
    return render_template('item/item.html', form=form, uForm=uForm, story=story, item=item, items=items, supitems=supitems, entered_supitems=entered_supitems, pagination=pagination, filename=filename, theme=current_user.theme)

@item.route('/delete-item', methods=['GET', 'POST'])
@login_required
def delete_item():
    data = json.loads(request.data)
    item = Item.query.get(int(data['item_id']))
    story = Story.query.get(item.story_id)
    if os.path.exists(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_i'+str(id)+'.png')):
        os.remove(os.path.join(basedir, 'app/static/tmp/'+str(current_user.id)+'/'+str(story.id)+'_i'+str(item.id)+'.png'))
    if item:
        try:
            
            db.session.delete(item)
            db.session.commit()
            flash(f'"{item.name}" deleted successfully', category='info')
        except:
            pass
    return jsonify({})

@item.route('/inclusion', methods=['GET', 'POST'])
@login_required
def inclusion():
    data = json.loads(request.data)
    item = Item.query.get(int(data['item_id']))
    supitem = Supitem.query.get(int(data['supitem_id']))
    item.supitems.append(supitem)
    db.session.add(item)
    db.session.commit()
    return jsonify({})

@item.route('/exclusion', methods=['GET', 'POST'])
@login_required
def exclusion():
    data = json.loads(request.data)
    item = Item.query.get(int(data['item_id']))
    supitem = Supitem.query.get(int(data['supitem_id']))
    item.supitems.remove(supitem)
    db.session.add(item)
    db.session.commit()
    return jsonify({})