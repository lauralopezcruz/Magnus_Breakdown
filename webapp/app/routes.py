from flask import render_template
from app import app
from app.forms import GroupInputForm
import magnus


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    form = GroupInputForm()
    if form.validate_on_submit():
        gens_str = form.generators.data
        rel_str = form.relation.data
        group = magnus.str_to_group(gens_str, rel_str, name="G_0")
        group_strings = [gp.latex() for gp in magnus.magnus_breakdown(group)]
        return render_template('index.html', form=form,
                               group_strings=group_strings)
    return render_template('index.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')
