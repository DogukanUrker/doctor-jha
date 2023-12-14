from helpers import (
    sqlite3,
    render_template,
    Blueprint,
)

homeBlueprint = Blueprint("home", __name__)


@homeBlueprint.route("/home")
def home():
    return render_template(
        "home.html",
    )
