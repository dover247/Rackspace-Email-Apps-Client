import emailandapps
import progressbar
import argparse
import time
import os


parser = argparse.ArgumentParser(
	prog='jiren.py',
	description="""


	   _ _____ _____  ______ _   _ 
	  | |_   _|  __ \|  ____| \ | |
	  | | | | | |__) | |__  |  \| |
  _   | | | | |  _  /|  __| | . ` |
 | |__| |_| |_| | \ \| |____| |\  |
  \____/|_____|_|  \_\______|_| \_|

**FOR INTERNAL USE ONLY**

A Rackspace Email & Apps api client designed to automate large tasks such as adding, deleting, editing, mailboxes to exporting data and more.
	""",
	usage='%(prog)s [--command] [subcommand] [-options]',
	epilog='''

sub commands:
domain
mailbox
contact
alias				
alternateaddress
distributionlist



EXAMPLES

jiren.py --get alias -a alias@raxrse.com
jiren.py --edit forwarding -i rsefwd.csv -t rs
jiren.py --reset mailbox -m thescriptkid@apitestdomain.com -p Hardpassw0rd12#
 
''',
	formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--acct', metavar='1213514',
					help='account number', default='me')
parser.add_argument('--reset', metavar='mailbox', help='reset password')
parser.add_argument('--get', metavar='mailbox', help='retrieve resource data')
parser.add_argument('--delete', metavar='alias', help='delete a resource')
parser.add_argument('--restore', metavar='mailbox',
					help='restore mailbox(RSE ONLY)')
parser.add_argument('--add', metavar='domain', help='add a resource')
parser.add_argument('--edit', metavar='mailbox', help='edit a resource')
parser.add_argument('--disable', metavar='mailbox', help='disable mailboxes')
parser.add_argument('--export', metavar='mailbox', help='export data')

parser.add_argument('-a', metavar='alias@domain.com', help='set alias')
parser.add_argument('-d', metavar='domain.com', help='set domain')
parser.add_argument(
	'-aA', metavar='alternateaddress@domain.com', help='set alternate address')
parser.add_argument('-m', metavar='mailbox@domain.com',
					nargs='+', help='set mailbox')
parser.add_argument('-c', metavar='contact@domain.com', help='set contact')
parser.add_argument('-iB', metavar='ipblacklist.csv',
					help='set ip blacklist file')
parser.add_argument('-iS', metavar='ipsafelist.csv',
					help='set ip safelist file')
parser.add_argument(
	'-dL', metavar='distribution_list@domain.com', help='set distribution list')
parser.add_argument('-mP', metavar='fullaccess', help='set mailbox permission')
parser.add_argument('-t', metavar='rs',
					help='set product type', choices=['rs', 'ex'])
parser.add_argument('-attr', metavar='enabled', help='set attribute')
parser.add_argument('-i', metavar='input file', help='input file')
parser.add_argument('-o', metavar='output file', help='output file')
parser.add_argument('-p', metavar='Hardpassword', help='set password')
args = parser.parse_args()

emailandapps = emailandapps.EmailandApps('demo-config.txt')
export_dir = "C:{}\\scripts\\exports\\".format(os.environ['HOMEPATH'])
print(args)


# Retrieve Resource Information
if args.get:
	if "mailbox" in args.get:
		if args.m:
			try:
				mailbox = emailandapps.get_mailbox(args.acct, args.m[0], 'rs')
				print(mailbox)
			except:
				mailbox = emailandapps.get_mailbox(args.acct, args.m[0], 'ex')
				print(mailbox)
		elif args.d:
			print()
			print('Rackspace Email')
			mailboxes = emailandapps.get_mailboxes(args.acct, args.d, 'rs')
			print(mailboxes)
			mailboxes = emailandapps.get_mailboxes(args.acct, args.d, 'ex')
			print()
			print('Exchange')
			print(mailboxes)
		else:
			parser.print_help()
	elif "alias" in args.get:
		if args.d:
			alias = emailandapps.get_aliases(args.acct, args.d)
			print(alias)
		elif args.a:
			aliases = emailandapps.get_alias(args.acct, args.a)
			print(aliases)
	else:
		parser.print_help()

