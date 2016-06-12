import datetime
from shadowfax import db

class Orders(db.Document):
	order_id = db.IntField(required = True)
     	seller_id = db.IntField(required = True)
	rider_id = db.IntField(required = True)
	cluster_id = db.IntField(required = True)
	scheduled_time = db.DateTimeField(required= True)
	allot_time = db.DateTimeField()
	pickup_time = db.DateTimeField()
   	delivered_time = db.DateTimeField()
	pickup_latitude = db.StringField(required=True)
	pickup_longitude = db.StringField(required=True)
	delivered_latitude = db.StringField(required=True)
	delivered_longitude = db.StringField(required=True)
	house_number = db.StringField()
	sublocality = db.StringField()


class Locations(db.Document):
 	uid = db.IntField(required= True)
	rider_id = db.IntField(required = True)
	update_timestamp = db.DateTimeField(required=True)
	latitude = db.StringField(required = True)
	longitude = db.StringField(required = True)
	source = db.IntField()
	create_timestamp = db.StringField()	


class AddressMapping(db.Document):
	house_number=db.StringField(required=True)
	latitude=db.StringField(required=True)
	longitude=db.StringField(required=True)
	google_sugg_landmark=db.ListField()
	google_useful_landmark=db.ListField()
	user_landmark=db.ListField()
