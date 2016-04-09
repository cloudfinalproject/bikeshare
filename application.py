#!/usr/bin/env python2.7

import os
from sqlalchemy import *
from flask import Flask, request, render_template, g, redirect, Response, session, jsonify
from server.config import *
from server.data_access.user_data_access import *


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# set the secret key.  keep this really secret:
app.secret_key = secret_key
DATABASEURI = database_uri
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.

    The variable g is globally accessible.
    """
    # if ('uid' not in session) and (request.endpoint != "login") and (request.endpoint != "userLogin"):
    #     return redirect('/login')
    try:
        g.conn = engine.connect()
    except:
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()
        g.conn = None

@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


@app.route('/login')
def login():  # test view
    return render_template("login.html")

@app.route('/view/register')
def reg():
    return render_template('register.html')

@app.route('/userLogin', methods=['POST'])
def userLogin():
    username = request.form['username']
    password = request.form['password']
    uda = UserDataAccess(g.conn)
    output = uda.authorize(username, password)

    if output['status']:
        user = output['result']['user']
        session['uid'] = user['uid']
        session['username'] = user['username']
        session['firstname'] = user['firstname']
        session['lastname'] = user['lastname']
        session['email'] = user['email']

    return jsonify(output)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    uda = UserDataAccess(g.conn)
    output = uda.register(username, password, firstname, lastname, email)

    return jsonify(output)

@app.route('/view/sendMsg')
def reg():
    return render_template('sendMsg.html')

@app.route('/view/showMsg')
def reg():
    return render_template('showMsg.html')


@app.route('/sendMsg', methods=['POST'])
def sendMsg():
    uid1 = session['uid']
    uid2 = request.form['toWhom']
    message = request.form['message']
    
    uma = UserMsgAccess(g.conn)
    output = uma.sendMsg(uid1, uid2, message)

    return jsonify(output)



@app.route('/showMsg', methods=['REQUEST'])
def showMsg():
    uid = session['uid']
    
    
    uma = UserMsgAccess(g.conn)
    output = uma.showMsg(uid)

    return jsonify(output)


if __name__ == "__main__":

    # @click.command()
    # @click.option('--debug', is_flag=True)
    # @click.option('--threaded', is_flag=True)
    # @click.argument('HOST', default='0.0.0.0')
    # @click.argument('PORT', default=5000, type=int)
    # def run(debug, threaded, host, port):
    #     """
    #         This function handles command line parameters.
    #         Run the server using:
    #         python server.py
    #
    #         Show the help text using:
    #
    #         python server.py --help
    #
    #     """
    #
    #     HOST, PORT = host, port
    #     print "running on %s:%d" % (HOST, PORT)
    #     app.run(host=HOST, port=PORT, debug=True, threaded=threaded)
    #
    # run()
    app.debug = True
    app.run()