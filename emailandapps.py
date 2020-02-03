import json
import logging
import sys
import time
from base64 import b64encode
from datetime import datetime
from hashlib import sha1

import pandas
import requests


class Operations(object):

	def domains(self, accountnumber, size, offset, contains=''):
		'''returns the domains operations returning all domains'''
		if contains:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains?size={}&offset={}&contains={}'.format(accountnumber, size, offset, contains)
		if not contains:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains?size={}&offset={}'.format(accountnumber, size, offset)

	def mailboxes(self, accountnumber, domain, service_type, size, offset, contains=''):
		'''returns either the rackspace email mailboxes operation or the hosted exchange mailboxes operation returning all mailboxes'''
		if contains:
			return "https://api.emailsrvr.com/v2/customers/{}/domains/{}/{}/mailboxes?size={}&offset={}&contains={}".format(accountnumber, domain, service_type, size, offset, contains)
		if not contains:
			return "https://api.emailsrvr.com/v2/customers/{}/domains/{}/{}/mailboxes?size={}&offset={}".format(accountnumber, domain, service_type, size, offset)

	def info(self, accountnumber):
		'''returns the customers operation for a single customer returning company information'''
		return 'https://api.emailsrvr.com/v2/customers/{}'.format(accountnumber)

	def invoices(self, accountnumber, invoice=''):
		'''returns the invoices operation returning all invoices'''
		if invoice:
			return 'https://api.emailsrvr.com/v2/customers/{}/invoices/{}'.format(accountnumber, invoice)
		if not invoice:
			return 'https://api.emailsrvr.com/v2/customers/{}/invoices'.format(accountnumber)

	def admins(self, accountnumber, pagesize, start, notificationtype, contains=''):
		'''returns the admins operation returning all administrators'''
		if contains:
			return 'https://api.emailsrvr.com/v3/customers/{}/admins/?pagesize={}&start={}&contains={}'.format(accountnumber, pagesize, start, contains)
		if notificationtype:
			return 'https://api.emailsrvr.com/v3/customers/{}/admins/?pagesize={}&start={}&notificationtype={}'.format(accountnumber, pagesize, start, notificationtype)
		if not contains or notificationtype:
			return 'https://api.emailsrvr.com/v3/customers/{}/admins/?pagesize={}&start={}'.format(accountnumber, pagesize, start)

	def admin(self, accountnumber, admin):
		'''returns the admins operation for a single administrator'''
		return 'https://api.emailsrvr.com/v3/customers/{}/admins/{}'.format(accountnumber, admin)

	def account_numbers(self, size, offset):
		'''returns the customers operation returning all customers'''
		return 'https://api.emailsrvr.com/v2/customers/?size={}&offset={}'.format(size, offset)

	def domain(self, accountnumber, domain):
		'''returns the domains operation for a single domain'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}'.format(accountnumber, domain)

	def mailbox(self, accountnumber, domain, service_type, mailbox):
		'''returns either a rackspace email mailbox operation or a hosted exchange mailbox operation for a single user.'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/{}/mailboxes/{}'.format(accountnumber, domain, service_type, mailbox)

	def mailbox_alternate_address(self, accountnumber, domain, service_type, mailbox, address):
		'''returns either a hosted exchange alternate email address mailbox operation for a single user.'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/{}/mailboxes/{}/emailaddresses/{}'.format(accountnumber, domain, service_type, mailbox, address)

	def distribution_list(self, accountnumber, domain, distributionlist):
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/distributionlists/{}'.format(accountnumber, domain, distributionlist)

	def distribution_list_add(self, accountnumber, domain):
		''' returns the host exchange distribution lists operation'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/distributionlists'.format(accountnumber, domain)

	def distribution_lists(self, accountnumber, domain, size, marker):
		''' returns the host exchange distribution lists operation'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/distributionlists?limit={}&marker={}'.format(accountnumber, domain, size, marker)

	def distribution_list_alternate_addresses(self, accountnumber, domain, distributionlist, size):
		''' returns the hosted exchange distribution alternate addresses operation'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/distributionlists/{}/emailaddresses?limit=100'.format(accountnumber, domain, distributionlist)

	def distribution_list_members(self, accountnumber, domain, distributionlist):
		''' returns the host exchange distribution list members operation for a single DL'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/distributionlists/{}/members'.format(accountnumber, domain, distributionlist)

	def distribution_list_senders(self, accountnumber, domain, distributionlist):
		''' returns the host exchange distribution list senders for a single DL'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/distributionlists/{}/senders'.format(accountnumber, domain, distributionlist)

	def distribution_list_errors(self, accountnumber, domain, distributionlist):
		''' returns the host exchange distribution list errors operation for a single DL'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/distributionlists/{}/errors'.format(accountnumber, domain, distributionlist)

	def contacts(self, accountnumber, domain, size, offset, contains=''):
		'''returns the hosted exchange contacts operation'''
		if contains:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/contacts?size={}&offset={}&contains={}'.format(accountnumber, domain, size, offset, contains)
		if not contains:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/contacts?size={}&offset={}'.format(accountnumber, domain, size, offset)

	def contact(self, accountnumber, domain, contact):
		'''return the hosted exchange contacts operation for a single user'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/contacts/{}'.format(accountnumber, domain, contact)

	def resources(self, accountnumber, domain, size, offset, contains=''):
		'''returns the hosted exchange resource operation'''
		if contains:
			return 'https://api.emailsrvr.com/v2/customers/{}domains/{}/ex/resources?size={}&offset={}&contains={}'.format(accountnumber, domain, size, offset, contains)
		if not contains:
			return 'https://api.emailsrvr.com/v2/customers/{}domains/{}/ex/resources/?size={}&offset={}'.format(accountnumber, domain, size, offset)

	def public_folders(self, accountnumber, domain):
		'''returns the hosted exchange domain public folders operation'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/publicfolders'.format(accountnumber, domain)

	def resource(self, accountnumber, domain, resource):
		'''returns the resource operation for a single resource'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/resources/{}'.format(accountnumber, domain, resource)

	def aliases(self, accountnumber, domain):
		'''returns the rackspace email aliases operation'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/rs/aliases'.format(accountnumber, domain)

	def alias(self, accountnumber, domain, alias):
		'''returns the rackspace email aliases operation for a single user'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/rs/aliases/{}'.format(accountnumber, domain, alias)

	def catch_all(self, accountnumber, domain):
		'''returns the catch all operation'''
		return 'https://api.emailsrvr.com/v1/customers/{}/domains/{}/catchalladdress'.format(accountnumber, domain)

	def domain_spam_setting(self, accountnumber, domain):
		'''returns the domain spam settings operation'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/spam/settings'.format(accountnumber, domain)

	def mailbox_spam_setting(self, accountnumber, domain, mailbox):
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/rs/mailboxes/{}/spam/settings'.format(accountnumber, domain, mailbox)

	def domain_spam_blacklist(self, accountnumber, domain, iporemailaddress=''):
		'''return the domain blacklist operation'''
		if iporemailaddress:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/spam/blacklist/{}'.format(accountnumber, domain, iporemailaddress)
		if not iporemailaddress:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/spam/blacklist'.format(accountnumber, domain)

	def domain_spam_ipblacklist(self, accountnumber, domain, iporemailaddress=''):
		'''returns the domain ip blacklist operation'''
		if iporemailaddress:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/spam/ipblacklist/{}'.format(accountnumber, domain, iporemailaddress)
		if not iporemailaddress:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/spam/ipblacklist'.format(accountnumber, domain)

	def domain_spam_safelist(self, accountnumber, domain, iporemailaddress=''):
		'''returns the domain safelist operation'''
		if iporemailaddress:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/spam/safelist/{}'.format(accountnumber, domain, iporemailaddress)
		if not iporemailaddress:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/spam/safelist'.format(accountnumber, domain)

	def domain_spam_ipsafelist(self, accountnumber, domain, iporemailaddress=''):
		'''returns the domain ip safelist operation'''
		if iporemailaddress:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/spam/ipsafelist/{}'.format(accountnumber, domain, iporemailaddress)
		if not iporemailaddress:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/spam/ipsafelist'.format(accountnumber, domain)

	def permissions(self, accountnumber, domain, delegator, delegate=''):
		'''returns the exchange permissions operator'''
		if delegate:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/mailboxes/{}/permissions/{}'.format(accountnumber, domain, delegator, delegate)
		if not delegate:
			return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/ex/mailboxes/{}/permissions'.format(accountnumber, domain, delegator)

	def storage_notifications(self, accountnumber, domain):
		'''returns the domain storage notification operation'''
		return 'https://api.emailsrvr.com/v2/customers/{}/domains/{}/rs/storagenotification'.format(accountnumber, domain)


class EmailandApps(Operations):
	def __init__(self, file):
		self.keys = file
		self.user_agent = 'Python API Client'
		self.accept = 'application/json'
		self.api_url = 'https://api.emailsrvr.com/v2/customers/'
		self.session = requests.session()
		self.colwidth = pandas.set_option('display.max_colwidth', 10000)
		self.session.headers.update(
			{
				'X-Api-Signature': self.construct_signature(),
				'User-Agent': self.user_agent,
				'Accept': self.accept
			}
		)

	def read_keys(self):
		keys = json.load(open(self.keys))
		user_key = keys['user_key']
		secret_key = keys['secret_key']
		return user_key, secret_key

	def construct_signature(self):
		'''Constructs a X-Api-Signature HTTP header.'''

		timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
		sha1hash = self.read_keys()[0].encode()
		sha1hash += self.user_agent.encode()
		sha1hash += timestamp.encode()
		sha1hash += self.read_keys()[1].encode()
		signature = b64encode(sha1(sha1hash).digest()).decode()

		return '{}:{}:{}'.format(self.read_keys()[0], timestamp, signature)

	def import_csv(self, csv):
		'''imports csv'''
		csv = pandas.read_csv(csv)
		csv.index += 1
		return csv

	def export_csv(self, data, filename, header=True, index=False, mode='w'):
		'''exports data to csv'''
		export = pandas.DataFrame(data)
		csv = export.to_csv('{}'.format(filename), header=header, index=index, mode=mode)
		return csv

	def get_storage_notifications(self, accountnumber, domain):
		'''returns storage notifications'''
		storagenotifications = self.session.get(self.storage_notifications('me', domain))
		if storagenotifications.status_code == 403:
			return json.loads(storagenotifications.text)['unauthorizedFault']['message']
		if storagenotifications.status_code == 404:
			return json.loads(storagenotifications.text)['itemNotFoundFault']['message']
		if storagenotifications.status_code == 400:
			return json.loads(storagenotifications.text)['badRequestFault']['message']
		if storagenotifications.status_code == 200:
			storagenotifications = pandas.DataFrame(json.loads(
				storagenotifications.text), index=[domain]).transpose()
			return storagenotifications

	def get_info(self, accountnumber):
		'''returns company information'''
		info = self.session.get(self.info(accountnumber))
		if info.status_code == 403:
			return json.loads(info.text)['unauthorizedFault']['message']
		if info.status_code == 404:
			return json.loads(info.text)['itemNotFoundFault']['message']
		if info.status_code == 400:
			return json.loads(info.text)['badRequestFault']['message']
		if info.status_code == 200:
			info = pandas.io.json.json_normalize(json.loads(info.text)).T
			info.columns = ['Company Information']
			return info

	def get_admins(self, accountnumber, size, offset, contains=''):
		'''returns administrators'''
		admins = self.session.get(self.admins(accountnumber, size, offset, contains))
		if admins.status_code == 200:
			admins = pandas.io.json.json_normalize(json.loads(
				admins.text)['results']).drop(columns='securityQuestions', axis=1)
			admins.index += 1
			return admins
		if not admins.status_code == 200:
			return json.loads(admins.text)['details']

	def get_admin(self, accountnumber, admin):
		'''returns administrator information'''
		data = self.session.get(self.admin(accountnumber, admin))
		if data.status_code == 200:
			return pandas.io.json.json_normalize(json.loads(data.text)).T
		if not data.status_code == 200:
			return json.loads(data.text)['details']

	def archiving(self, accountnumber, domain, archiving):
		'''enable or disable archiving'''
		data = {'archivingServiceEnabled': archiving}
		archiving = self.session.put(self.domain(accountnumber, domain), data=data)
		if archiving.status_code == 403:
			return json.loads(archiving.text)['unauthorizedFault']['message']
		if archiving.status_code == 404:
			return json.loads(archiving.text)['itemNotFoundFault']['message']
		if archiving.status_code == 400:
			return json.loads(archiving.text)['badRequestFault']['message']
		if archiving.status_code == 200:
			return 'archving enabled for {} {}'.format(domain, data['archivingServiceEnabled'])

	def add_distribution_list(self, accountnumber, displayname, distributionList):
		distribution_list = distributionList.split("@")
		data = {"CommonName": distribution_list[0],
				"DisplayName": displayname,
				"Members": {"Recipients":[{"Action": "Add", "Value": "john.pirtle"},{"Action": "Add", "Value": "george.sauceda"},{"Action": "Add", "Value": "daisy.jordan"},{"Action": "Add", "Value": "courtney.ramirez"}]}}
		distributionlist = self.session.post(self.distribution_list_add(accountnumber, distribution_list[1]), data=data)
		if distributionlist.status_code == 403:
			return json.loads(distributionlist.text)['unauthorizedFault']['message']
		if distributionlist.status_code == 404:
			return json.loads(distributionlist.text)['itemNotFoundFault']['message']
		if distributionlist.status_code == 400:
			try:
				return json.loads(distributionlist.text)['validationFault']['message']
			except:
				return json.loads(distributionlist.text)['badRequestFault']['message']
		if distributionlist.status_code == 204:
			return '{} added successfully.'.format(distributionList)

	def add_distribution_list_members(self, accountnumber, distributionlist, users=list()):
		distribution_list = distributionlist.split("@")
		members = []
		recipients = {}
		for user in users:
			members.append({"Action": "Add", "Value": user})
		print(members)
		recipients.update({"DisplayName": "API", "Members": {"Recipients": members}})
		print(recipients)
		members = self.session.put(self.distribution_list(accountnumber, distribution_list[1],  distribution_list[0]), data=recipients)
		if members.status_code == 403:
			return json.loads(members.text)['unauthorizedFault']['message']
		if members.status_code == 404:
			return json.loads(members.text)['itemNotFoundFault']['message']
		if members.status_code == 400:
			try:
				return json.loads(members.text)['validationFault']['message']
			except:
				return json.loads(members.text)['badRequestFault']['message']
		if members.status_code == 204:
			return '{}: members added to {} successfully.'.format(members.status_code,distributionlist)
			#return self.distribution_list(accountnumber, distribution_list[1],  distribution_list[0])



	def add_domain(self, accountnumber, domainame, archiving, reseller, newdata=dict(), exchangemaxnummailboxes=0, rsemailmaxnumbermailboxes=0, rsemailbasemailboxsize=25, service_type='both'):
		'''adds a domain'''
		data = {
					'serviceType': service_type,
					'archivingServiceEnabled': archiving,
			   		'exchangeMaxNumMailboxes': exchangemaxnummailboxes,
					'rsEmailMaxNumberMailboxes': rsemailmaxnumbermailboxes,
   	  		 		'rsEmailBaseMailboxSize': rsemailbasemailboxsize * 1024
				}
		if bool(newdata) != False:
			if newdata["rsEmailProduct"] == "rse-plus":
				data["rsEmailProduct"] = "rse-plus"
		if reseller == False:
			del data["exchangeMaxNumMailboxes"]
			del data["rsEmailMaxNumberMailboxes"]
		domain = self.session.post(self.domain(accountnumber, domainame), data=data)
		if domain.status_code == 403:
			return json.loads(domain.text)['unauthorizedFault']['message']
		if domain.status_code == 404:
			return json.loads(domain.text)['itemNotFoundFault']['message']
		if domain.status_code == 400:
			return json.loads(domain.text)['badRequestFault']['message']
		if domain.status_code == 200:
			return '{} added successfully.'.format(domainame)

	def delete_domain(self, accountnumber, domain):
		'''delete a domain'''
		data = self.session.delete(self.domain(accountnumber, domain))
		if data.status_code == 403:
			return json.loads(data.text)['unauthorizedFault']['message']
		if data.status_code == 404:
			return json.loads(data.text)['itemNotFoundFault']['message']
		if data.status_code == 400:
			return json.loads(data.text)['badRequestFault']['message']
		if data.status_code == 200:
			return '{} deleted successfully.'.format(domain)

	def get_catch_all_address(self, accountnumber, domain):
		'''return catch all address'''
		catch_all = self.session.get(self.catch_all(accountnumber, domain))
		if catch_all.status_code == 403:
			return json.loads(catch_all.text)['unauthorizedFault']['message']
		if catch_all.status_code == 404:
			return json.loads(catch_all.text)['itemNotFoundFault']['message']
		if catch_all.status_code == 400:
			return json.loads(catch_all.text)['badRequestFault']['message']
		if catch_all.status_code == 200:
			catch_all = pandas.DataFrame(json.loads(catch_all.text), index=[''])
			return catch_all

	def get_domain_spam_settings(self, accountnumber, domain):
		'''return domain spam settings'''
		setting = self.session.get(self.domain_spam_setting(accountnumber, domain))
		if setting.status_code == 403:
			return json.loads(setting.text)['unauthorizedFault']['message']
		if setting.status_code == 404:
			return json.loads(setting.text)['itemNotFoundFault']['message']
		if setting.status_code == 400:
			return json.loads(setting.text)['badRequestFault']['message']
		if setting.status_code == 200:
			setting = pandas.DataFrame(json.loads(setting.text))
			return setting

	def get_domain_spam_blacklist(self, accountnumber, domain):
		'''return domain blacklist'''
		blacklist = self.session.get(self.domain_spam_blacklist(
			accountnumber, domain))
		if blacklist.status_code == 403:
			return json.loads(blacklist.text)['unauthorizedFault']['message']
		if blacklist.status_code == 404:
			return json.loads(blacklist.text)['itemNotFoundFault']['message']
		if blacklist.status_code == 400:
			return json.loads(blacklist.text)['badRequestFault']['message']
		if blacklist.status_code == 200:
			blacklist = pandas.DataFrame(json.loads(blacklist.text))
			blacklist.index += 1
			return blacklist

	def get_domain_spam_ip_blacklist(self, accountnumber, domain):
		'''return domain ip_blacklist'''
		ip_blacklist = self.session.get(self.domain_spam_ipblacklist(
			accountnumber, domain))
		if ip_blacklist.status_code == 403:
			return json.loads(ip_blacklist.text)['unauthorizedFault']['message']
		if ip_blacklist.status_code == 404:
			return json.loads(ip_blacklist.text)['itemNotFoundFault']['message']
		if ip_blacklist.status_code == 400:
			return json.loads(ip_blacklist.text)['badRequestFault']['message']
		if ip_blacklist.status_code == 200:
			ip_blacklist = pandas.DataFrame(json.loads(ip_blacklist.text))
			ip_blacklist.index += 1
			return ip_blacklist

	def get_domain_spam_safelist(self, accountnumber, domain):
		'''return domain safelist or ipsafelist'''
		safelist = self.session.get(self.domain_spam_safelist(
			accountnumber, domain))
		if safelist.status_code == 403:
			return json.loads(safelist.text)['unauthorizedFault']['message']
		if safelist.status_code == 404:
			return json.loads(safelist.text)['itemNotFoundFault']['message']
		if safelist.status_code == 400:
			return json.loads(safelist.text)['badRequestFault']['message']
		if safelist.status_code == 200:
			safelist = pandas.DataFrame(json.loads(safelist.text))
			safelist.index += 1
			return safelist

	def get_domain_spam_ip_safelist(self, accountnumber, domain):
		'''return domain safelist or ipsafelist'''
		ip_safelist = self.session.get(self.domain_spam_ipsafelist(
			accountnumber, domain))
		if ip_safelist.status_code == 403:
			return json.loads(ip_safelist.text)['unauthorizedFault']['message']
		if ip_safelist.status_code == 404:
			return json.loads(ip_safelist.text)['itemNotFoundFault']['message']
		if ip_safelist.status_code == 400:
			return json.loads(ip_safelist.text)['badRequestFault']['message']
		if ip_safelist.status_code == 200:
			ip_safelist = pandas.DataFrame(json.loads(ip_safelist.text))
			ip_safelist += 1
			return ip_safelist

	def add_domain_spam_blacklist(self, accountnumber, domain, address):
		blacklist = self.session.post(self.domain_spam_blacklist(
			accountnumber, domain, iporemailaddress=address))
		if blacklist.status_code == 403:
			return json.loads(blacklist.text)['unauthorizedFault']['message']
		if blacklist.status_code == 404:
			return json.loads(blacklist.text)['itemNotFoundFault']['message']
		if blacklist.status_code == 400:
			return json.loads(blacklist.text)['badRequestFault']['message']
		if blacklist.status_code == 200:
			return '{} added to {} blacklist'.format(address, domain)

	def add_domain_spam_ip_blacklist(self, accountnumber, domain, address):
		ip_blacklist = self.session.post(self.domain_spam_ipblacklist(
			accountnumber, domain, iporemailaddress=address))
		if ip_blacklist.status_code == 403:
			return json.loads(ip_blacklist.text)['unauthorizedFault']['message']
		if ip_blacklist.status_code == 404:
			return json.loads(ip_blacklist.text)['itemNotFoundFault']['message']
		if ip_blacklist.status_code == 400:
			return json.loads(ip_blacklist.text)['badRequestFault']['message']
		if ip_blacklist.status_code == 200:
			return '{} added to {} ip blacklist'.format(address, domain)

	def add_domain_spam_safelist(self, accountnumber, domain, address):
		safelist = self.session.post(self.domain_spam_safelist(
			accountnumber, domain, iporemailaddress=address))
		if safelist.status_code == 403:
			return json.loads(safelist.text)['unauthorizedFault']['message']
		if safelist.status_code == 404:
			return json.loads(safelist.text)['itemNotFoundFault']['message']
		if safelist.status_code == 400:
			return json.loads(safelist.text)['badRequestFault']['message']
		if safelist.status_code == 200:
			return '{} added to {} safelist'.format(address, domain)

	def add_domain_spam_ip_safelist(self, accountnumber, domain, address):
		ip_safelist = self.session.post(self.domain_spam_ipsafelist(
			accountnumber, domain, iporemailaddress=address))
		if ip_safelist.status_code == 403:
			return json.loads(ip_safelist.text)['unauthorizedFault']['message']
		if ip_safelist.status_code == 404:
			return json.loads(ip_safelist.text)['itemNotFoundFault']['message']
		if ip_safelist.status_code == 400:
			return json.loads(ip_safelist.text)['badRequestFault']['message']
		if ip_safelist.status_code == 200:
			return '{} added to {} ip safelist'.format(address, domain)

	def get_account_numbers(self):
		'''return all customer accounts'''
		size = 250
		offset = 0
		total = 1
		count = 1
		while offset < total:
			data = self.session.get(self.account_numbers(size, offset))
			if data.status_code == 403:
				return json.loads(data.text)['unauthorizedFault']['message']
			if data.status_code == 404:
				return json.loads(data.text)['itemNotFoundFault']['message']
			if data.status_code == 400:
				return json.loads(data.text)['badRequestFault']['message']
			if data.status_code == 200:
				accounts = pandas.DataFrame(json.loads(data.text)['customers'])
				total = json.loads(data.text)['total']
			offset += size
			count += 1
		return accounts

	def get_distribution_lists(self, accountnumber, domain, limit, marker=''):
		'''returns hosted exchange distribution lists'''
		distributionlists = self.session.get(
			self.distribution_lists(accountnumber, domain, limit, marker))
		if distributionlists.status_code == 403:
			return json.loads(distributionlists.text)['unauthorizedFault']['message']
		if distributionlists.status_code == 404:
			return json.loads(distributionlists.text)['itemNotFoundFault']['message']
		if distributionlists.status_code == 400:
			return json.loads(distributionlists.text)['badRequestFault']['message']
		if distributionlists.status_code == 200:
			distributionlists = pandas.io.json.json_normalize(json.loads(distributionlists.text)['DistributionLists'])
			distributionlists.index += 1
			return distributionlists

	def get_distribution_list_alternate_addresses(self, accountnumber, distributionlist):
		'''return hosted exchange distribution list alternate addresses'''

	def get_distribution_list_members(self, accountnumber, distributionlist):
		'''return hosted exchange distritbution list members'''
		distribution_list = distributionlist.split('@')
		distributionlistmembers = self.session.get(
			self.distribution_list_members(
				accountnumber, distribution_list[1], distribution_list[0]))
		if distributionlistmembers.status_code == 403:
			return json.loads(distributionlistmembers.text)['unauthorizedFault']['message']
		if distributionlistmembers.status_code == 404:
			return json.loads(distributionlistmembers.text)['itemNotFoundFault']['message']
		if distributionlistmembers.status_code == 400:
			return json.loads(distributionlistmembers.text)['badRequestFault']['message']
		if distributionlistmembers.status_code == 200:
			distributionlistmembers = pandas.DataFrame(
				json.loads(distributionlistmembers.text)['Recipients'])
			distributionlistmembers.index += 1
			distributionlistmembers.columns = ['Recipients']
		return distributionlistmembers

	def get_distribution_list_senders(self, accountnumber, distributionlist):
		'''return hosted exchange distribution list senders'''
		distribution_list = distributionlist.split('@')
		distributionlistsenders = self.session.get(
			self.distribution_list_senders(
				accountnumber, distribution_list[1], distribution_list[0]))
		if distributionlistsenders.status_code == 403:
			return json.loads(distributionlistsenders.text)['unauthorizedFault']['message']
		if distributionlistsenders.status_code == 404:
			return json.loads(distributionlistsenders.text)['itemNotFoundFault']['message']
		if distributionlistsenders.status_code == 400:
			return json.loads(distributionlistsenders.text)['badRequestFault']['message']
		if distributionlistsenders.status_code == 200:
			distributionlistsenders = pandas.DataFrame(
				json.loads(distributionlistsenders.text)['Recipients'])
			distributionlistsenders.index += 1
			distributionlistsenders.columns = ['Recipients']
		return distributionlistsenders

	def get_distribution_list_errors(self, accountnumber, distributionlist):
		'''return hosted exchange distribution list errors for a single DL'''
		distribution_list = distributionlist.split('@')
		distributionlisterrors = self.session.get(self.distribution_list_errors(
			accountnumber, distribution_list[1], distribution_list[0]))
		if distributionlisterrors.status_code == 403:
			return json.loads(distributionlisterrors.text)['unauthorizedFault']['message']
		if distributionlisterrors.status_code == 404:
			return json.loads(distributionlisterrors.text)['itemNotFoundFault']['message']
		if distributionlisterrors.status_code == 400:
			return json.loads(distributionlisterrors.text)['badRequestFault']['message']
		if distributionlisterrors.status_code == 200:
			distributionlisterrors = pandas.io.json.json_normalize(
				json.loads(distributionlisterrors.text)['Errors']).T
			distributionlisterrors.columns = [distributionlist]
			return distributionlisterrors

	def get_contacts(self, accountnumber, domain, size, offset):
		'''return hosted exchange contacts'''
		contacts = self.session.get(
			self.contacts(accountnumber, domain, size, offset))
		if contacts.status_code == 403:
			return json.loads(contacts.text)['unauthorizedFault']['message']
		if contacts.status_code == 404:
			return json.loads(contacts.text)['itemNotFoundFault']['message']
		if contacts.status_code == 400:
			return json.loads(contacts.text)['badRequestFault']['message']
		if contacts.status_code == 200:
			contacts = pandas.DataFrame(json.loads(contacts.text)['contacts'])
			contacts.index += 1
			return contacts

	def get_aliases(self, accountnumber, domain):
		'''return rackspace email aliases'''
		aliases = self.session.get(self.aliases(accountnumber, domain))
		if aliases.status_code == 403:
			return json.loads(aliases.text)['unauthorizedFault']['message']
		if aliases.status_code == 404:
			return json.loads(aliases.text)['itemNotFoundFault']['message']
		if aliases.status_code == 400:
			return json.loads(aliases.text)['badRequestFault']['message']
		if aliases.status_code == 200:
			aliases = pandas.DataFrame(json.loads(aliases.text)['aliases'])
			return aliases

	def get_alias(self, accountnumber, aliasname):
		'''return a rackspace email alias'''
		alias_name = aliasname.split('@')
		alias = self.session.get(self.alias(
			accountnumber, alias_name[1], alias_name[0]))
		if alias.status_code == 403:
			return json.loads(alias.text)['unauthorizedFault']['message']
		if alias.status_code == 404:
			return json.loads(alias.text)['itemNotFoundFault']['message']
		if alias.status_code == 400:
			return json.loads(alias.text)['badRequestFault']['message']
		if alias.status_code == 200:
			alias = pandas.DataFrame(json.loads(alias.text)['emailAddressList'])
			alias.index += 1
			return alias

	def add_contact(self, accountnumber, displayname, contactname, externalemail):
		data = {'displayName': displayname,
				'externalEmail': externalemail}
		contact_name = contactname.split('@')
		contact = self.session.post(self.contact(
			accountnumber, contact_name[1], contact_name[0]), data=data)
		if contact.status_code == 403:
			return json.loads(contact.text)['unauthorizedFault']['message']
		if contact.status_code == 404:
			return json.loads(contact.text)['itemNotFoundFault']['message']
		if contact.status_code == 400:
			try:
				return json.loads(contact.text)['validationFault']['message']
			except:
				return json.loads(contact.text)['badRequestFault']['message']
			
		if contact.status_code == 200:
			return '{} contact added successfully.'.format(contactname)

	def add_alias(self, accountnumber, aliasname, members):
		'''adds a rackspace email alias'''
		data = {'aliasEmails': members}
		alias_name = aliasname.split('@')
		alias = self.session.post(self.alias(
			accountnumber, alias_name[1], alias_name[0]), data=data)
		if alias.status_code == 403:
			return json.loads(alias.text)['unauthorizedFault']['message']
		if alias.status_code == 404:
			return json.loads(alias.text)['itemNotFoundFault']['message']
		if alias.status_code == 400:
			return json.loads(alias.text)['validationFault']['message']
		if alias.status_code == 200:
			return '{} alias added successfully.'.format(aliasname)

	def delete_alias(self, accountnumber, aliasname):
		'''delete a rackspace email alias'''
		alias_name = aliasname.split('@')
		alias = self.session.delete(self.alias(
			accountnumber, alias_name[1], alias_name[0]))
		if alias.status_code == 403:
			return json.loads(alias.text)['unauthorizedFault']['message']
		if alias.status_code == 404:
			return json.loads(alias.text)['itemNotFoundFault']['message']
		if alias.status_code == 400:
			return json.loads(alias.text)['badRequestFault']['message']
		if alias.status_code == 200:
			return '{} alias deleted successfully.'.format(aliasname)

	def get_domains(self, accountnumber):
		'''return domains'''
		size = 250
		offset = 0
		total = 1
		alldomains = pandas.DataFrame()
		while offset < total:
			domains = self.session.get(self.domains(accountnumber, size, offset))
			if domains.status_code == 403:
				return json.loads(domains.text)['unauthorizedFault']['message']
			if domains.status_code == 404:
				return json.loads(domains.text)['itemNotFoundFault']['message']
			if domains.status_code == 400:
				return json.loads(domains.text)['badRequestFault']['message']
			if domains.status_code == 200:
				total = json.loads(domains.text)['total']
				domains = pandas.DataFrame(json.loads(domains.text)['domains'])
				domains.index += 1
				offset += size
			alldomains = alldomains.append(domains, ignore_index=True)
		return alldomains

	def get_domain(self, accountnumber, domain):
		'''return a domain'''
		domain = self.session.get(self.domain(accountnumber, domain))
		if domain.status_code == 403:
			return json.loads(domain.text)['unauthorizedFault']['message']
		if domain.status_code == 404:
			return json.loads(domain.text)['itemNotFoundFault']['message']
		if domain.status_code == 400:
			return json.loads(domain.text)['badRequestFault']['message']
		if domain.status_code == 200:
			domain = pandas.io.json.json_normalize(json.loads(domain.text)).T
			domain.columns = ['Details']
			return domain

	def enable_public_folders(self, accountnumber, domain):
		'''enables public folders a domain'''
		data = {'': ''}
		public_folders = self.session.post(
			self.public_folders(accountnumber, domain), data=data)
		if public_folders.status_code == 403:
			return json.loads(public_folders.text)['unauthorizedFault']['message']
		if public_folders.status_code == 404:
			return json.loads(public_folders.text)['itemNotFoundFault']['message']
		if public_folders.status_code == 400:
			return json.loads(public_folders.text)['badRequestFault']['message']
		if public_folders.status_code == 202:
			return '{} public folders enabled'.format(domain)

	def add_mailboxrse(self, accountnumber, username, password, newdata=dict(), service_type='rs', size=25):
		'''adds a rackspace email mailbox'''
		user = username.split('@')
		if newdata == False:
			data = {
					'password': password,
					'size': size * 1024,
					'visibleInRackspaceEmailCompanyDirectory': True,
		 			'visibleInExchangeGAL': True
				}
		else:
			data = newdata
			data['password'] = password

		mailbox = self.session.post(self.mailbox(
			accountnumber, user[1], service_type, user[0]), data=data)
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(mailbox.text)['itemNotFoundFault']['message']
		if mailbox.status_code == 400:
			try:
				return json.loads(mailbox.text)['validationFault']['message']
			except:
				return json.loads(mailbox.text)['badRequestFault']['message']
		if mailbox.status_code == 200:
			return '{} added successfully.'.format(username)

	def edit_mailboxrse(self, accountnumber, username, newdata, service_type='rs'):
		'''edits a rackspace email mailbox'''
		user = username.split('@')
		data = newdata

		mailbox = self.session.put(self.mailbox(
			accountnumber, user[1], service_type, user[0]), data=data)
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(mailbox.text)['itemNotFoundFault']['message']
		if mailbox.status_code == 400:
			try:
				return json.loads(mailbox.text)['validationFault']['message']
			except:
				return json.loads(mailbox.text)['badRequestFault']['message']
		if mailbox.status_code == 200:
			return '{} updated successfully.'.format(username)

	def edit_mailboxhex(self, accountnumber, username, newdata, service_type='ex'):
		'''edits a rackspace email mailbox'''
		user = username.split('@')
		data = newdata

		mailbox = self.session.put(self.mailbox(
			accountnumber, user[1], service_type, user[0]), data=data)
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(mailbox.text)['itemNotFoundFault']['message']
		if mailbox.status_code == 400:
			try:
				return json.loads(mailbox.text)['validationFault']['message']
			except:
				return json.loads(mailbox.text)['badRequestFault']['message']
		if mailbox.status_code == 200:
			return '{} updated successfully.'.format(username)

	def enable_mailbox(self, accountnumber, username, service_type):
		'''enables an existing mailbox'''
		user = username.split('@')
		mailbox = self.session.put(self.mailbox(
			accountnumber, user[1], service_type, user[0]), data={'enabled': True})
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(mailbox.text)['itemNotFoundFault']['message']
		if mailbox.status_code == 400:
			return json.loads(mailbox.text)['validationFault']['message']
			#return json.loads(mailbox.text)['badRequestFault']['message']
		if mailbox.status_code == 200:
			return '{} enabled successfully.'.format(username)

	def add_mailboxhex(self, accountnumber, username, displayname, password, service_type='ex', size=25):
		'''adds a hosted exchange mailbox'''
		user = username.split('@')
		data = {
					'password': password,
			   					'displayName': displayname,
					'size': size * 1024,
			   					'visibleInRackspaceEmailCompanyDirectory': True
				}
		mailbox = self.session.post(self.mailbox(
			accountnumber, user[1], service_type, user[0]), data=data)
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(mailbox.text)['itemNotFoundFault']['message']
		if mailbox.status_code == 400:
			return json.loads(mailbox.text)['badRequestFault']['message']
		if mailbox.status_code == 200:
			return '{} added successfully.'.format(username)
	
	def add_mailbox_permission(self, accountnumber, delegator, delegate, permissions):
		delegator_mailbox = delegator.split("@")
		delegate_mailbox = delegate.split("@")
		data = {'permission': permissions}
		permission = self.session.post(self.permissions(accountnumber, delegator_mailbox[1], delegator_mailbox[0], delegate_mailbox[0]), data=data)
		if permission.status_code == 403:
			return json.loads(permission.text)['unauthorizedFault']['message']
		if permission.status_code == 404:
			return json.loads(permission.text)['itemNotFoundFault']['message']
		if permission.status_code == 400:
			return json.loads(permission.text)['badRequestFault']['message']
		if permission.status_code == 200:
			return '{} now has {} permissions to {}'.format(delegate, permissions, delegator)

	def disable_mailbox(self, accountnumber, username, service_type):
		user = username.split("@")
		mailbox = self.session.put(self.mailbox(accountnumber, user[1], service_type, user[0]), data={'enabled': False})
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(mailbox.text)['itemNotFoundFault']['message']
		if mailbox.status_code == 400:
			return json.loads(mailbox.text)['badRequestFault']['message']
		if mailbox.status_code == 200:
			return '{} disabled successfully.'.format(username)

	def delete_mailbox(self, accountnumber, username, service_type):
		'''delete mailbox'''
		user = username.split('@')
		print(self.mailbox(accountnumber, user[1], service_type, user[0]))
		mailbox = self.session.delete(self.mailbox(
			accountnumber, user[1], service_type, user[0]))
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(mailbox.text)['itemNotFoundFault']['message']
		if mailbox.status_code == 400:
			return json.loads(mailbox.text)['badRequestFault']['message']
		if mailbox.status_code == 200:
			return '{} deleted successfully.'.format(username)
	
	def restore_mailbox(self, accountnumber, username, password, service_type='rs'):
		user = username.split('@')
		mailbox = self.session.post(self.mailbox(
			accountnumber, user[1], service_type, user[0]), data={'recoverDeleted': True, 'password': password})
		print(mailbox)
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(mailbox.text)['itemNotFoundFault']['message']
		if mailbox.status_code == 400:
			return json.loads(mailbox.text)['validationFault']['message']
		if mailbox.status_code == 200:
			return '{} restored successfully.'.format(username)

	def delete_mailbox_permission(self, accountnumber, delegator, delegate):
		delegator_mailbox = delegator.split("@")
		delegate_mailbox = delegate.split("@")
		permission = self.session.delete(self.permissions(accountnumber, delegator_mailbox[1], delegator_mailbox[0], delegate_mailbox[0]))
		if permission.status_code == 403:
			return json.loads(permission.text)['unauthorizedFault']['message']
		if permission.status_code == 404:
			return json.loads(permission.text)['itemNotFoundFault']['message']
		if permission.status_code == 400:
			return json.loads(permission.text)['badRequestFault']['message']
		if permission.status_code == 200:
			return '{} no longer has any permissions to {}'.format(delegate, delegator)

	def get_mailbox(self, accountnumber, username, service_type):
		'''return mailbox details'''
		user = username.split('@')
		mailbox = self.session.get(self.mailbox(
			accountnumber, user[1], service_type, user[0]))
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(pandas.io.json.json_normalize(mailbox.text))
		if mailbox.status_code == 400:
			return json.loads(mailbox.text)['badRequestFault']['message']
		if mailbox.status_code == 200:
			mailbox = pandas.io.json.json_normalize(json.loads(mailbox.text)).T
			mailbox.columns = ['Details']
			return mailbox
	def get_mailbox_usage(self, accountnumber, username, service_type):
		user = username.split('@')
		mailbox = self.session.get(self.mailbox(
			accountnumber, user[1], service_type, user[0]))
		if mailbox.status_code == 403:
			return json.loads(mailbox.text)['unauthorizedFault']['message']
		if mailbox.status_code == 404:
			return json.loads(pandas.io.json.json_normalize(mailbox.text))
		if mailbox.status_code == 400:
			return json.loads(mailbox.text)['badRequestFault']['message']
		if mailbox.status_code == 200:
			mailbox = pandas.io.json.json_normalize(json.loads(mailbox.text)).T
			mailbox.columns = ['Details']
			usage = pandas.DataFrame({'mailbox': username, 'usage': str(mailbox['Details'][1]) + " MB"}, index=[1])
			return usage

	def get_mailbox_alternate_address(self, accountnumber, username, service_type='ex'):
		user = username.split('@')
		alternate_emailaddress = self.session.get(self.mailbox(accountnumber, user[1], service_type, user[0]))
		if alternate_emailaddress.status_code == 403:
			return json.loads(alternate_emailaddress.text)['unauthorizedFault']['message']
		if alternate_emailaddress.status_code == 404:
			return json.loads(pandas.io.json.json_normalize(alternate_emailaddress.text))
		if alternate_emailaddress.status_code == 400:
			return json.loads(alternate_emailaddress.text)['badRequestFault']['message']
		if alternate_emailaddress.status_code == 200:
			alternate_emailaddress = pandas.io.json.json_normalize(json.loads(alternate_emailaddress.text)).T[0]['emailAddressList']
			return pandas.DataFrame(alternate_emailaddress)

	def add_mailbox_alternate_address(self, accountnumber, username, newAddress, service_type='ex'):
		user = username.split('@')
		address = newAddress
		alternate_emailaddress = self.session.post(self.mailbox_alternate_address(accountnumber, user[1], service_type, user[0], address))
		if alternate_emailaddress.status_code == 403:
			return json.loads(alternate_emailaddress.text)['unauthorizedFault']['message']
		if alternate_emailaddress.status_code == 404:
			return json.loads(pandas.io.json.json_normalize(alternate_emailaddress.text))
		if alternate_emailaddress.status_code == 400:
			return json.loads(alternate_emailaddress.text)['badRequestFault']['message']
		if alternate_emailaddress.status_code == 200:
			return '{} successfully added to mailbox {}'.format(address, username)

	def get_mailbox_permissions(self, accountnumber, username):
		user = username.split('@')
		permissions = self.session.get(
			self.permissions(accountnumber, user[1], user[0]))
		if permissions.status_code == 403:
			return json.loads(permissions.text)['unauthorizedFault']['message']
		if permissions.status_code == 404:
			return json.loads(permissions.text)['itemNotFoundFault']['message']
		if permissions.status_code == 400:
			return json.loads(permissions.text)['badRequestFault']['message']
		if permissions.status_code == 200:
			permissions = pandas.DataFrame(json.loads(permissions.text)['permissions'])
			permissions.index += 1
			return permissions



	def change_catch_all_address(self, accountnumber, domain, address):
		'''changes catch all address'''
		data = {'address': address}
		catch_all_address = self.session.put(
			self.catch_all(accountnumber, domain), data=data)
		if catch_all_address.status_code == 403:
			return json.loads(catch_all_address.text)['unauthorizedFault']['message']
		if catch_all_address.status_code == 404:
			return json.loads(catch_all_address.text)['itemNotFoundFault']['message']
		if catch_all_address.status_code == 400:
			return json.loads(catch_all_address.text)['badRequestFault']['message']
		if catch_all_address.status_code == 200:
			return 'catch all address changed to {} for {}'.format(address, domain)

	def change_mailbox_password(self, accountnumber, username, password, service_type):
		'''change mailbox password'''
		data = {'password': password}
		user = username.split('@')
		newpassword = self.session.put(self.mailbox(
					accountnumber, user[1], service_type, user[0]), data=data)
		if newpassword.status_code == 403:
			return json.loads(newpassword.text)['unauthorizedFault']['message']
		if newpassword.status_code == 404:
			return json.loads(newpassword.text)['itemNotFoundFault']['message']
		if newpassword.status_code == 400:
			return json.loads(newpassword.text)['badRequestFault']['message']
		if newpassword.status_code == 200:
			return '{} password changed succsessfully.'.format(username)

	#def change_contact(self, accountnumber, contactname, data={}):
	#	data = {'displayName': displayname,
	#			'externalEmail': externalemail}
	#	contact_name = contactname.split('@')
	#	contact = self.session.post(self.contact(
	#		accountnumber, contact_name[1], contact_name[0]), data=data)
	#	if contact.status_code == 403:
	#		return json.loads(contact.text)['unauthorizedFault']['message']
	#	if contact.status_code == 404:
	#		return json.loads(contact.text)['itemNotFoundFault']['message']
	#	if contact.status_code == 400:
	#		return json.loads(contact.text)['validationFault']['message']
	#	if contact.status_code == 200:
	#		return '{} contact added successfully.'.format(contactname)

	def change_mailbox_username(self, accountnumber, username, newusername, service_type='rs'):
		'''rename mailbox rackspace email only'''
		data = {'name': newusername.split('@')[0]}
		user = username.split('@')
		newusername = self.session.put(self.mailbox(
			accountnumber, user[1], service_type, user[0]), data=data)
		if newusername.status_code == 403:
			return json.loads(newusername.text)['unauthorizedFault']['message']
		if newusername.status_code == 404:
			return json.loads(newusername.text)['unauthorizedFault']['message']
		if newusername.status_code == 400:
			return json.loads(newusername.text)['validationFault']['message']
		if newusername.status_code == 200:
			return '{} renamed to {} successfully,'.format(username, newusername)

	def change_mailbox_permission(self, accountnumber, delegator, delegate, permissions):
		delegator_mailbox = delegator.split("@")
		delegate_mailbox = delegate.split("@")
		data = {'permission': permissions}
		permission = self.session.put(self.permissions(accountnumber, delegator_mailbox[1], delegator_mailbox[0], delegate_mailbox[0]), data=data)
		if permission.status_code == 403:
			return json.loads(permission.text)['unauthorizedFault']['message']
		if permission.status_code == 404:
			return json.loads(permission.text)['itemNotFoundFault']['message']
		if permission.status_code == 400:
			return json.loads(permission.text)['badRequestFault']['message']
		if permission.status_code == 200:
			return "{} now has {} permissions to {}".format(delegate, permissions, delegator)
	
	def change_rse_mailbox_spam_setting(self, accountnumber, username, filterlevel, spamfolderagelimit, spamfoldernumlimit, spamhandling='toFolder', foldercleaner=True):
		user = username.split("@")
		data = {'filterLevel': filterlevel,
				'rsEmail.spamHandling': spamhandling,
				'rsEmail.hasFolderCleaner': foldercleaner,
				'rsEmail.spamFolderAgeLimit': spamfolderagelimit,
				'rsEmail.spamFolderNumLimit': spamfoldernumlimit}
		spam_setting = self.session.put(self.mailbox_spam_setting(accountnumber, user[1], user[0]), data=data)
		if spam_setting.status_code == 403:
			return json.loads(spam_setting.text)['unauthorizedFault']['message']
		if spam_setting.status_code == 404:
			return json.loads(spam_setting.text)['itemNotFoundFault']['message']
		if spam_setting.status_code == 400:
			return json.loads(spam_setting.text)['badRequestFault']['message']
		if spam_setting.status_code == 200:
			return "{} mailbox spam settings changed successfully".format(username)

	def get_mailboxes(self, accountnumber, domain, service_type, contains=''):
		'''return mailboxes for a domain\n
		accountnumber: str\n
		domain: str\n
		service_type: str\n
		contain: str'''
		mailboxes = list()
		displaynames = list()
		size = 250
		offset = 0
		total = 1
		while offset < total:
			data = self.session.get(self.mailboxes(
				accountnumber, domain, service_type, size, offset, contains))
			if data.status_code == 403:
				return json.loads(data.text)['unauthorizedFault']['message']
			if data.status_code == 404:
				return json.loads(data.text)['itemNotFoundFault']['message']
			if data.status_code == 400:
				return data.text
			if data.status_code == 200:
				total = json.loads(data.text)['total']
				try:
					if service_type == 'rs':
						users = pandas.DataFrame(json.loads(data.text)['rsMailboxes'])
						for user in users['name']:
							mailboxes.append('{}@{}'.format(user, domain))
					elif service_type == 'ex':
						users = pandas.DataFrame(json.loads(data.text)['mailboxes'])
						for user in users['name']:
								mailboxes.append('{}@{}'.format(user, domain))
						for display_name in users['displayName']:
							displaynames.append('{}'.format(display_name))
				except KeyError:
					continue
			offset += 250
		if service_type == 'ex':
			pair = pandas.DataFrame({'name': mailboxes, 'displayname': displaynames})
		if service_type == 'rs':
			pair = pandas.DataFrame({'name': mailboxes})
		pair.index += 1
		return pair


if __name__ == "__main__":
	pass
