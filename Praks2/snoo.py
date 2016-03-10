import os
import argparse
import gzip
import urllib
import codecs
import GeoIP
from lxml import etree
from lxml.cssselect import CSSSelector
from jinja2 import Environment, FileSystemLoader # This it the templating engine we will use

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
        continue
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

document =  etree.parse(open('templates/BlankMap-World6.svg'))
print countries
for country_code, hits in countries.items():
    max_hits = max(countries.values())
    print"country with max ammount of hits : ", max_hits;
     
    if not country_code: continue #skip localhost,satelite phones etc
    print country_code, hex(hits * 255 / max_hits)[2:] #2: skips the hexadecimal number
    sel = CSSSelector("#" + country_code.lower())
    for j in sel(document):
        j.set("style", "fill:hsl(%d, 80%%, 60%%)"%(120-hits*120/max_hits))
        # Remove styling from children
        for i in j.iterfind("{http://www.w3.org/2000/svg}path"):
            i.attrib.pop("class", "")

with open("buld/highlighted.svg", "w") as fh:
    fh.write(etree.tostring(document))

 
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
    print source_ip, "==>", hits
    
print    
print "Top 5 IP-addresses:"    
results = ip_addresses.items()
results.sort(key = lambda item:item[1], reverse=True)
for source_ip, hits in results [0:5]:
    print source_ip, "==>", hits
    
print    
print "Top 5 Countries:"    
results = countries.items()
results.sort(key = lambda item:item[1], reverse=True)
for cc, hits in results [0:5]:
    print cc, "==>", hits


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
    
    
users = sorted(users.items(), key = lambda item:item[1], reverse=True)
 
env = Environment(
    
    loader=FileSystemLoader(os.path.dirname(__file__)),
    trim_blocks=True)
with codecs.open("build/output.html", "w", encoding="utf-8") as fh:    
    fh.write(env.get_template("templates/index.html").render(locals()))
    # locals() is a dict which contains all locally defined variables ;)
 
#os.system("x-www-browser file://" + os.path.realpath("output.html") + " &")
