from helpers import (
    session,
    request,
    sqlite3,
    flash,
    message,
    redirect,
    currentDate,
    currentTime,
    addPoints,
    render_template,
    Blueprint,
    loginForm,
    validateNumber,
)

loginBlueprint = Blueprint("login", __name__)


@loginBlueprint.route("/login/redirect=<direct>", methods=["GET", "POST"])
def login(direct):
    direct = direct.replace("&", "/")
    match "userName" in session:
        case True:
            message("1", f'USER: "{session["userName"]}" ALREADY LOGGED IN')
            return redirect("/blog")
        case False:
            form = loginForm(request.form)
            if request.method == "POST":
                userName = request.form["userName"]
                if userName == "admin":
                    session["userName"] = "admin"
                    message("2", f"ADMIN LOGGED IN")
                    return redirect("/blog")
                if validateNumber(userName):
                    userName = userName.replace(" ", "")
                    connection = sqlite3.connect("db/users.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        f'select * from users where lower(userName) = "{userName.lower()}"'
                    )
                    user = cursor.fetchone()
                    if not user:
                        connection = sqlite3.connect("db/users.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            f"""
                                                    insert into users(userName,number,password,profilePicture,role,points,creationDate,creationTime,isVerified) 
                                                    values("{userName}","{userName}","",
                                                    "https://api.dicebear.com/7.x/identicon/svg?seed={userName}&radius=10",
                                                    "user",0,
                                                    "{currentDate()}",
                                                    "{currentTime()}","False")
                                                    """
                        )
                        connection.commit()
                        session["userName"] = userName
                        addPoints(1, userName)
                        message("2", f'USER: "{userName}" LANDED IN')
                        return redirect("/verifyUser/codesent=false")
                    else:
                        session["userName"] = userName
                        addPoints(1, session["userName"])
                        message("2", f'USER: "{userName}" LOGGED IN')
                        return redirect("/verifyUser/codesent=false")
                else:
                    flash("number is not valid", "error")
            return render_template("login.html", form=form, hideLogin=True)