elif args.edit:
	if 'mailbox' in args.edit:
		if 'rs' in args.t:
			# resume here
			mailboxes = emailandapps.import_csv(args.i)
			for row, mailbox in mailboxes.iterrows():
				print(emailandapps.edit_mailboxrse(args.acct, mailbox['Username'], {
					'emailForwardingAddresses': mailbox['emailForwardingAddresses'], 'saveForwardedEmail': mailbox['saveForwardedEmail']}, 'rs'))
				time.sleep(2)
elif args.export:
	if 'mailboxusage' in args.export:
		if args.i:
			try:
				accountnumbers = emailandapps.import_csv(args.i)['account']
				for accountnumber in progressbar.progressbar(accountnumbers, redirect_stdout=True, min_value=1):
					domains = emailandapps.get_domains(accountnumber)['name']
					time.sleep(1)
					for domain in domains:
						rs_mailboxes = emailandapps.get_mailboxes(
							accountnumber, domain, 'rs')['name']
						time.sleep(1)
						ex_mailboxes = emailandapps.get_mailboxes(
							accountnumber, domain, 'ex')['name']
						for mailbox in rs_mailboxes:
							mailbox_usage = emailandapps.get_mailbox_usage(
								accountnumber, mailbox, 'rs')
							emailandapps.export_csv(mailbox_usage, '{}{}'.format(
								export_dir, args.o), mode='a', header=False)
							time.sleep(1)
						for mailbox in ex_mailboxes:
							mailbox_usage = emailandapps.get_mailbox_usage(
								accountnumber, mailbox, 'ex')
							emailandapps.export_csv(mailbox_usage, '{}{}'.format(
								export_dir, args.o), header=False, mode='a')
							time.sleep(1)
			except KeyError:
				pass
			except IndexError:
				pass
			except FileNotFoundError:
				print("file not found")
		else:
			parser.print_help()

	elif 'mailbox' in args.export:
		if args.i:
			domains = emailandapps.import_csv(args.i)
			for domain in domains['name']:
				emailandapps.export_csv(emailandapps.get_mailboxes(args.acct, domain, service_type='rs')[
										'name'], '{}{}'.format(export_dir, args.o), mode='a')
				emailandapps.export_csv(emailandapps.get_mailboxes(args.acct, domain, service_type='ex')[
										'name'], '{}{}'.format(export_dir, args.o), header=False, mode='a')
		elif args.d:
			emailandapps.export_csv(emailandapps.get_mailboxes(args.acct, args.d, service_type='rs')[
				'name'], '{}{}'.format(export_dir, args.o), mode='a')
			emailandapps.export_csv(emailandapps.get_mailboxes(args.acct, args.d, service_type='ex')[
				'name'], '{}{}'.format(export_dir, args.o), header=False, mode='a')

	else:
		parser.print_help()

# Reset Passwords for Microsoft Exchange or Rackspace Email Mailboxes
elif args.reset:
	if 'import' in args.reset:
		mailboxes = emailandapps.import_csv(args.i)
		for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True, min_value=1):
			print(emailandapps.change_mailbox_password(
				args.acct, mailbox, args.p, args.t))
			time.sleep(2)
	elif 'domain' in args.reset:
		mailboxes = emailandapps.get_mailboxes(
			args.acct, args.d, 'rs')
		for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True, min_value=1):
			print(emailandapps.change_mailbox_password(
				args.acct, mailbox, args.p, 'rs'))
		mailboxes = emailandapps.get_mailboxes(
			args.acct, args.d, 'ex')
		for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True, min_value=1):
			print(emailandapps.change_mailbox_password(
				args.acct, mailbox, args.p, 'ex'))
	elif 'mailbox' in args.reset:
		try:
			mailbox = emailandapps.get_mailbox(args.acct, args.m[0], 'rs')
			print(emailandapps.change_mailbox_password(
				args.acct, args.m[0], args.p, 'rs'))
		except:
			print(emailandapps.change_mailbox_password(
				args.acct, args.m[0], args.p, 'ex'))
	else:
		parser.print_help()

