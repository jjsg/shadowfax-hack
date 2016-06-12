from shadowfax import app
from shadowfax.models import *
from flask import request
from bson import ObjectId
import json
import difflib
import requests

@app.route("/")
def hello():
        return "Hello World!!!"

@app.route("/landmarks")
def landMarks():
        arg = request.args
        order_id=arg.get("order_id")
	dataType=arg.get("type")	
	order = Orders.objects.get(order_id=order_id)
	maximumRatio=0.5
	relatedId=None
	mappings = AddressMapping.objects
	for address in mappings:
		percent = difflib.SequenceMatcher(None,order.house_number,address.house_number).ratio()
		if percent>maximumRatio:
			maximumRatio=percent
			relatedId=address.id
	data = {}
	data["latitude"] = order.delivered_latitude
	data["longitude"] = order.delivered_longitude
	if relatedId==None:
		url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyBXlR4n5T_yKXDesqcU_qrZXHcAQIOuAkY&location="+order.delivered_latitude+","+order.delivered_longitude
		if dataType is None:
			url +="&radius=500"
		else:
			url +="&rankby=distance&type="+dataType
		result = requests.get(url).json()["results"]
		landMarks = []
		for res in result:
			if 'name' in res:
				landMarks.append(res["name"])
		landmarks = landMarks[:3]
		addressmaps = AddressMapping(
			house_number=order.house_number,
			latitude = order.delivered_latitude,
			longitude = order.delivered_longitude,
			google_sugg_landmark=landmarks)
		addressmaps.save()			
	else:
		addressmaps = AddressMapping.objects.get(id=relatedId)
		data["latitude"] = addressmaps.latitude
		data["longitude"] = addressmaps.longitude
		landMarks=addressmaps.user_landmark
		landMarks += addressmaps.google_useful_landmark
		landMarks += addressmaps.google_sugg_landmark
		landmarks = landMarks[:3]	
	data["landmarks"]=landmarks
	data["ref_id"] = str(addressmaps.id)
        return json.dumps(data)


@app.route('/delivered', methods=['POST'])
def postDelivery():
	latitude = request.form['latitude']
	longitude = request.form['longitude']
	ref_id = ObjectId(request.form['ref_id'])
	google_useful_landmark = str(request.form['google_useful_landmark'])
	user_landmark = str(request.form['user_landmark'])	
	order_id = request.form['order_id']
	order = Orders.objects.get(order_id=order_id)
	address = AddressMapping.objects.get(id=ref_id)
	if address.house_number == order.house_number:
		address.latitude=latitude
		address.longitude = longitude
	if not address.google_useful_landmark:
		address.google_useful_landmark += google_useful_landmark.split(",")
	else:
		address.google_useful_landmark += google_useful_landmark.split(",")
		address.google_useful_landmark = list(set(address.google_useful_landmark))
	if not address.user_landmark:
		address.user_landmark += user_landmark.split(",")
	else:
		address.user_landmark += user_landmark.split(",")
		address.user_landmark = list(set(address.user_landmark))
	address.save()	
		
	return "Success"
