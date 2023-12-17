from helpers import (
    render_template,
    Blueprint,
)

homeBlueprint = Blueprint("home", __name__)


@homeBlueprint.route("/home")
def home():
    return render_template(
        "home.html",
    )
