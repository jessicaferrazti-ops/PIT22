import os
from flask import Flask
from models.database import init_db
from controllers.routes import bp

def create_app():
    app=Flask(__name__)
    app.secret_key=os.environ.get('SECRET_KEY','dev-key-change-me')
    app.register_blueprint(bp)
    with app.app_context(): init_db()
    return app

app=create_app()
if __name__=='__main__': app.run(debug=True)
