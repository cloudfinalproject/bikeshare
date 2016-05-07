class UserRequestAccess:
    def __init__(self, conn):
        self.conn = conn

    def showRequest(self, uid):
        output = {'result': {}, 'status': False, 'message': ''}
        msg = {}
        status = False
        message = ''
        try:
            cursor = self.conn.execute("SELECT * FROM requests WHERE ownerid = %s", (uid, ))
            for row in cursor:
                msg[row['rid']] = {}
                msg[row['rid']]['from'] = row['uid']
                msg[row['rid']]['bike'] = row['bid']
                msg[row['rid']]['status'] = row['status']
                msg[row['rid']]['fromDate'] = row['from_date']
                msg[row['rid']]['toDate'] = row['to_date']

             
        except Exception, e:
            status = False
            message = e
            raise e

        finally:
            cursor.close()
            output['status'] = status
            output['message'] = message
            output['result']['requests'] = msg
            return output
            

    def sendRequest(self, uid, ownerid, bid, respond, fromDate, toDate):
        output = {'result': {}, 'status': False, 'message': ''}
        user = {}
        status = False
        message = ''
        try:

            cursor = self.conn.execute("""insert into requests(uid, ownerid, bid, status, from_date, to_date)
            values (%s, %s, %s, %s, %s, %s) returning rid""", (uid, ownerid, bid, respond, fromDate, toDate))
            print 'try'
            for row in cursor:
                new_request_id = row['rid']
                # creationdate = row['creationdate']
            output['result']['rid'] = new_request_id
            # output['result']['creationdate'] = creationdate
            message = "Request sent successfully!"
            cursor.close()
        except Exception, e:
            print e
            status = False
            message = e
            raise e

        finally:  
            output['message'] = message
            return output


    def respondRequest(self, rid, status):
        output = {'result': {}, 'status': False, 'message': ''}
        user = {}
        # status = False
        message = ''
        try:
            cursor = self.conn.execute('update requests set status=%s where rid=%s', (status, rid))
            message = "Request " + status + " successfully!"
            # status = True
            cursor.close()
        except Exception, e:
            print e
            # status = False
            message = e
            raise e

        finally:  
            output['message'] = message
            output['status'] = True
            return output


    
   

