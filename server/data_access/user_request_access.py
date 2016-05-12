from user_data_access import *
from bike_data_access import *


class UserRequestAccess:
    def __init__(self, conn):
        self.conn = conn

    def get_requests(self, uid, request_status=False):
        output = {'result': {}, 'status': False, 'message': ''}
        requests = []
        status = False
        message = ''
        try:
            query = 'SELECT r.* FROM requests r, bikes b WHERE r.bid = b.bid AND b.uid = ' + str(uid)
            if request_status:
                query += ' AND r.status = ' + str(request_status)
            cursor = self.conn.execute(query)

            for row in cursor:
                r = dict(row)

                bid = r['bid']
                bda = BikeDataAccess(self.conn)
                bike = bda.get_bike(bid)
                r['bike'] = bike['result']

                uid = r['uid']
                uda = UserDataAccess(self.conn)
                user = uda.get_user(uid)
                r['user'] = user['result']['user']

                requests.append(r)

            cursor.close()

            status = True
            message = "You have got all the requests successfully."
             
        except Exception, e:
            status = False
            message = e
            raise e

        finally:
            output['status'] = status
            output['message'] = message
            output['result'] = requests
            return output

    def get_request_by_id(self, rid):
        output = {'result': {}, 'status': False, 'message': ''}
        request = {}
        status = False
        message = ''
        try:
            cursor = self.conn.execute("SELECT r.* FROM requests r WHERE r.rid = %s", (rid, ))

            for row in cursor:
                request = dict(row)

                bid = request['bid']
                bda = BikeDataAccess(self.conn)
                bike = bda.get_bike(bid)
                request['bike'] = bike['result']

                uid = request['uid']
                uda = UserDataAccess(self.conn)
                user = uda.get_user(uid)
                request['user'] = user['result']['user']

            cursor.close()

            status = True
            message = "You have got the request successfully."

        except Exception, e:
            status = False
            message = e
            raise e

        finally:
            output['status'] = status
            output['message'] = message
            output['result'] = request
            return output


    def send_request(self, uid, bid, from_date, to_date, respond='pending'):
        output = {'result': {}, 'status': False, 'message': ''}
        status = False
        message = ''

        bda = BikeDataAccess(self.conn)
        bike = bda.get_bike(bid)
        price = bike['result']['price']

        try:
            cursor = self.conn.execute("""insert into requests(uid, bid, status, from_date, to_date, unitprice)
            values (%s, %s, %s, %s, %s, %s) returning rid""", (uid, bid, respond, from_date, to_date, price))

            for row in cursor:
                new_request_id = row['rid']
                # creationdate = row['creationdate']
                output['result']['rid'] = new_request_id
            # output['result']['creationdate'] = creationdate
            cursor.close()

            status = True
            message = "Request sent successfully!"
        except Exception, e:
            print e
            status = False
            message = e
            raise e

        finally:  
            output['message'] = message
            output['status'] = status
            return output

    def respond_request(self, rid, respond):  # respond can be: 'pending', 'approved', 'rejected' and 'finished'
        output = {'result': {}, 'status': False, 'message': ''}
        status = False
        message = ''
        try:
            cursor = self.conn.execute('update requests set status=%s where rid=%s', (respond, rid))
            cursor.close()

            if respond == 'approved':  # should automatically reject all the collided requests
                request = self.get_request_by_id(rid)
                request = request['result']
                bid = request['bid']
                from_date = request['from_date']
                to_date = request['to_date']
                self.__reject_collided_requests(bid, from_date, to_date)

            message = "Request " + respond + " successfully!"
            status = True
        except Exception, e:
            print e
            status = False
            message = e
            raise e

        finally:  
            output['message'] = message
            output['status'] = status
            output['result']['respond'] = respond
            return output

    def __reject_collided_requests(self, bid, from_date, to_date):
        cursor = self.conn.execute("""select rid from requests
        where from_date < %s
        and %s < to_date
        and status = 'pending'
        and bid = %s""", (to_date, from_date, bid))
        for row in cursor:
            rid = row['rid']
            self.respond_request(rid, 'rejected')