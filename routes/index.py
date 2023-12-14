from helpers import (
    sqlite3,
    render_template,
    Blueprint,
    session,
)

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/")
def index():
    match "userName" in session:
        case True:
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute("select * from posts")
            posts = cursor.fetchall()
            return render_template(
                "index.html",
                posts=posts,
            )
        case False:
            return render_template("home.html")
