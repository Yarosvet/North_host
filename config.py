from flask import Flask, render_template, redirect, request, abort, send_file
import datetime
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import os
#  LOCAL
from forms import LoginForm, RegForm, ChangePassForm, UploadFileForm
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '77ac4973981o3xu7s1aj55o7cg76592z612wt4jg486u91u615j5587zh696x6q4'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
#  Папка выгруженных файлов
app.config['UPLOAD_FOLDER'] = "files/"
login_manager = LoginManager()
login_manager.init_app(app)
#  Максимальный размер файла
MAX_FILE_SIZE = 1024 * 1024 + 1
#  Домен, на котором располагается сайт (обязательно для работы)
domain = "north-host.herokuapp.com"
