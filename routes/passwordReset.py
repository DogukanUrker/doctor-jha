from helpers import (
    flash,
    randint,
    sqlite3,
    request,
    redirect,
    Blueprint,
    sha256_crypt,
    render_template,
    passwordResetForm,
    message as messageDebugging,
)
from twilio.rest import Client
from tokens import account_sid, auth_token

passwordResetBlueprint = Blueprint("passwordReset", __name__)


@passwordResetBlueprint.route(
    "/passwordreset/codesent=<codeSent>", methods=["GET", "POST"]
)
def passwordReset(codeSent):
    global userName
    global passwordResetCode
    form = passwordResetForm(request.form)
    match codeSent:
        case "true":
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            if request.method == "POST":
                code = request.form["code"]
                password = request.form["password"]
                passwordConfirm = request.form["passwordConfirm"]
                match code == passwordResetCode:
                    case True:
                        cursor.execute(
                            f'select password from users where lower(userName) = "{userName.lower()}"'
                        )
                        oldPassword = cursor.fetchone()[0]
                        match password == passwordConfirm:
                            case True:
                                match sha256_crypt.verify(password, oldPassword):
                                    case True:
                                        flash(
                                            "new password can not be same with old password",
                                            "error",
                                        )
                                    case False:
                                        password = sha256_crypt.hash(password)
                                        cursor.execute(
                                            f'update users set password = "{password}" where lower(userName) = "{userName.lower()}"'
                                        )
                                        connection.commit()
                                        messageDebugging(
                                            "2",
                                            f'USER: "{userName}" CHANGED HIS PASSWORD',
                                        )
                                        flash(
                                            "you need login with new password",
                                            "success",
                                        )
                                        return redirect("/login/redirect=&")
                            case False:
                                flash("passwords must match", "error")
                    case False:
                        flash("Wrong Code", "error")
            return render_template("passwordReset.html", form=form, numberSent=True)
        case "false":
            if request.method == "POST":
                userName = request.form["userName"]
                number = request.form["number"]
                userName = userName.replace(" ", "")
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute(
                    f'select * from users where lower(userName) = "{userName.lower()}"'
                )
                userNameDB = cursor.fetchone()
                cursor.execute(
                    f'select * from users where lower(number) = "{number.lower()}"'
                )
                numberDB = cursor.fetchone()
                match not userNameDB or not numberDB:
                    case False:
                        passwordResetCode = str(randint(1000, 9999))
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                            to=number,
                            from_="+12058805093",
                            body=f"Your verifiaction code is: {passwordResetCode}",
                        )
                        messageDebugging(
                            "2",
                            f'VERIFICATION CODE: "{passwordResetCode}" SENT TO {number}',
                        )
                        flash("code sent", "success")
                        return redirect("/passwordreset/codesent=true")
                    case True:
                        messageDebugging("1", f'USER: "{userName}" NOT FOUND')
                        flash("user not found", "error")
            return render_template("passwordReset.html", form=form, numberSent=False)
