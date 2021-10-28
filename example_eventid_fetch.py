#import the function fetch_fields_from_db
from targeted_population_api.targeted_population import fetch_fields_from_db

#database dwtails
database_name='mongodb'
database='exhibitor_details'
collection='exhibitor_details'
#specify the fields to be fetched
fields=['_id','BDEvent_ID','brand_name', 'Timestamp']

#call the fetch_fields_from_db function
data=fetch_fields_from_db(database_name, fields,collection, database)
print(data)



