import emailandapps
import logging
import pandas
import argparse
import progressbar
import time

parser = argparse.ArgumentParser(
	description="Mass Password Reset tool changes mailbox passwords for a domain.", usage="masspasswordreset.py accountnumber filename password service")
parser.add_argument("accountnumber")
parser.add_argument("filename")
parser.add_argument("password")
parser.add_argument("type", help='ex or rs')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

accountnumber = args.accountnumber
filename = args.filename
password = args.password
service_type = args.type

emailandapps = emailandapps.EmailandApps('customer-config.txt')
mailboxes = emailandapps.import_csv(filename)

for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True):
	print(emailandapps.change_mailbox_password(accountnumber, mailbox, password, service_type))
	time.sleep(2)