from flask import Flask, render_template, request, redirect, url_for, flash, abort
import json
import os.path
from werkzeug.utils import secure_filename

# you have to have a file that creates the Flask application instance
app = Flask(__name__)
app.secret_key = 'someRandomStrongKey'  # used to encrypt the session cookie


@app.route('/')
def home():
    return render_template('home.html')


# provide a list of methods that are allowed, GET is default
@app.route('/your-url', methods=['GET', 'POST'])
def your_url():  # we can't use - in function names
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls = json.load(url_file)

        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)

            f.save(
                '/Users/solidstojan/Documents/Workspaces.nosync/FlaskEssentialTrainingLinkedinCourse/url-shortener/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)

        """
        render_template looks for files in templates folder
        Jinja2 is the template engine that Flask uses
        it enables us to pass variables to the html file
        args is a dictionary for different parameters
        we have to use .form instead of .args because we are using POST
        """
        return render_template('your_url.html', code=request.form['code'])
    else:
        # url_for is a function that takes the name of the function as an argument and returns the url for that function; if url is changed, we don't have to change it everywhere
        return redirect(url_for('home'))


# <string:code> is a dynamic parameter, any string that is passed in will be stored in code variable
@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urls = json.load(url_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)  # 404 is a status code for not found


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404