import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging
import sys

conn_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
# Note: this function also updates the conn_count variable
def get_db_connection():
    global conn_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    conn_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      return render_template('404.html'), 404
    else:
      logging.info(f'Article \"${post["title"] }\" retrieved!')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logging.info('About Us Page is retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# Healthcheck endpoint
@app.route('/healthz')
def healthz():
    response = app.response_class(
            response = json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

# Metrics endpoint
@app.route('/metrics')
def metrics():
    global conn_count
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    response = app.response_class(
            response = json.dumps({
                "status":"success",
                "data":{
                    "db_connection_count": conn_count, "post_count": len(posts)
                    }
                }),
            status=200,
            mimetype='application/json'
    )
    return response

# start the application on port 3111
if __name__ == "__main__":
    formatter = logging.Formatter(
        '%(levelname)s:%(name)s:%(asctime)s %(message)s'
    )
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    app.logger.addHandler(stdout_handler)
    stderr_handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt='%d/%M/%Y, %H:%M:%S',
        handlers=[
            stdout_handler, stderr_handler,
        ])
    app.run(host='0.0.0.0', port='3111')
