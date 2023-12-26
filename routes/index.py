from helpers import (
    sqlite3,
    render_template,
    Blueprint,
    session,
)

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/blog")
def index():
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    anyPost = True
    if posts == []:
        anyPost = False
    return render_template(
        "index.html",
        posts=posts,
        anyPost=anyPost,
    )
