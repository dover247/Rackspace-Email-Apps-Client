import emailandapps
import logging
import pandas
import argparse
import progressbar

parser = argparse.ArgumentParser(
	description="Mass Resurrection tool able to restore mailboxes (RSE Only)", usage="massresurrection.py accountnumber filename password")
parser.add_argument("accountnumber")
parser.add_argument("filename")
parser.add_argument("password")
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

accountnumber = args.accountnumber
filename = args.filename

emailandapps = emailandapps.EmailandApps('demo-config.txt')

try:
	mailboxes = emailandapps.import_csv(filename)
	for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True):
		print(emailandapps.restore_mailbox(accountnumber, mailbox, args.password))
except FileNotFoundError:
	print("file {} does not exist".format(filename))