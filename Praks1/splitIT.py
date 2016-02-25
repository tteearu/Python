fh = open("access.log")

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {}


for line in fh:

	total = total +1	
	try:
		source_timestamp, request, response, _, _, agent, _= line.split("\"")
		method, path, protocol = request.split(" ")
		print ("User visited URL: http://enos.itcollege.ee" + path)

		for keyword in keywords
		#keyword = 'Windows'
			if keyword in agent:
				try:
					d[keyword] = d[keyword] + 1
				except KeyError:
					d[keyword] = 1

	except ValueError:
		pass
#		print ("Failed to parse",line)
	for keyword in keywords
		#keyword = 'Windows'
		if keyword in agent:
			try:
				d[keyword] = d[keyword] + 1
			except KeyError:
				d[keyword] = 1


print ("Total requests", total)
total = sum(d.values())

print("Total lines with requested keywords:", sum(d.values()))
for key, value in d.items():
	print(key, "==>", value, "(",value * 100.0 / total "%)"

print ("Requests from windows", win)
print ("Percentage of windows requests", win * 100.0 / total ," %" )
print ("Percentage of windows requests %.02f%%" % (win * 100.0 / total ))
