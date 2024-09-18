from controllers.user_controller import user_blueprint
from controllers.question_controller import question_blueprint
import seed_database as seed
from flask import Flask
from repository.database import create_tables

app = Flask(__name__)


if __name__ == '__main__':
    create_tables()
    app.register_blueprint(user_blueprint, url_prefix="/api/users")
    app.register_blueprint(question_blueprint, url_prefix="/api/questions")
    app.run(debug=True)


