#!/usr/bin/python
import urllib2
import json
import sys

orig_stdout = sys.stdout
f = file('/home/arunkumar/work/rails_projects/mailer_app/script/user.json', 'w')
sys.stdout = f

u='arunkumar'
p='arun123'

def encodeUserData(user, password):
    return "Basic " + (user + ":" + password).encode("base64").rstrip()

review_list_url='http://reviewboard.chronus.com/api/users/'
req = urllib2.Request(review_list_url)
req.add_header('Accept', 'application/json')
req.add_header("Content-type", "application/x-www-form-urlencoded")
req.add_header('Authorization', encodeUserData(u, p))
res = urllib2.urlopen(req)
users = json.loads(res.read())['users']

counter = 0
print '{'
for user in users:
	if counter !=0:
		print ','
	print '"'+user['username']+'"',":",'"'+user['email']+'"'
	counter += 1

print '}'

sys.stdout = orig_stdout
f.close()
