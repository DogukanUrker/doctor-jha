from helpers import (
    flash,
    randint,
    sqlite3,
    request,
    session,
    redirect,
    Blueprint,
    render_template,
    verifyUserForm,
    message as messageDebugging,
)
from twilio.rest import Client
from tokens import account_sid, auth_token

verifyUserBlueprint = Blueprint("verifyUser", __name__)


@verifyUserBlueprint.route("/verifyUser/codesent=<codeSent>", methods=["GET", "POST"])
def verifyUser(codeSent):
    match "userName" in session:
        case True:
            userName = session["userName"]
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select isVerified from users where lower(username) = "{userName.lower()}"'
            )
            isVerfied = cursor.fetchone()[0]
            match isVerfied:
                case "True":
                    return redirect("/")
                case "False":
                    global verificationCode
                    form = verifyUserForm(request.form)
                    match codeSent:
                        case "true":
                            if request.method == "POST":
                                code = request.form["code"]
                                match code == verificationCode:
                                    case True:
                                        cursor.execute(
                                            f'update users set isVerified = "True" where lower(userName) = "{userName.lower()}"'
                                        )
                                        connection.commit()
                                        messageDebugging(
                                            "2",
                                            f'USER: "{userName}" HAS BEEN VERIFIED',
                                        )
                                        flash(
                                            "Your account has been verified.",
                                            "success",
                                        )
                                        return redirect("/")
                                    case False:
                                        flash("Wrong Code", "error")
                            return render_template(
                                "verifyUser.html", form=form, numberSent=True
                            )
                        case "false":
                            if request.method == "POST":
                                connection = sqlite3.connect("db/users.db")
                                cursor = connection.cursor()
                                cursor.execute(
                                    f'select * from users where lower(userName) = "{userName.lower()}"'
                                )
                                userNameDB = cursor.fetchone()
                                cursor.execute(
                                    f'select number from users where lower(username) = "{userName.lower()}"'
                                )
                                number = cursor.fetchone()
                                match not userNameDB:
                                    case False:
                                        verificationCode = str(randint(1000, 9999))
                                        client = Client(account_sid, auth_token)
                                        message = client.messages.create(
                                            to=number,
                                            from_="+13603835415",
                                            body=f"Your verifiaction code is: {verificationCode}",
                                        )
                                        messageDebugging(
                                            "2",
                                            f'VERIFICATION CODE: "{verificationCode}" SENT TO {number}',
                                        )
                                        flash("code sent", "success")
                                        return redirect("/verifyUser/codesent=true")
                                    case True:
                                        messageDebugging(
                                            "1", f'USER: "{userName}" NOT FOUND'
                                        )
                                        flash("user not found", "error")
                            return render_template(
                                "verifyUser.html", form=form, numberSent=False
                            )
        case False:
            return redirect("/")
