# Snippets

- [Adding Aliases](#adding-aliases)
- [Adding email addresses to domain blacklist](#adding-email-addresses-to-domain-blacklist)
- [Adding IP addresses to domain blacklist](#adding-ip-addresses-to-domain-blacklist)
- [Importing CSVs](#importing-csvs)
- [Exporting to CSVs](#exporting-to-csvs)
- [Enabling Public Folders](#enabling-public-folders)
- [RSE & HEX mailbox export](#rse--hex-mailbox-export)
- [Retrieving Mailbox permissions](#retrieving-mailbox-permissions)
  
## Adding Aliases

```python
import emailandapss
emailandapps = emailandapps.EmailandApps('demo-config.txt')
aliases = emailandapps.import_csv('test.csv')
for index,row in aliases.iterrows():
	print(emailandapps.add_alias('me', row['Alias'], row['Addresses']))
```

## Adding email addresses to domain blacklist

```python
import emailandapps
emailandapps = emailandapps.EmailandApps('demo-config.txt')
blacklist = emailandapps.import_csv('test.csv')['Blacklist']
for address in blacklist:
	print(emailandapps.add_domain_spam_blacklist('me', 'raxrse.com', address))
```

## Adding IP addresses to domain blacklist

```python
import emailandapps
emailandapps = emailandapps.EmailandApps('demo-config.txt')
blacklist = emailandapps.import_csv('test.csv')['Ipblacklist']
for address in blacklist:
	print(emailandapps.add_domain_spam_ip_blacklist('me', 'raxrse.com', address))
```

## Importing CSVs

```python
import emailandapps
emailandapps = emailandapps.EmailandApps('demo-config.txt')
print(emailandapps.import_csv('test.csv'))
```
## Exporting to CSVs

```python
import emailandapps
domains = emailandapps.get_domains(['me'])
emailandapps.export(domains, 'test.csv')
```

## Enabling Public Folders

```python
import emailandapps
emailandapps = emailandapps.EmailandApps('demo-config.txt')
print(emailandapps.enable_public_folders('me', 'apitestdomain.com'))
```

## RSE & HEX mailbox export

```python
import emailandapps
emailandapps = emailandapps.EmailandApps('demo-config.txt')
domains = emailandapps.get_domains(['me'])
rsboxes = emailandapps.get_mailboxes(['me'], domains, 'rs')
exboxes = emailandapps.get_mailboxes(['me'], domains, 'ex')
emailandapps.export(rsboxes, 'mailboxes.csv', header=False)
emailandapps.export(exboxes, 'mailboxes.csv', header=False)
```

## Retrieving Mailbox permissions

```python
import emailandapps
emailandapps = emailandapps.EmailandApps('demo-config.txt')
permissions = emailandapps.get_mailbox_permissions('me', 'a.melita@raxmex09.com')
print(permissions)
```