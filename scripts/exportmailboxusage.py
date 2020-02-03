import emailandapps
import logging
import argparse
import progressbar
import time

parser = argparse.ArgumentParser(
	description="Export Mailbox Current usage.", usage="exportmailboxusage.py filename type")
parser.add_argument("filename")
parser.add_argument("type", help="rs or ex")
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

emailandapps = emailandapps.EmailandApps('customer-config.txt')
accountnumbers = emailandapps.import_csv(args.filename)['acct']

for accountnumber in progressbar.progressbar(accountnumbers, redirect_stdout=True):
	try:
		domains = emailandapps.get_domains(accountnumber)['name']
		time.sleep(1)
		for domain in domains:
			rs_mailboxes = emailandapps.get_mailboxes(accountnumber, domain, 'rs')['name']
			time.sleep(1)
			
			file = open("mailboxusage.txt", "a")
			for mailbox in rs_mailboxes:
				time.sleep(1)
				file.write("{} {}\n".format(accountnumber, emailandapps.get_mailbox_usage(accountnumber, mailbox, service_type=args.type)))
			
	except KeyError as k:
		pass