from flask import Flask
from flask_login import LoginManager
from climbing_route import ClimbingRoute
from user import User
from climbing_route_dao import ClimbingRouteDao
from user_dao import UserDao
from climbing_route_blueprint import climbing_route_blueprint
from user_blueprint import user_blueprint

app = Flask(__name__)
app.secret_key = 'supersecretkey'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_dao = UserDao('climbing_management.db')
    return user_dao.get_user_by_id(int(user_id))


app.register_blueprint(climbing_route_blueprint)
app.register_blueprint(user_blueprint)


def generate_testdata():
    # Insert DAOs into DB
    route_dao = ClimbingRouteDao('climbing_management.db')
    user_dao = UserDao('climbing_management.db')

    # Generate users
    user_dao.create_user_table()
    user_dao.add_user(User(1, 'admin', 'admin@example', 'admin'))
    user_dao.add_user(User(2, 'user', 'user@example', 'user'))

    # Generate climbing routes
    route_dao.create_table()
    route_dao.add_route(ClimbingRoute(1, 1, 'Easy Route', '5a'), 1)
    route_dao.add_route(ClimbingRoute(2, 1, 'Intermediate Route', '6b'), 1)
    route_dao.add_route(ClimbingRoute(3, 1, 'Advanced Route', '7c'), 1)
    route_dao.add_route(ClimbingRoute(4, 1, 'Expert Route', '8a'), 1)

    route_dao.close()
    user_dao.close()


if __name__ == '__main__':
    generate_testdata()
    app.run(debug=True)
