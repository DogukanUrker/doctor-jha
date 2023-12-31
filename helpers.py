import os
import ssl
import smtplib
import secrets
import sqlite3
from os import mkdir
from random import randint
from os.path import exists
from datetime import datetime, timezone, timedelta
from passlib.hash import sha256_crypt
from flask import render_template, Blueprint
from forms import (
    loginForm,
    signUpForm,
    commentForm,
    createPostForm,
    verifyUserForm,
    passwordResetForm,
    changePasswordForm,
    changeUserNameForm,
    changeProfilePictureForm,
)
from flask import (
    Flask,
    flash,
    request,
    session,
    redirect,
    Blueprint,
    render_template,
    send_from_directory,
)

import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

timezone_offset = 5.5
tzinfo = timezone(timedelta(hours=timezone_offset))


def currentDate():
    return datetime.now(tzinfo).strftime("%d.%m.%y")


def currentTime(seconds=False):
    match seconds:
        case False:
            return datetime.now(tzinfo).strftime("%H:%M")
        case True:
            return datetime.now(tzinfo).strftime("%H:%M:%S")


def message(color, message):
    print(
        f"\n\033[94m[{currentDate()}\033[0m"
        f"\033[95m {currentTime(True)}]\033[0m"
        f"\033[9{color}m {message}\033[0m\n"
    )
    logFile = open("log.log", "a", encoding="utf-8")
    logFile.write(f"[{currentDate()}" f"|{currentTime(True)}]" f" {message}\n")
    logFile.close()


def addPoints(points, user):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'update users set points = points+{points} where userName = "{user}"'
    )
    connection.commit()
    message("2", f'{points} POINTS ADDED TO "{user}"')


def validateNumber(number):
    try:
        carrier._is_mobile(number_type(phonenumbers.parse(number)))
        return True
    except:
        return False


def getProfilePicture(userName):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'select profilePicture from users where lower(userName) = "{userName.lower()}"'
    )
    return cursor.fetchone()[0]
