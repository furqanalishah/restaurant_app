from flask_migrate import Migrate

from web import create_app, db  # noqa

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)