#!/usr/bin/env python

import sys
import random
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import os
from baseclass import OkCupid

def loadlists():
	global sendmsgsto
	sendmsgsto = OkCupid.getlist(listpath)
	global sentamessage 
	sentamessage = OkCupid.getlist("./Lists/SentAMessage.txt")

def savelists():
	OkCupid.writelisttofile(listpath, sendmsgsto)
	OkCupid.writelisttofile("./Lists/SentAMessage.txt", sentamessage)

def getauthcode():
	request = urllib2.build_opener()
	request.addheaders.append(OkCupid.cookietuple)
	returnedpage = request.open('http://www.okcupid.com/messages')
	msgs = BeautifulSoup(returnedpage.read()).findAll('li', { 'class' : re.compile('Message*') })
	threadid = random.choice(msgs)['id'].encode('utf-8').replace('message_', '')
	thread = request.open('http://www.okcupid.com/messages?readmsg=true&threadid=' + threadid + '&folder=1')
	return BeautifulSoup(thread.read()).find('input', { 'id' : 'message_authcode' })['value'].encode('utf-8')

def sendmessage(recipent, message, authcode):
	msgdata = {'folderid' : 1, 'contactflag' : 'compose', 'threadid' : '', 'from_msgid' : '', 'reply' : '', 'authcode' : authcode, 'msg_filter' : '', 'r1' : recipent, 'r2' : 'none', 'body' : message, 'sendmsg' : 'SEND MESSAGE'}
	data = urllib.urlencode(msgdata)
	url = 'http://www.okcupid.com/mailbox'
	msgrequest = urllib2.Request(url, data, OkCupid.cookiedict)
	msgrespon = urllib2.urlopen(msgrequest)

if  __name__ =='__main__':
	listpath = str(sys.argv[1])
	nummsgs = int(sys.argv[2])
	authcode = getauthcode()
	loadlists()
	choosenusers = random.sample(sendmsgsto, nummsgs)
	messages = []
	messagefiles = os.listdir("./Messages")
	for filename in messagefiles:
		messages.append(open("./Messages/" + filename).read().encode('utf-8'))
	for user in choosenusers:
		sendmessage(user, random.choice(messages), authcode)
		sendmsgsto.remove(user)
		sentamessage.append(user)
		savelists()
		loadlists()