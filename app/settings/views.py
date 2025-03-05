from flask import render_template, request, redirect, url_for

from flask_login import login_required, current_user


from . import settings

from .. import db
from ..models import User

@settings.route('/', methods=['GET', 'POST'])
@login_required
def index():
    id = request.args.get('id')
    if request.method == 'POST':
        user = User.query.get(id)
        try:
            user.theme = request.form['theme']
            db.session.add(user)
            db.session.commit()
        except:
            pass
        return redirect(url_for('.index'))
    
    return render_template('settings/index.html', theme=current_user.theme)