import csv
from shadowfax.models import *
e[]

def readCsv(file):
	with open(file, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		count = 0
		for row in reader:
			count+=1
			if count == 1:
				headers=row
			else:
				location = Locations(uid=row[0],
				rider_id=row[1],
				update_timestamp=row[2],
				latitude=row[3],
				longitude=row[4],
				source=row[5],
				create_timestamp=row[6])
				location.save()

def readOrderCsv(file):
	with open(file, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		count = 0
		for row in reader:
			count+=1
			if count == 1:
				headers=row
			else:	
				order = Orders(order_id=row[0],
				seller_id=row[1],
				rider_id=row[2],
				cluster_id=row[3],
				scheduled_time=row[4],
				allot_time=row[5] if row[5] != 'NULL' else None,
				pickup_time=row[6] if row[6] != 'NULL' else None,
				delivered_time=row[7] if row[7] != 'NULL' else None,
				pickup_latitude=row[8],
				pickup_longitude=row[9],
				delivered_latitude=row[10],
				delivered_longitude=row[11],
				house_number=row[12],
				sublocality=row[13])
				order.save()


def sameLocality():
	done=[]
	for id in range(0,len(orderIds)):
		if id in done:
			continue
		order = Orders.objects.get(order_id=orderIds[id])
		home = order.house_number
		done.append(id)
		print str(order.order_id) +":"+home
		for j in range(id+1,len(orderIds)):
			if j in done:
				continue
			newOrder = Orders.objects.get(order_id=orderIds[j])
			percent=difflib.SequenceMatcher(None,home,newOrder.house_number).ratio()
			if percent>0.6:
				done.append(j)
				print str(newOrder.order_id) +":"+newOrder.house_number
		print "-----"	
