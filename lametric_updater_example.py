#!/usr/bin/python
##->lametric_updater.py
##->purpose: scrape content from website post to user defined api via POST request
##->author: Mo~JR (@2018)
##->pre-req:
##->***script needs read/write access to the directory it is being executed from
#scrape url parse html
import ast, urllib2, urllib, HTMLParser, os, json, time # for file system activities

print('The LaMetric updater script has begun...Please be patience')
# Preliminary items
#Some global variables
#ideas.lego.com url string
myurl = "enter you url here"

#laMetric device url string
url2 = "https://developer.lametric.com/api/v1/dev/widget/update/com.lametric.yourlametricnumberhere/1"

#get working directory for the script
dir_path = os.path.dirname(os.path.realpath(__file__))

#set file path for content received from ideas.lego.com
myfilepath = dir_path + '/' + 'parsed_content'

#set logging dir
mylogpath = dir_path + '/' + 'laMetric_logging'
mylogfile_W = open(mylogpath, 'ab')

def log(entry):
    localtime = time.asctime( time.localtime(time.time()) )
    lt = localtime.strip()
    nlt = lt.replace(' ', '-')
    stamp = nlt + '--' + entry + '\n'
    return stamp

print('The LaMetric updater script has begun...Please be patience')
print('logs can be reviewed here: ', mylogpath)
print('Values retrieved from myurl are located here: ', myurl)
mylogfile_W.write(log('The LaMetric updater script has begun'))

def htmlscraper_routine():
	#scrape the website
	myfile_W = open(myfilepath, 'w')
	line1 = "The value(s) below this line were obtained from: " + myurl
	myfile_W.write(line1)

	class SupportersExtractor(HTMLParser.HTMLParser):
		def reset(self):
			HTMLParser.HTMLParser.reset(self)
			self.in_li = False
			self.next_li_text_pair = None
		def handle_starttag(self, tag, attrs):
			if tag=='li':
				for name, value in attrs:
					if name=='class' and value=='tile-supporters text-center':
						self.next_li_text_pair = [value, '']
						self.in_li = True
						break
		def handle_data(self, data):
			if self.in_li:self.next_li_text_pair[1] += data

		def handle_endtag(self, tag):
			if tag=='li':
				if self.next_li_text_pair is not None:
					myfile_W.write(self.next_li_text_pair[1].rstrip('Supporters  \n'))
				self.next_li_text_pair = None
				self.in_li = False

	if __name__=='__main__':
		p = SupportersExtractor()
		p.feed((urllib2.urlopen(myurl).read()).decode('utf-8'))

	myfile_W.close()

	myfile_R = open(myfilepath, 'r')
	lines = myfile_R.readlines()
	num_supporters = lines[1].strip()
	return num_supporters

def updateLametric(num_supporters):
	# Specify the request type
	method = "POST"
	handler = urllib2.HTTPHandler()

	# create an openerdirector instance
	opener = urllib2.build_opener(handler)
	opener.add_headers = [('Content-length','0')]
	opener.add_headers = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')]
	opener.add_headers = [('Accept-Encoding', 'UTF-8')]
	opener.add_headers = [('Accept', '*/*')]
	opener.add_headers = [('Content-Type', 'application/json')]
	opener.add_headers = [('Cache-Control', 'no-cache')]

	#build json payload - specific to your use case
	json_a = '{"frames": [{"text": "'
	json_b = '","icon": "i4506","index": 0}]}'
	json_full = json_a + scraper_res + json_b

	# build a request including the scraped supporters value
	js = json_full.strip()
	js = ast.literal_eval(json_full)

	#define access token in header
	content_header = {'X-Access-Token': 'YOUR Access Key Here'}

	#submit the POST request
	request = urllib2.Request(url2, data=json.dumps(js, sort_keys=True, indent=2, separators=(',', ': ')), headers=content_header)
	# print request.get_host()
	# print request.get_full_url()
	# print request.get_data()
	# # overload the get method function with a small anonymous function...
	request.get_method = lambda: method

	# try it; catch the result
	try:
	    connection = opener.open(request)
	except urllib2.HTTPError, e:
	    connection = e
	    print e

	# Get Response code from the server
	if connection.code == 200:
		mylogfile_W.write(log('LaMetric_update was successful'))
		print("LaMetric_update was successful")
	else:
		mylogfile_W.write(log('Oops! LaMetric_update encountered an error:', connection.read()))
	    # print("Oops! LaMetric_update encountered an error:", connection.read())

mylogfile_W.write(log('executing htmlscraper_routine'))
#run htmlscraper_routine to pull latest number of supporters value from the web
scraper_res = htmlscraper_routine()

mylogfile_W.write(log('executing updateLametric to update the LaMetric device'))
#run updateLametric to update the device with the current number of supports
updateLametric(scraper_res)


mylogfile_W.write(log('LaMetric updater script has completed.'))
print('LaMetric updater script has completed.')

#close log file
mylogfile_W.close()
