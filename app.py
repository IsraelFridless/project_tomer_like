from controllers.user_controller import user_blueprint
from controllers.question_controller import question_blueprint
from seed_database import fetch_users
from flask import Flask

app = Flask(__name__)


if __name__ == '__main__':
    fetch_users()
    app.register_blueprint(user_blueprint, url_prefix="/api/users")
    app.register_blueprint(question_blueprint, url_prefix="/api/questions")
    app.run(debug=True)


