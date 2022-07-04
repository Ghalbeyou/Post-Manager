# this is a flask server that uses sessions and json files to store data and load.
# it can be customized but
# if there was bugs, feel free to fork and fix them.
# this project cannot used for personal uses.
from hashlib import md5
import json
import flask
with open('config.json') as f:
    config = json.load(f)
app = flask.Flask(__name__)
app.secret_key = 'b<9rdX$us[qf@6!pc~-4~W/_(OEa0@21?2tmD2txz07<+=^Qnl|8.88T[KoK(P+'
app.config['SESSION_TYPE'] = 'filesystem'
with open('posts.json') as f:
    posts = json.load(f)
with open('users.json') as f:
    users = json.load(f)

@app.route('/')
def index():
    return flask.render_template('index.html', posts=posts, users=users, post_len=len(posts), user_len=len(users)) + '<br/><a href="/">Home</a>'
@app.route('/send_yours')
def send_yours():
    # check if the user is logged in
    if flask.session.get('logged_in'):
        return flask.render_template('send.html', author=flask.session['username']) + '<br/><a href="/">Home</a>'
    else:
        return flask.render_template('access_de.html')
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
    return '<p>Your post has been sent!</p>'  + "<br/><a href='/'>Home</a>"
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
    _ = id-1
    # do a simple try
    try:
        return flask.render_template('post.html', post=posts[_]) + '<br/><a href="/">Home</a>'
    except:
        return "<p>Post not found</p>" + '<br/><a href="/">Home</a>'

@app.route('/posts/<string:author>')
def posts_by_author(author):
    return flask.render_template('posts.html', posts=posts, author=author)  + '<br/><a href="/">Home</a>'
@app.route('/login')
def login():
    if len(users) < 1:
        return "<p>No Users found!</p>"
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
        return flask.render_template('access_de.html')
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
@app.route('/delete')
def delete():
    if flask.session.get('logged_in'):
        if flask.session.get('username') == 'admin':
            return 'Delete any post you want!'
        return flask.render_template('delete.html', user=flask.session.get('username'), posts=posts)
@app.route('/delete/<int:id>')
def delete_post(id):
    if flask.session.get('username') == 'admin':
        posts.pop(id)
        return 'Done!'
    for post in posts:
        if post["id"] == id:
            if post["author"] == flask.session.get('username'):
                # remove the giving id from array

                posts.pop(id)
                with open('posts.json', 'w') as f:
                    json.dump(posts, f)
                return "<p> deleted!</p>" + "<br/><a href='/'>Home</a>"
            else:
                return "<p>You are not the owner of that post!</p>" + '<br/><a href="/">Home</a>'
        else:
            return "<p>Post don't exist.</p>" + '<br/><a href="/">Home</a>'
@app.route('/report/<int:id>')
def report(id):
    if flask.session.get('logged_in'):
        return flask.render_template('report_.html', id=id) + '<br/><a href="/">Home</a>'
    else:
        return flask.render_template('access_de.html')
@app.route('/report')
def report_post():
    if flask.session.get('logged_in'):
        return flask.render_template('report.html', posts=posts) + '<br/><a href="/">Home</a>'
    else:
        return flask.render_template('access_de.html')
@app.route('/report', methods=['POST'])
def report_post_post():
    if flask.session.get('logged_in'):
        for post in posts:
            if post["id"] == int(flask.request.form['post_id']):
                return "<p> reported!</p>" + "<br/><a href='/'>Home</a>"
        return "<p>Post don't exist.</p>" + '<br/><a href="/">Home</a>'
    else:
        return flask.render_template('access_de.html')
@app.route('/reportuser/<string:id>')
def reportuser(id):
    if flask.session.get('logged_in'):
        return flask.render_template('reportuser_.html', user=id) + '<br/><a href="/">Home</a>'
    else:
        return flask.render_template('access_de.html')
@app.route('/reportuser')
def reportuser_post():
    if flask.session.get('logged_in'):
        return flask.render_template('reportuser.html') + '<br/><a href="/">Home</a>'
    else:
        return flask.render_template('access_de.html')
@app.route('/reportuser', methods=['POST'])

def reportuser_post_post():
    if flask.session.get('logged_in'):
        for user in users:
            if user['username'] == flask.request.form['username']:
                return "<p> reported!</p>" + "<br/><a href='/'>Home</a>"
        return "<p>User don't exist.</p>" + '<br/><a href="/">Home</a>'
    else:
        return flask.render_template('access_de.html')
@app.errorhandler(404)
def notfound(a):
    return flask.render_template('404.html')
@app.errorhandler(500)
def internalerror(a):
    return flask.render_template('500.html')
@app.errorhandler(403)
def forbidden(a):
    return flask.render_template('403.html')
@app.errorhandler(405)
def methodnotallowed(a):
    return flask.render_template('405.html')
app.run(debug=config["debug"], port=config["port"])