# Delete a resource
elif args.delete:
	if 'import' in args.delete:
		if 'rs' in args.t:
			mailboxes = emailandapps.import_csv(args.i)
			for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True, min_value=1):
				print(emailandapps.delete_mailbox(
					args.acct, mailbox, 'rs'))
				time.sleep(3)
		elif 'ex' in args.t:
			mailboxes = emailandapps.import_csv(args.i)
			for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True, min_value=1):
				print(emailandapps.delete_mailbox(
					args.acct, mailbox, 'ex'))
				time.sleep(3)
	elif 'domain' in args.delete:
		if 'rs' in args.t:
			mailboxes = emailandapps.get_mailboxes(args.acct, args.d, 'rs')
			for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True, min_value=1):
				print(emailandapps.delete_mailbox(
					args.acct, mailbox, 'rs'))
				time.sleep(3)
		elif 'ex' in args.t:
			mailboxes = emailandapps.get_mailboxes(args.acct, args.d, 'ex')
			for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True, min_value=1):
				print(emailandapps.delete_mailbox(
					args.acct, mailbox, 'ex'))

	elif 'mailbox' in args.delete:
		try:
			mailbox = emailandapps.get_mailbox(args.a, args.m, 'rs')
			print(emailandapps.delete_mailbox(args.a, args.m, 'rs'))
		except:
			print(emailandapps.delete_mailbox(args.a, args.m, 'ex'))
	else:
		parser.print_help()

# Add a Resource
elif args.add:
	if 'mailbox' in args.add:
		if 'rs' in args.t:
			print(emailandapps.add_mailboxrse(
				args.acct, args.add.m, args.p))
		elif 'ex' in args.t:
			print(emailandapps.add_mailboxhex(args.acct,
											  args.m[0], args.m[1], args.p))
	else:
		parser.print_help()

# Disable Microsoft Exchange or Rackspace Email Mailboxes
elif args.disable:
	if 'domain' in args.disable:
		rse_mailboxes = emailandapps.get_mailboxes(
			args.acct, args.d, 'rs')
		hex_mailboxes = emailandapps.get_mailboxes(
			args.acct, args.d, 'ex')
		for rsemailbox in progressbar.progressbar(rse_mailboxes['name'], redirect_stdout=True, min_value=1):
			print(emailandapps.disable_mailbox(
				args.acct, rsemailbox, 'rs'))
		for hexmailbox in progressbar.progressbar(hex_mailboxes['name'], redirect_stdout=True, min_value=1):
			print(emailandapps.disable_mailbox(
				args.acct, hexmailbox, 'ex'))
	elif 'mailbox' in args.disable:
		try:
			mailbox = emailandapps.get_mailbox(args.a, args.m, 'rs')
			print(emailandapps.disable_mailbox(
				args.a, args.m, 'rs'))
		except:
			print(emailandapps.disable_mailbox(
				args.a, args.m, 'ex'))
	else:
		parser.print_help()

# Restore Rackspace Email Mailboxes
elif args.restore:
	if 'import' in args.restore:
		mailboxes = emailandapps.import_csv(args.i)
		for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True, min_value=1):
			print(emailandapps.restore_mailbox(
				args.acct, mailbox, 'rs'))
	elif 'domain' in args.restore:
		mailboxes = emailandapps.get_mailboxes(
			args.acct, args.d, 'rs')
		for mailbox in progressbar.progressbar(mailboxes['name'], redirect_stdout=True, min_value=1):
			print(emailandapps.restore_mailbox(
				args.acct, mailbox, args.restore[2], 'rs'))
	elif 'mailbox' in args.restore:
		print(emailandapps.restore_mailbox(
			args.acct, args.m, 'rs'))
else:
	parser.print_help()
