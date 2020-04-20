from flask import Flask, render_template, redirect
from forms import LoginForm, RegForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '77ac4973981o3xu7s1aj55o7cg76592z612wt4jg486u91u615j5587zh696x6q4'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/cabinet')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        return redirect('/cabinet')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
