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
	#print review_req_id
	review_requests_url='http://reviewboard.chronus.com/api/review-requests/'+ str(review_req_id) + '/reviews/'
	ishan_chappu = 'http://reviewboard.chronus.com/r/'+ str(review_req_id) + '/'
	#review_requests_url='http://reviewboard.chronus.com/api/review-requests/'+ str(7934) + '/reviews/'
	if counter!=0:
		print ','
	print '"'+str(review_req_id )+'"' +":" +'{ "url": ' + '"' + ishan_chappu +'"'
	req = urllib2.Request(review_requests_url)
	req.add_header('Accept', 'application/json')
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	req.add_header('Authorization', encodeUserData(u, p))
	res = urllib2.urlopen(req)
	reviews = json.loads(res.read())["reviews"]
	rev_id_array = []
	reviewers = []
	pooja_bull_shit = {}
	for i in reviews:
	  rev_id_array.append(i["id"])
	  reviewers.append(i["links"]["user"]["title"])
	  pooja_bull_shit[i["links"]["user"]["title"]] = 0
	total_missing_cnt = []
	pooja_total_shit = 0
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
	    #print res_int_rep[0]
	    reviews_replies_url = reviews_replies_intemediate_url + str(reply_id) + '/diff-comments/'
	    req = urllib2.Request(reviews_replies_url)
	    req.add_header('Accept', 'application/json')
	    req.add_header("Content-type", "application/x-www-form-urlencoded")
	    req.add_header('Authorization', encodeUserData(u, p))
	    res_rep = urllib2.urlopen(req)
	    reply_cnt = json.loads(res_rep.read())["total_results"]
	  total_missing_cnt.append((comnt_cnt-reply_cnt) if (comnt_cnt-reply_cnt>0) else 0)
	  pooja_bull_shit [reviewers[pooja_total_shit]] += total_missing_cnt[pooja_total_shit]
	  pooja_total_shit += 1
	#print "total_Missing_counter is " + str(total_missing_cnt)
	#print "List of Reviewers is " 
	#print reviewers
	print ',"review_requester":' + "\"" +str(review_poster) +"\""
	if review_poster in pooja_bull_shit:
	  del pooja_bull_shit[review_poster]
	#print pooja_bull_shit
	backup = {}
	for key, value in pooja_bull_shit.items():
		if value!=0:
			backup [str(key)] = value
			#print key,value
	#print backup
	pooja_bull_shit = backup
	print ',"reviewers":'
	
	print json.dumps(pooja_bull_shit)
	print "}"
        counter +=1


print '}'
sys.stdout = orig_stdout
f.close()
