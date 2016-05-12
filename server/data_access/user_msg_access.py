from user_data_access import *


class UserMsgAccess:
    def __init__(self, conn):
        self.conn = conn

    def show_messages(self, rid):
        output = {'result': {}, 'status': False, 'message': ''}
        messages = []
        status = False
        message = ''
        try:
            cursor = self.conn.execute("SELECT m.*, r.uid FROM messages m, requests r WHERE m.rid = r.rid and m.rid = %s order by creationdate desc", (rid, ))
            for row in cursor:
                msg = dict(row)

                uda = UserDataAccess(self.conn)
                owner_id = msg['uid1']
                owner = uda.get_user(owner_id)
                msg['owner'] = owner['result']['user']
                requester_id = msg['uid']
                requester = uda.get_user(requester_id)
                msg['requester'] = requester['result']['user']

                # remove unnecessary fields
                msg.pop('uid', None)
                msg.pop('uid1', None)
                # msg.pop('uid2', None)

                messages.append(msg)
            cursor.close()

            status = True
            message = "All the messages for this request has been retrieved successfully."
             
        except Exception, e:
            status = False
            message = e
            raise e

        finally:
            output['status'] = status
            output['message'] = message
            output['result'] = messages
            return output

    def send_message(self, uid1, rid, contents):
        output = {'result': {}, 'status': False, 'message': ''}
        status = False
        message = ''
        try:
            cursor = self.conn.execute("""insert into messages(uid1, message, creationdate, rid)
            values (%s, %s, now(), %s) returning mid, creationdate""", (uid1, contents, rid))
            for row in cursor:
                new_msg_id = row['mid']
                creationdate = row['creationdate']
                output['result']['mid'] = new_msg_id
                output['result']['creationdate'] = creationdate
            cursor.close()

            message = "Message sent successfully!"
            status = True
        except Exception, e:
            status = False
            message = e
            raise e

        finally:
            output['status'] = status
            output['message'] = message
            return output




    
   

