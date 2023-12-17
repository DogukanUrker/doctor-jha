from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    addPoints,
    currentDate,
    currentTime,
    render_template,
    Blueprint,
    signUpForm,
    sha256_crypt,
)

signUpBlueprint = Blueprint("signup", __name__)


@signUpBlueprint.route("/signup", methods=["GET", "POST"])
def signup():
    match "userName" in session:
        case True:
            message("1", f'USER: "{session["userName"]}" ALREADY LOGGED IN')
            return redirect("/")
        case False:
            form = signUpForm(request.form)
            if request.method == "POST":
                userName = request.form["userName"]
                number = request.form["number"]
                password = request.form["password"]
                userName = userName.replace(" ", "")
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute("select userName from users")
                users = str(cursor.fetchall())
                cursor.execute("select number from users")
                numbers = str(cursor.fetchall())
                if not userName in users and not number in numbers:
                    if password:
                        match userName.isascii():
                            case True:
                                password = sha256_crypt.hash(password)
                                connection = sqlite3.connect("db/users.db")
                                cursor = connection.cursor()
                                cursor.execute(
                                    f"""
                                    insert into users(userName,number,password,profilePicture,role,points,creationDate,creationTime,isVerified) 
                                    values("{userName}","{number}","{password}",
                                    "https://api.dicebear.com/7.x/identicon/svg?seed={userName}&radius=10",
                                    "user",0,
                                    "{currentDate()}",
                                    "{currentTime()}","False")
                                    """
                                )
                                connection.commit()
                                message("2", f'USER: "{userName}" ADDED TO DATABASE')
                                session["userName"] = userName
                                addPoints(1, session["userName"])
                                message("2", f'USER: "{userName}" LOGGED IN')
                                flash(f"Welcome {userName}", "success")
                                return redirect("/verifyUser/codesent=false")
                            case False:
                                message(
                                    "1",
                                    f'USERNAME: "{userName}" DOES NOT FITS ASCII CHARACTERS',
                                )
                                flash("username does not fit ascii charecters", "error")
                elif userName in users and number in numbers:
                    message("1", f'"{userName}" & "{number}" IS UNAVAILABLE ')
                    flash("This username and number is unavailable.", "error")
                elif not userName in users and number in numbers:
                    message("1", f'THIS number "{number}" IS UNAVAILABLE ')
                    flash("This number is unavailable.", "error")
                elif userName in users and not number in numbers:
                    message("1", f'THIS USERNAME "{userName}" IS UNAVAILABLE ')
                    flash("This username is unavailable.", "error")
            return render_template("signup.html", form=form, hideSignUp=True)
