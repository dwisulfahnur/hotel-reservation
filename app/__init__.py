from app.core.helper import create_app
from app.core.db import db
from app.core.json import json_respon

from app.user.views import user_views
from app.user.models import*
from app.user.loginmanager import login_manager

from app.hotel.views import hotel_views
from app.hotel.models import*

from app.reservation.views import reservation_views
from app.reservation.models import*

config = 'app.config'
app = create_app(config)
db.init_app(app)
login_manager.init_app(app)

# register blueprint
app.register_blueprint(user_views)
app.register_blueprint(hotel_views)
app.register_blueprint(reservation_views)

@app.errorhandler(401)
def say_401(error):
    return json_respon(code=401, msg="You must login to access this url")

@app.errorhandler(404)
def say_404(error):
    return json_respon(code=404, msg=error.description)

@app.errorhandler(405)
def say_405(error):
    return json_respon(code=405, msg=error.description)

@app.errorhandler(500)
def say_500(error):
    return json_respon(code=500, msg=error.description)
