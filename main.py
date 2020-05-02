from config import *


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
        file = request.files["file"]
        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            if len(file_bytes) >= MAX_FILE_SIZE:
                return render_template('upload_file.html',
                                       message=f'Размер файла превышает максимальный ({MAX_FILE_SIZE} байт)', form=form)
            else:
                session = db_session.create_session()
                obj = Files(filename=file.filename, user_id=current_user.id, is_private=form.is_private.data,
                            comment=form.comment.data)
                session.add(obj)
                session.commit()
                f = open(f'files/{obj.id}/{file.filename}', 'wb')
                f.write(file_bytes)
                f.close()
                del file_bytes
                return render_template('upload_file.html', link=f"https://{domain}/getFile?id={obj.id}", form=form)
    return render_template('upload_file.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(port=80, host='127.0.0.1')
