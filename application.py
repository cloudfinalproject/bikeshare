#!/usr/bin/env python2.7

import os
from sqlalchemy import *
from flask import Flask, request, render_template, g, redirect, Response, session, jsonify, abort
from server.config import *
from server.data_access.user_data_access import *
from server.data_access.bike_data_access import *
from server.data_access.user_msg_access import *


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
application = api = Flask(__name__, template_folder=tmpl_dir)

# set the secret key.  keep this really secret:
application.secret_key = secret_key
DATABASEURI = database_uri
engine = create_engine(DATABASEURI)

@application.before_request
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

@application.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


@application.route('/login')
def login():  # test view
    return render_template("login.html")

@application.route('/view/register')
def reg():
    return render_template('register.html')

@application.route('/userLogin', methods=['POST'])
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

@application.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    uda = UserDataAccess(g.conn)
    output = uda.register(username, password, firstname, lastname, email)

    return jsonify(output)

@application.route('/getAllBikes')
def get_all_bikes():
    if not session or 'uid' not in session:
        return abort(403)
    else:
        bda = BikeDataAccess(g.conn)
        output = bda.get_bikes_by_user_id(session['uid'])

        return jsonify(output)

@application.route('/view/sendMsg')
def view_send_msg():
    return render_template('sendMsg.html')

@application.route('/view/showMsg')
def view_show_msg():
    return render_template('showMsg.html')


@application.route('/sendMsg', methods=['POST'])
def sendMsg():
    uid1 = session['uid']
    uid2 = request.form['toWhom']
    message = request.form['message']

    uma = UserMsgAccess(g.conn)
    output = uma.sendMsg(uid1, uid2, message)

    return jsonify(output)



@application.route('/showMsg', methods=['REQUEST'])
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
    application.debug = True
    application.run()