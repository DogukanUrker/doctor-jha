from wtforms import validators, Form, StringField, PasswordField, TextAreaField


class commentForm(Form):
    comment = TextAreaField(
        "Comment",
        [validators.Length(min=1, max=500), validators.InputRequired()],
        render_kw={"placeholder": ""},
    )


class loginForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "number"},
    )


class createPostForm(Form):
    postTitle = StringField(
        "Post Title",
        [validators.Length(min=4, max=75), validators.InputRequired()],
        render_kw={"placeholder": "title"},
    )
    postContent = TextAreaField(
        "Post Content",
        [validators.Length(min=50)],
    )


class passwordResetForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "name"},
    )
    number = StringField(
        "Number",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"placeholder": "Phone Number"},
    )
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()],
        render_kw={"placeholder": "code"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "confirm your password"},
    )


class verifyUserForm(Form):
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()],
        render_kw={"placeholder": "code"},
    )


class changePasswordForm(Form):
    oldPassword = PasswordField(
        "oldPassword",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "old password"},
    )
    password = PasswordField(
        "password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "new password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "confirm your password"},
    )


class changeUserNameForm(Form):
    newUserName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "name"},
    )


class changeProfilePictureForm(Form):
    newProfilePictureSeed = StringField(
        "ProfilePictureSeed",
        [validators.InputRequired()],
        render_kw={"placeholder": "text"},
    )


class signUpForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "name"},
    )
    number = StringField(
        "Number",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"placeholder": "number"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "password"},
    )
