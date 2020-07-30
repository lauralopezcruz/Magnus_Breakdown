from flask import render_template
from app import app
from app.forms import InputForm

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        return render_template('index.html', form=form, input=form.group.data)
    return render_template('index.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')
