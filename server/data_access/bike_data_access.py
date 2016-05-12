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

    def add_bike(self, user_id, model, price, address, state, city, postcode, country, lat, lon, details, file_url=False):
        output = {'result': {}, 'status': False, 'message': ''}
        bike = {}
        cursor = self.conn.execute("""insert into bikes(uid, model, price, address, state, city, postcode, country, lat, lon, details)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning bid""", (user_id, model, price, address, state, city, postcode, country, lat, lon, details))
        for row in cursor:
            new_bike_id = row['bid']
            bike['bid'] = new_bike_id
            bike['uid'] = user_id
            bike['model'] = model
            bike['price'] = price
            bike['address'] = address
            bike['state'] = state
            bike['city'] = city
            bike['postcode'] = postcode
            bike['country'] = country
            bike['lat'] = lat
            bike['lon'] = lon
            bike['details'] = details

            if file_url:
                cursor_1 = self.conn.execute("""insert into bike_photos(bid, url)
                values (%s, %s)""", (new_bike_id, file_url))
                cursor_1.close()
                bike['file_url'] = file_url

        cursor.close()
        output['status'] = True
        output['message'] = 'A new bike is added!'
        output['result'] = bike

        return output

    def edit_bike_address(self, bid, address, state, city, postcode, country, lat, lon):
        output = {'message': '', 'status': False}
        output['status'] = True
        output['message'] = 'The address of the bike has been updated!'
        self.conn.execute("""update bikes
        set address=%s, state=%s, city=%s, postcode=%s, country=%s, lat=%s, lon=%s
        where bid=%s""", (address, state, city, postcode, country, lat, lon, bid))

        return output

    def edit_bike_info(self, bid, model, price, details):
        output = {'message': '', 'status': False}
        output['status'] = True
        output['message'] = 'The information of the bike has been updated!'
        self.conn.execute("""update bikes
        set model=%s, price=%s, details=%s
        where bid=%s""", (model, price, details, bid))

        return output

    def get_bike(self, bid):
        output = {'result': {}, 'status': False, 'message': ''}
        bike = {}
        cursor = self.conn.execute("SELECT * FROM bikes WHERE bid=%s", (bid,))
        for row in cursor:
            bike = dict(row)
        cursor.close()

        output['status'] = True
        output['result'] = bike

        return output


    def get_available_bikes(self, lon, lat, distance, from_date, to_date, from_price=0, to_price=sys.maxint):
        output = {'result': {}, 'status': False, 'message': ''}
        bikes = []
        cursor = self.conn.execute("""
        select *, point(%s, %s) <@> point(lon, lat)::point AS distance
        from bikes b, users u
        where (point(%s, %s) <@> point(lon, lat)) < %s
        and b.status = true
        and b.uid = u.uid
        and b.price between %s and %s
        order by distance
        """, (lon, lat, lon, lat, distance, from_price, to_price))
        for row in cursor:
            if self.__is_bike_available(row['bid'], from_date, to_date):
                bike_info = dict(row)
                bike = {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [row['lat'], row['lon']]
                    }
                }
                bike['properties'] = bike_info
                bike['properties']['name'] = row['model']
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
        and status = 'approved'
        and bid = %s""", (to_date, from_date, bid))
        for row in cursor:
            size = int(row['size'])
            if size == 0:
                is_available = True

        return is_available