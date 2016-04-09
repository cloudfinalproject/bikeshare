class BikeDataAccess:
    def __init__(self, conn):
        self.conn = conn

    def get_bikes_by_user_id(self, user_id):
        output = {'result': {}, 'status': False, 'message': ''}
        bikes = []
        cursor = self.conn.execute("SELECT * FROM bikes WHERE uid=%s", (user_id,))
        for row in cursor:
            bike = dict(row)
            bike['price'] = float(row['price'])
            bikes.append(bike)
        cursor.close()

        output['status'] = True
        output['result'] = bikes

        return output

    def add_bike(self, user_id, model, price, location, details):
        output = {'result': {}, 'status': False, 'message': ''}
        bike = {}
        cursor = self.conn.execute("""insert into bikes(uid, model, price, location, details)
        values (%s, %s, %s, %s, %s) returning bid""", (user_id, model, price, location, details))
        for row in cursor:
            new_bike_id = row['bid']
            bike['bid'] = new_bike_id
            bike['uid'] = user_id
            bike['model'] = model
            bike['price'] = price
            bike['location'] = location
            bike['details'] = details
        cursor.close()
        output['status'] = True
        output['message'] = 'A new bike is added!'
        output['result'] = bike

        return output