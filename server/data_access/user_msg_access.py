class UserMsgAccess:
    def __init__(self, conn):
        self.conn = conn

    def showMsg(self, uid):
        output = {'result': {}, 'status': False, 'message': ''}
        msg = {}
        status = False
        message = ''
        try:
            cursor = self.conn.execute("SELECT * FROM messages WHERE uid2 = %s", (uid, ))
            for row in cursor:
                cursor2 = self.conn.execute("SELECT username FROM users WHERE uid = %s", (row['uid1'], ))
                for row2 in cursor2:
                    msg[row['mid']] = {}
                    msg[row['mid']]['from'] = row2['username']
                    msg[row['mid']]['content'] = row['message']
                    msg[row['mid']]['timestamp'] = row['creationdate']
             
        except Exception, e:
            status = False
            message = e
            raise e

        finally:
            cursor.close()
            output['status'] = status
            output['message'] = message
            output['result']['messages'] = msg
            return output
            

    def sendMsg(self, uid1, uid2, msgToSend):
        output = {'result': {}, 'status': False, 'message': ''}
        user = {}
        status = False
        message = ''
        try:
            cursor = self.conn.execute("""insert into messages(uid1, uid2, message, creationdate)
            values (%s, %s, %s, now()) returning mid, creationdate""", (uid1, uid2, msgToSend))
            for row in cursor:
                new_msg_id = row['mid']
                creationdate = row['creationdate']
            output['result']['mid'] = new_msg_id
            output['result']['creationdate'] = creationdate
            message = "Message sent successfully!"
        except Exception, e:
            status = False
            message = e
            raise e

        finally:  
            cursor.close()
            return output




    
   

