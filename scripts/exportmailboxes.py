import emailandapps
import logging
import pandas
import argparse
import progressbar

parser = argparse.ArgumentParser(
	description="Mailbox Export tool exports all mailboxes for a domain.", usage="exportmailboxes.py accountnumber domain")
parser.add_argument("accountnumber")
parser.add_argument("-d")
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

accountnumber = args.accountnumber

emailandapps = emailandapps.EmailandApps('demo-config.txt')

if args.d.endswith('.csv'):
	domains = emailandapps.import_csv(args.d)
	for domain in domains['domain']:
		emailandapps.export_csv(emailandapps.get_mailboxes(accountnumber, domain, service_type='rs')['name'], 'mailboxes.csv', mode='a')
		emailandapps.export_csv(emailandapps.get_mailboxes(accountnumber, domain, service_type='ex')['name'], 'mailboxes.csv', header=False, mode='a')
else:
	emailandapps.export_csv(emailandapps.get_mailboxes(accountnumber, args.d, service_type='rs')['name'], 'mailboxes.csv', mode='a')
	emailandapps.export_csv(emailandapps.get_mailboxes(accountnumber, args.d, service_type='ex')['name'], 'mailboxes.csv', header=False, mode='a')