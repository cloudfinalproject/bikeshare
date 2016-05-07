import sys


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

    def get_available_bikes(self, lon, lat, distance, from_date, to_date, from_price=0, to_price=sys.maxint):
        output = {'result': {}, 'status': False, 'message': ''}
        bikes = []
        cursor = self.conn.execute("""
        select *, point(%s, %s) <@> point(lon, lat)::point AS distance
        from bikes b
        where (point(%s, %s) <@> point(lon, lat)) < %s
        and b.status = true
        and b.price between %s and %s
        order by distance
        """, (lon, lat, lon, lat, distance, from_price, to_price))
        for row in cursor:
            bike = dict(row)
            if self.__is_bike_available(bike['bid'], from_date, to_date):
                bikes.append(bike)
        cursor.close()

        output['status'] = True
        output['result'] = bikes

        return output

    def __is_bike_available(self, bid, from_date, to_date):
        is_available = False

        cursor = self.conn.execute("""select count(*) as size from requests
        where from_date < %s
        and %s < to_date
        and bid = %s""", (to_date, from_date, bid))
        for row in cursor:
            size = int(row['size'])
            if size == 0:
                is_available = True

        return is_available