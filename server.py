# this is a flask server that uses sessions and json files to store data and load.
# it can be customized but
# if there was bugs, feel free to fork and fix them.
# this project cannot used for personal uses.
from hashlib import md5
import json
import flask

app = flask.Flask(__name__)
app.secret_key = 'b<9rdX$us[qf@6!pc~-4~W/_(OEa0@21?2tmD2txz07<+=^Qnl|8.88T[KoK(P+'
app.config['SESSION_TYPE'] = 'filesystem'
with open('posts.json') as f:
    posts = json.load(f)
with open('users.json') as f:
    users = json.load(f)

@app.route('/')
def index():
    return flask.render_template('index.html', posts=posts, users=users) + '<br/><a href="/">Home</a>'
@app.route('/contact')
def contact():
    return 'Contact us!<br/><a href="/">Home</a>'
@app.route('/send_yours')
def send_yours():
    # check if the user is logged in
    if flask.session.get('logged_in'):
        return flask.render_template('send.html', author=flask.session['username']) + '<br/><a href="/">Home</a>'
    else:
        return '<p>You need to <a href="/login">login</a> first.</p>' + '<br/><a href="/">Home</a>'
@app.route('/send', methods=['POST'])
def send_yours_post():
    ids = 0
    title = flask.request.form['title']
    content = flask.request.form['content']
    for post in posts:
        ids+=1
    posts.append({'id': ids,'title': title, 'content': content, 'author': flask.session['username']})
    with open('posts.json', 'w') as f:
        json.dump(posts, f)
    return '<p>Your post has been sent!</p>'
@app.route('/api/posts')
def api_posts():
    return flask.jsonify(posts)
@app.route('/api/users')
def api_users():
    usernames = []
    for i in users:
        usernames.append({"userame": i["username"]})
    return flask.jsonify(usernames)

@app.route('/api/send/<string:title>/<string:content>/<string:author>')
def api_send(title, content, author):
    for post in posts:
        id+=1
    posts.append(
        {'id': id, 'title': title, 'content': content, 'author': author, 'year': 2022}
    )
    with open('posts.json', 'w') as f:
        json.dump(posts, f)
    return '<p>Your post has been sent!</p>' + '<br/><a href="/">Home</a>'
@app.route('/post/<int:id>')
def post(id):
    return flask.render_template('post.html', post=posts[id]) + '<br/><a href="/">Home</a>'
@app.route('/posts/<string:author>')
def posts_by_author(author):
    return flask.render_template('posts.html', posts=posts, author=author)  + '<br/><a href="/">Home</a>'
@app.route('/login')
def login():
    return flask.render_template('login.html') + '<br/><a href="/">Home</a>'
@app.route('/login', methods=['POST'])
def login_post():
    for user in users:
        if user['username'] == flask.request.form['username']:
            passs = md5(flask.request.form['password'].encode('utf-8')).hexdigest()
            if user['password'] == passs:
                flask.session['logged_in'] = True
                flask.session['username'] = flask.request.form['username']
                return flask.redirect(flask.url_for('index')) 
    return '<p>Login failed!</p>' + '<br/><a href="/">Home</a>'
@app.route('/dashboard')
def dashboard():
    if flask.session.get('logged_in'):
        return flask.render_template('dash.html', username=flask.session['username']) + '<br/><a href="/">Home</a>'
    else:
        return '<p>You need to <a href="/login">login</a> first.</p>' + '<br/><a href="/">Home</a>'
@app.route('/logout')
def logout():
    if flask.session.get('logged_in'):
        del flask.session['logged_in']
        del flask.session['username']
        return flask.redirect(flask.url_for('index')) 
    else:
        return '<p>You are not logged in!</p>' + '<br/><a href="/">Home</a>'
@app.route('/register')
def register():
    if flask.session.get('logged_in'):
        return flask.redirect(flask.url_for('index'))
    else:
        return flask.render_template('register.html') + '<br/><a href="/">Home</a>'
@app.route('/register', methods=['POST'])
def register_post():
    # check if the username has space or illegal characters
    illegal = [
        ' ',
        '$',
        '%',
        '^',
        '&',
        '*',
        '+',
        '=',
        '|',
        '\\',
        '/',
        '?',
        '<',
        '>',
        '"',
        '\'',
        '`',
        '~',
        '!',
        '@',
        '#',
    ]
    for i in illegal:
        if i in flask.request.form['username']:
            return '<p>Username cannot contain spaces or illegal characters!</p>' + '<br/><a href="/">Home</a>'
    if flask.request.form['username'] == '':
        return '<p>Username cannot be empty!</p>' + '<br/><a href="/">Home</a>'
    if flask.request.form['password'] == '':
        return '<p>Password cannot be empty!</p>' + '<br/><a href="/">Home</a>'
    if "<" in flask.request.form['password'] or ">" in flask.request.form['password']:
        return '<p>Password cannot contain < or >!</p>' + '<br/><a href="/">Home</a>'
    for user in users:
        if user['username'] == flask.request.form['username']:
            return '<p>Username already exists!</p>' + '<br/><a href="/">Home</a>'
    passs = md5(flask.request.form['password'].encode('utf-8')).hexdigest()
    users.append(
        {'username': flask.request.form['username'], 'password': passs}
    )
    with open('users.json', 'w') as f:
        json.dump(users, f)
    return '<p>You have been registered!</p>' + '<br/><a href="/">Home</a>'
app.run(debug=False)