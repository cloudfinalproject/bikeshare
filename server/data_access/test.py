from bike_data_access import *
from server.config import *
from sqlalchemy import *


DATABASEURI = database_uri
engine = create_engine(DATABASEURI)
conn = None
try:
    conn = engine.connect()
except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    conn = None

bda = BikeDataAccess(conn)
print bda.get_bikes_by_user_id(1)