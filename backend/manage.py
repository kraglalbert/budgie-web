import os
from app import create_app, db

# from app.models import User, Role
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv("FLASK_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()


# def make_shell_context():
#     return dict(app=app)
# manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)
if __name__ == "__main__":
    manager.run()
