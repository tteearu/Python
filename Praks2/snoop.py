import os
import argparse
import gzip
import urllib
import GeoIP

parser = argparse.ArgumentParser(description='Apache2 log parser')
parser.add_argument("--path", help="Path to Apache2 log files", default="/var/log/apache2")
parser.add_argument("--top-urls", help="Find top URL-s", default="store_true")
parser.add_argument("--geoip", help="Resolve IP-s to country codes", default="store_true")
parser.add_argument("--verbose", help="Increase verbosity", default="store_true")
args = parser.parse_args()

root = "/home/taavi/logs"

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {}
urls = {}
users = {}
ip_addresses = {}
countries = {}
total = 0
usernr = 0

gi = GeoIP.open("GeoIP.dat", GeoIP.GEOIP_MEMORY_CACHE)
 
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
            
            source_ip, _, _, timestamp = source_timestamp.split(" ", 3)
            
            if not ":" in source_ip: #skip IPv6
                ip_addresses[source_ip] = ip_addresses.get(source_ip,0) + 1
                cc = gi.country_code_by_addr(source_ip)
               # print source_ip, "resolve to", cc
                countries[cc] = countries.get(cc, 0) + 1
            
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
    print keyword, "==>", hits, "(", hits * 100 / total, "% of traffic)"

print    
print "Top 5 visited URL-s:"    
results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for path, hits in results [0:5]:
    print path, "==>", hits, "(", hits * 100 / total, "% of traffic)"
    
print    
print "Top 5 IP-addresses:"    
results = ip_addresses.items()
results.sort(key = lambda item:item[1], reverse=True)
for source_ip, hits in results [0:5]:
    print source_ip, "==>", hits, " hits"
    
    
print    
print "Top 5 Countries:"    
results = countries.items()
results.sort(key = lambda item:item[1], reverse=True)
for cc, hits in results [0:5]:
    print cc, "==>", hits, " hits"


print    
print "Top 5 bandwidth hoggers:"    
results =  users.items()
results.sort(key = lambda item:item[1], reverse=True)
for username, hits in results [0:5]:
    def humanize(bytes):
        if bytes < 1024:
            return  "%.2f B" % bytes
        elif bytes < 1024 ** 2:
            return "%.2f kB" % (bytes / 1024.0)
        elif bytes < 1024 ** 3:
            return "%.2f MB" % (bytes / 1024.0 ** 2)
        elif bytes < 1024 ** 4:
            return "%.2f GB" % (bytes / 1024.0 ** 3)
        else:
            return "%.2f TB" % (bytes / 1024.0 ** 4)


        for filename in os.listdir("."):
            mode, inode, devide, nlink, uid, gid, size, atime, mtime, ctime = os.stat(filename)
   #         print filename, humanize(size)
    print username, "==>", humanize(hits)
