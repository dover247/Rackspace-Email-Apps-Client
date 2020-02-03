import emailandapps
import logging
import pandas
import argparse
import progressbar

parser = argparse.ArgumentParser(prog="python ./massdisabler.py", description="Disable ALL mailboxes on a domain.")
parser.add_argument("domain")
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

accountnumber = "me"
domain = args.domain

emailandapps = emailandapps.EmailandApps('demo-config.txt')
rse_mailboxes = emailandapps.get_mailboxes(accountnumber, domain, 'rs')
hex_mailboxes = emailandapps.get_mailboxes(accountnumber, domain, 'ex')
for rsemailbox in progressbar.progressbar(rse_mailboxes['name'], redirect_stdout=True):
    print(emailandapps.disable_mailbox(accountnumber, rsemailbox, 'rs'))
for hexmailbox in progressbar.progressbar(hex_mailboxes['name'], redirect_stdout=True):
    print(emailandapps.disable_mailbox(accountnumber, hexmailbox, 'ex'))

