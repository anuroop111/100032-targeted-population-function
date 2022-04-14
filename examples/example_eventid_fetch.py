#import the function fetch_fields_from_db
from targeted_population_api.targeted_population import fetch_fields_from_db

#database details
database_name='mongodb'
database='exhibitor_details'
collection='exhibitor_details'
#specify the fields to be fetched
fields=['_id','BDEvent_ID','brand_name', 'Timestamp']

#call the fetch_fields_from_db function with start point and end point
start_point=0
end_point = 999999999999

data=fetch_fields_from_db(database_name, fields,collection, database, start_point, end_point)
print(data)



