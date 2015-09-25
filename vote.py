import requests, re, json, time, random
requests.packages.urllib3.disable_warnings()

url = 'https://polldaddy.com/poll/'
redirect = ""

def vote_once(form, value):
	c = requests.Session()
	init = c.get(url + str(form) + "/", headers=redirect, verify=False)
	data = re.search("data-vote=\"(.*?)\"",init.text).group(1).replace('&quot;','"')
	data = json.loads(data)
	pz = re.search("type='hidden' name='pz' value='(.*?)'",init.text).group(1)
	request = "https://polldaddy.com/vote.php?va=" + str(data['at']) + "&pt=0&r=0&p=" + str(form) + "&a=" + str(value) + "%2C&o=&t=" + str(data['t']) + "&token=" + str(data['n']) + "&pz=" + str(pz)
	send = c.get(request, headers=redirect, verify=False)
	return ('revoted' in send.url)

def vote(form, value, times):
	global redirect
	redirect = {"Referer": url + str(form) + "/", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36", "Upgrade-Insecure-Requests":"1", "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "en-US,en;q=0.8"}
	for i in xrange(1,times+1):
		b = vote_once(form, value)
		if not b:
			print "Voted (time number " + str(times) + ")!"
			time.sleep(3)
		else:
			print "Locked.  Sleeping for 60 seconds."
			i-=1
			time.sleep(60)

poll_id = 0
answer_id = 0
number_of_votes = 0

vote(poll_id, answer_id, number_of_votes)