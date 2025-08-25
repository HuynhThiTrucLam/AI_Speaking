from flask import Blueprint
from flask.views import MethodView


audio_bp = Blueprint('audio', __name__)


class Audio(MethodView):
    def post(self):
        return "Hello"


audio_bp.add_url_rule('/audio', view_func=Audio.as_view('audio'))


