from helpers import (
    render_template,
    Blueprint,
)

directMessageBlueprint = Blueprint("directMessage", __name__)


@directMessageBlueprint.route("/directMessage")
def directMessage():
    return render_template("directMessage.html")
