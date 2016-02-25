import os
 
# Following is the directory with log files,
# On Windows substitute it where you downloaded the files
root = "/home/tteearu/logs"

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {}
urls = {}
users = {}
total = 0
usernr = 0
import gzip
import urllib
 
for filename in os.listdir(root):
    if not filename.startswith("access.log"):
        print "Skipping unknown file:", filename
        continue
    if filename.endswith(".gz"):
        fh = gzip.open(os.path.join(root, filename))   
    else: 
        fh = open(os.path.join(root, filename))   
    print "Going to process:", filename
    for line in fh:
        try:
            source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
            method, path, protocol = request.split(" ")
            _, status_code, content_length, _ = response.split(" ")
            content_length = int(content_length) 
            
            path = urllib.unquote(path)
            url="http://enos.itcollege.ee" + urllib.unquote(path)
            if path.startswith("/~"):
                username, remainder=path[2:].split("/",1)
                #print "Got user: ", username
                try:
                    users[username] = users[username] + content_length
                except:
                    users[username] = content_length
            try:
                urls[path] = urls[path] + 1
            except:
                urls[path] = 1
               # users[username] = 1
            for keyword in keywords:
                if keyword in agent:
                    d[keyword] = d.get(keyword, 0) + 1
                    break
        except ValueError:
            pass
 
total = sum(d.values())
print
print "Total lines:", total  
print
print "Devices:" 
results = d.items()
results.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in results:
    print keyword, "==>", hits, "(", hits * 100 / total, "%)"

print    
print "Top 5 visited URL-s:"    
results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for path, hits in results [0:5]:
    print path, "==>", hits, "(", hits * 100 / total, "%)"

print    
print "Top 5 visited users-s:"    
results =  users.items()
results.sort(key = lambda item:item[1], reverse=True)
for username, hits in results [0:5]:
    print username, "==>", hits / (1024*1024), "MB"
    
    
