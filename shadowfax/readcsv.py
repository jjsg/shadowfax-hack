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

bigOrderIds=[1865297,1868494,1869930,1870558,1870766,1871182,1871378,1874852,1875810,1875964,1876265,1876838,1877367,1883701,1884588,1886294,1888185,1888315,1888929,1890082,1894945,1895003,1895051,1895657,1895799,1895921,1896288,1896304,1896342,1896470,1896928,1897061,1899934,1900711,1904673,1909202,1911570,1911656,1911772,1912131,1919923,1920534,1921011,1924985,1925009,1925373,1925577,1925940,1926425,1926808,1930333,1933196,1933539,1933624,1935256,1935263,1936717,1936869,1936876,1937343,1937379,1937424,1937824,1938018,1938701,1944861,1945301,1948723,1949932,1950922,1951718,1952054]
orderIds=[1870558,1875964,1870766,1871182,1871378,1875810,1895799,1896470,1904673,1874852,1876838,1883701,1895003.1896288]
def sameLocality():
	print("Compaign Orders in Sublocality JP Nagar 7th Phase")
	cont = "y"
	threshold=0.5
	while cont=='y' or cont=='Y':
		print "Calculating for threshold" + str(threshold)
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
				if percent>threshold:
					done.append(j)
					print str(newOrder.order_id) +":"+newOrder.house_number
			print "-----"	
		val=raw_input("What to increment threshold by(0 if done)?");
		if val =='0':
			break
		threshold+=float(val)
