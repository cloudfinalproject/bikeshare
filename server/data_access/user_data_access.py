class UserDataAccess:
    def __init__(self, conn):
        self.conn = conn

    def authorize(self, username, password):
        output = {'result': {}, 'status': False, 'message': ''}
        user = {}
        status = False
        message = ''
        cursor = self.conn.execute("SELECT count(*) as size FROM users WHERE username = %s and password = %s", (username, password))
        for row in cursor:
            if int(row['size']) > 0:
                status = True
                message = 'Login successful!'
                cursor_2 = self.conn.execute("SELECT * FROM users WHERE username = %s and password = %s", (username, password))
                for row_2 in cursor_2:
                    user['uid'] = row_2['uid']
                    user['username'] = row_2['username']
                    user['firstname'] = row_2['firstname']
                    user['lastname'] = row_2['lastname']
                    user['email'] = row_2['email']
                cursor_2.close()
            else:
                message = 'The username and password does not match!'
        cursor.close()
        output['status'] = status
        output['message'] = message
        output['result']['user'] = user

        return output

    def register(self, username, password, firstname, lastname, email):
        output = {'result': {}, 'status': False, 'message': ''}
        status = False
        message = ''
        user = {}

        is_unique, message = self.__is_unique(username, email)
        if not is_unique:
            output['message'] = message
            return output
        else:
            status = True
            cursor = self.conn.execute("""insert into users(username, password, firstname, lastname, email, creationdate)
            values (%s, %s, %s, %s, %s, now()) returning uid, creationdate""", (username, password, firstname, lastname, email))
            for row in cursor:
                new_user_id = row['uid']
                creationdate = row['creationdate']
                user['uid'] = new_user_id
                user['username'] = username
                user['firstname'] = firstname
                user['lastname'] = lastname
                user['email'] = email
                user['creationdate'] = creationdate
            cursor.close()
            output['result'] = user
            output['message'] = 'The registration is successful!'
            output['status'] = status

            return output

    def __is_unique(self, username, email):
        message = 'You can use this username and email!'
        status = True
        cursor = self.conn.execute('select count(*) as size from users where username=%s', (username, ))
        for row in cursor:
            if int(row['size']) > 0:
                status = False
                message = 'The username has been taken!'
        cursor.close()

        if status:
            cursor = self.conn.execute('select count(*) as size from users where email=%s', (email, ))
            for row in cursor:
                if int(row['size']) > 0:
                    status = False
                    message = 'The email has been taken!'
            cursor.close()

        return status, message

