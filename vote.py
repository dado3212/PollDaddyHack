import requests, re, json, time
requests.packages.urllib3.disable_warnings()

# Created by Alex Beals
# Last updated: January 29th, 2016

# Edited by trashcannot February 20th, 2016

base_url = 'https://polldaddy.com/poll/'
redirect = ""

useragents = []
current_useragent = ''

proxies = []
current_proxy = {'http':''}
current_proxy_num = -1

def get_all_useragents():
    f = open('useragent.txt', 'r')
    for line in f:
        useragents.append(line.rstrip('\n').rstrip('\r'))

def choose_useragent():
    k = random.randint(0, len(useragents)-1)
    current_useragent = useragents[k]
#print current_useragent

def get_all_proxies():
    f = open('proxy.txt', 'r')
    for line in f:
        proxies.append(line.rstrip('\n').rstrip('\r'))

def choose_proxy():
    
    k = random.randint(0, len(proxies)-1)
    current_num = k
    current_proxy['http'] = proxies[k]
    #print current_proxy


def vote_once(form, value):
    
	c = requests.Session()
    #Chooses useragent randomly
    choose_useragent()
    redirect = {"Referer": base_url + str(form) + "/", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "User-Agent": current_useragent, "Upgrade-Insecure-Requests":"1", "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "en-US,en;q=0.8"}
                
    # Chooses proxy randomly
    choose_proxy()
    try:
        init = c.get(base_url + str(form) + "/", headers=redirect, verify=False, proxies=current_proxy)
    except:
        print 'error'
        proxies.remove(current_proxy_num)
        return None

	# Search for the data-vote JSON object
	data = re.search("data-vote=\"(.*?)\"",init.text).group(1).replace('&quot;','"')
	data = json.loads(data)
	# Search for the hidden form value
	pz = re.search("type='hidden' name='pz' value='(.*?)'",init.text).group(1)
	# Build the GET url to vote
    request = "https://polldaddy.com/vote.php?va=" + str(data['at']) + "&pt=0&r=0&p=" + str(form) + "&a=" + str(value) + "%2C&o=&t=" + str(data['t']) + "&token=" + str(data['n']) + "&pz=" + str(pz)
    try:
        send = c.get(request, headers=redirect, verify=False, proxies=current_proxy)
    except:
        print 'error'
        proxies.remove(current_proxy_num)
        return None
    
    return ('revoted' in send.url)

def vote(form, value, times):
	global redirect
    #redirect = {"Referer": base_url + str(form) + "/", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36", "Upgrade-Insecure-Requests":"1", "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "en-US,en;q=0.8"}
	# For each voting attempt
	for i in xrange(1,times+1):
		b = vote_once(form, value)
		# If successful, print that out, else try waiting for 60 seconds (rate limiting)
		if not b:
			print "Voted (time number " + str(i) + ")!"
			time.sleep(3)
		else:
			print "Locked.  Sleeping for 60 seconds."
			i-=1
			time.sleep(60)

# Initialize these to the specific form and how often you want to vote
# These can be found by inspecting page source to get poll ID,
# going to polldaddy.com/poll/<pollID>, and then use some dev tool
# to view the answer id.
poll_id = 0
answer_id = 0
number_of_votes = 0


get_all_proxies()
get_all_useragents()
vote(poll_id, answer_id, number_of_votes)