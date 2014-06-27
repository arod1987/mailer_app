#!/usr/bin/python
import urllib2
import json
import sys

orig_stdout = sys.stdout
f = file('/home/arunkumar/work/rails_projects/mailer_app/script/out.json', 'w')
sys.stdout = f

u='arunkumar'
p='arun123'

def encodeUserData(user, password):
    return "Basic " + (user + ":" + password).encode("base64").rstrip()

review_list_url='http://reviewboard.chronus.com/api/review-requests/'
req = urllib2.Request(review_list_url)
req.add_header('Accept', 'application/json')
req.add_header("Content-type", "application/x-www-form-urlencoded")
req.add_header('Authorization', encodeUserData(u, p))
res = urllib2.urlopen(req)
review_reqs = json.loads(res.read())['review_requests']
counter = 0
print '{'
for review_req in review_reqs:
	review_req_id = review_req['id']
	review_poster = review_req["links"]["submitter"]["title"]
	review_requests_url='http://reviewboard.chronus.com/api/review-requests/'+ str(review_req_id) + '/reviews/'
	review_url = 'http://reviewboard.chronus.com/r/'+ str(review_req_id) + '/'
	if counter!=0:
		print ','
	print '"'+str(review_req_id )+'"' +":" +'{ "url": ' + '"' + review_url +'"'
	req = urllib2.Request(review_requests_url)
	req.add_header('Accept', 'application/json')
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	req.add_header('Authorization', encodeUserData(u, p))
	res = urllib2.urlopen(req)
	reviews = json.loads(res.read())["reviews"]
	rev_id_array = []
	reviewers = []
	json_hash = {}
	for i in reviews:
	  rev_id_array.append(i["id"])
	  reviewers.append(i["links"]["user"]["title"])
	  json_hash[i["links"]["user"]["title"]] = 0
	total_missing_cnt = []
	json_hash_idx = 0
	for review_id in rev_id_array:
	  reviews_comments_url = review_requests_url + str(review_id) + '/diff-comments/'
	  req = urllib2.Request(reviews_comments_url)
	  req.add_header('Accept', 'application/json')
	  req.add_header("Content-type", "application/x-www-form-urlencoded")
	  req.add_header('Authorization', encodeUserData(u, p))
	  res_com = urllib2.urlopen(req)
	  comnt_cnt = json.loads(res_com.read())["total_results"]
	  reviews_replies_intemediate_url = review_requests_url + str(review_id) + '/replies/'
	  req = urllib2.Request(reviews_replies_intemediate_url)
	  req.add_header('Accept', 'application/json')
	  req.add_header("Content-type", "application/x-www-form-urlencoded")
	  req.add_header('Authorization', encodeUserData(u, p))
	  devu = urllib2.urlopen(req)
	  res_int_rep = urllib2.urlopen(req)
	  res_int_rep = json.loads(res_int_rep.read())["replies"]
	  reply_cnt = 0
	  if len(res_int_rep)!=0:
	    reply_id = res_int_rep[0]["id"]
	    reviews_replies_url = reviews_replies_intemediate_url + str(reply_id) + '/diff-comments/'
	    req = urllib2.Request(reviews_replies_url)
	    req.add_header('Accept', 'application/json')
	    req.add_header("Content-type", "application/x-www-form-urlencoded")
	    req.add_header('Authorization', encodeUserData(u, p))
	    res_rep = urllib2.urlopen(req)
	    reply_cnt = json.loads(res_rep.read())["total_results"]
	  total_missing_cnt.append((comnt_cnt-reply_cnt) if (comnt_cnt-reply_cnt>0) else 0)
	  json_hash[reviewers[json_hash_idx]] += total_missing_cnt[json_hash_idx]
	  json_hash_idx += 1
	print ',"review_requester":' + "\"" +str(review_poster) +"\""
	if review_poster in json_hash:
	  del json_hash[review_poster]
	backup = {}
	for key, value in json_hash.items():
		if value!=0:
			backup [str(key)] = value
	json_hash = backup
	print ',"reviewers":'
	
	print json.dumps(json_hash)
	print "}"
        counter +=1


print '}'
sys.stdout = orig_stdout
f.close()
