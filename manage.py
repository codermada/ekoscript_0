

from flask_script import Manager, Shell
from flask_migrate import Migrate, init, migrate, upgrade


from app import create_app, db

from app.models import Story

app = create_app('default')
manager = Manager(app)
migration = Migrate(app, db)


def run_server(host='0.0.0.0', port=5000):
    app.run(host=host, port=port)
    
def shell_make_context():
    return dict(db=db, Story=Story)

def migrations():
    return dict(i=init, m=migrate, u=upgrade)

manager.add_command('shell', Shell(make_context=shell_make_context))
manager.add_command('db', Shell(make_context=migrations))
manager.add_command('run_server', Shell(make_context=run_server))

if __name__ == '__main__':
    manager.run()