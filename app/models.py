
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70))
    password_hash = db.Column(db.String(1000))
    @property
    def password(self):
        raise AttributeError("Not a readable attribute")
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    theme = db.Column(db.String(70), default="css/styles.css")
    stories = db.relationship('Story', backref='user', lazy='dynamic')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  

class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    concepts = db.relationship('Concept', backref='story', lazy='dynamic')
    characters = db.relationship('Character', backref='story', lazy='dynamic')
    groups = db.relationship('Group', backref='story', lazy='dynamic')
    items = db.relationship('Item', backref='story', lazy='dynamic')
    chapters = db.relationship('Chapter', backref='story', lazy='dynamic')
    albums = db.relationship('Album', backref='story', lazy='dynamic')
    def __repr__(self):
        return f'<Story {self.id}>'

class Concept(db.Model):
    __tablename__ = 'concepts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    def __repr__(self):
        return f'<Concept {self.id}>'

inclusions = db.Table('inclusions',
                        db.Column('character_id', db.Integer, db.ForeignKey('characters.id')),
                        db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
                    )

inclusions2 = db.Table('inclusions2',
                        db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
                        db.Column('supgroup_id', db.Integer, db.ForeignKey('supgroups.id'))
                    )

inclusions3 = db.Table('inclusions3',
                        db.Column('item_id', db.Integer, db.ForeignKey('items.id')),
                        db.Column('supitem_id', db.Integer, db.ForeignKey('supitems.id'))
                    )

inclusions4 = db.Table('inclusions4',
                        db.Column('character_id', db.Integer, db.ForeignKey('characters.id')),
                        db.Column('supcharacter_id', db.Integer, db.ForeignKey('supcharacters.id'))
                    )


class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    birthday = db.Column(db.Date)
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    lines = db.relationship('Line', backref='character', lazy='dynamic')
    texts = db.relationship('Text', backref='character', lazy='dynamic')
    illustrations = db.relationship('Illustration', backref='character', lazy='dynamic')
    supcharacters = db.relationship('Supcharacter', 
                             secondary=inclusions4,
                             backref=db.backref('characters', lazy='dynamic'),
                             lazy='dynamic')
    groups = db.relationship('Group', 
                             secondary=inclusions,
                             backref=db.backref('characters', lazy='dynamic'),
                             lazy='dynamic')
    def __repr__(self):
        return f'<Character {self.id}>'


class Illustration(db.Model):
    __tablename__ = 'illustrations'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    image = db.Column(db.LargeBinary)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    def __repr__(self):
        return f'<Illustration {self.id}>'

class Supcharacter(db.Model):
    __tablename__ = 'supcharacters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    def __repr__(self):
        return f'<Supcharacter {self.id}>'


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    supgroups = db.relationship('Supgroup', 
                             secondary=inclusions2,
                             backref=db.backref('groups', lazy='dynamic'),
                             lazy='dynamic')
    def __repr__(self):
        return f'<Group {self.id}>'

class Supgroup(db.Model):
    __tablename__ = 'supgroups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    def __repr__(self):
        return f'<Supgroup {self.id}>'


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    supitems = db.relationship('Supitem', 
                             secondary=inclusions3,
                             backref=db.backref('items', lazy='dynamic'),
                             lazy='dynamic')
    def __repr__(self):
        return f'<Item {self.id}>'

class Supitem(db.Model):
    __tablename__ = 'supitems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    def __repr__(self):
        return f'<Supitem {self.id}>'


class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    serial = db.Column(db.String)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    lines = db.relationship('Line', backref='chapter', lazy='dynamic')
    panels = db.relationship('Panel', backref='chapter', lazy='dynamic')
    def __repr__(self):
        return f'<Chapter {self.id}>'


class Line(db.Model):
    __tablename__ = 'lines'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
    def __repr__(self):
        return f'<Line {self.id}>'


class Panel(db.Model):
    __tablename__ = 'panels'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    illustration = db.Column(db.LargeBinary)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
    divisions = db.relationship('Division', backref='panel', lazy='dynamic')
    def __repr__(self):
        return f'<Panel {self.id}>'


class Division(db.Model):
    __tablename__ = 'divisions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    illustration = db.Column(db.LargeBinary)
    serial = db.Column(db.String)
    panel_id = db.Column(db.Integer, db.ForeignKey('panels.id'))
    texts = db.relationship('Text', backref='division', lazy='dynamic')
    def __repr__(self):
        return f'<Division {self.id}>'


class Text(db.Model):
    __tablename__ = 'texts'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    def __repr__(self):
        return f'<Text {self.id}>'

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    cover = db.Column(db.LargeBinary)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    photos = db.relationship('Photo', backref='album', lazy='dynamic')
    def __repr__(self):
        return f'<Album {self.id}>'

class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    image = db.Column(db.LargeBinary)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    def __repr__(self):
        return f'<Album {self.id}>'
