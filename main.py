from config import *


def get_file_class(file_id):
    session = db_session.create_session()
    file = session.query(Files).get(file_id)
    return file


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/cabinet')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/cabinet")
        return render_template('login.html',
                               message="Неверный логин или пароль",
                               form=form)
        return redirect('/cabinet')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='NorthHost - Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.username.data).first():
            return render_template('register.html', title='NorthHost - Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.username.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', form=form, title='NorthHost - Регистрация')


@app.route('/cabinet')
@login_required
def cabinet():
    return render_template('cabinet.html')


@app.route('/cabinet/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('change_password.html', form=form,
                                   message="Пароли не совпадают")
        elif not current_user.check_password(form.old_password.data):
            return render_template('change_password.html', form=form,
                                   message="Старый пароль введен неверно")
        user_id = current_user.id
        mess = current_user.change_password(user_id, form.password.data)
        if mess:
            return render_template('change_password.html', form=form,
                                   message=str(mess))
        return redirect('/')
    return render_template('change_password.html', form=form)


@app.route('/cabinet/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file
        obj = Files(filename=file.data.filename, user_id=current_user.id, is_private=form.is_private.data,
                    comment=form.comment.data)
        if not file.has_file():
            return render_template('upload_file.html', form=form, message="Выберите файл!")
        if file.data.content_length > MAX_FILE_SIZE:
            return render_template('upload_file.html',
                                   message=f'Размер файла превышает максимальный ({MAX_FILE_SIZE} байт)', form=form)
        session = db_session.create_session()
        session.add(obj)
        session.merge(current_user)
        session.commit()
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], str(obj.id)))
        file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], str(obj.id), file.data.filename))
        return render_template('upload_file.html', link=f"http://{domain}/infoFile?id={obj.id}", form=form)
    return render_template('upload_file.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/infoFile')
def infoFile():
    file_id = int(request.args.get('id'))
    if not file_id:
        return redirect('/')
    file = get_file_class(file_id)
    if not file:
        return abort(404)
    if file.is_private and not current_user.is_authenticated:
        return abort(401)
    dt = file.upload_date.date()
    day = str(dt.day).rjust(2, '0')
    month = str(dt.month).rjust(2, '0')
    year = str(dt.year).rjust(4, '0')
    dt = f"{day}.{month}.{year}"
    username = file.user.login
    return render_template('getFile.html', filename=file.filename, comment=file.comment, downloaded=file.downloaded,
                           date=dt, username=username, download_link=f"/download?id={file_id}")


@app.route('/download')
def download():
    file_id = int(request.args.get('id'))
    if not file_id:
        return redirect('/')
    file = get_file_class(file_id)
    if not file:
        return abort(404)
    if file.is_private and not current_user.is_authenticated:
        return abort(401)
    path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], str(file_id))
    file.downloaded += 1
    session = db_session.create_session()
    session.merge(file)
    session.commit()
    return send_file(os.path.join(path, file.filename), as_attachment=True)


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(port=80, host='127.0.0.1')
