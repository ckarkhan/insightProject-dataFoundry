from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Chetan'}
    return '''
<html>
    <head>
        <title>"</title>
    </head>
    <body>
        <h1></h1>Hello, ''' + user['username'] + ''' Welcome to X-ray Annotations. You are contributing to better clinical diagnosis!</h>
    </body>
</html>'''