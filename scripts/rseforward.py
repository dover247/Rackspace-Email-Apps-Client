import emailandapps
import time

emailandapps = emailandapps.EmailandApps("customer-config.txt")

acct_num = "all"
counter = 1
#bulk add forwarding for RSE mailboxes
# needs csv with three columns
# Username | emailForwardingAddresses | saveForwardedEmail
# exampleuser | user1@domain.com | true
# exampleuser2 | user2@domain.com,user3@domain.com | false

print("Make sure API Keys are in a file named customer-config.txt in same directory as this script.\n")

domain = input("Input domain.\n")
filename = input("Input CSV file path.\n")

try:
    mailboxes = emailandapps.import_csv(filename)
    print(mailboxes)
    for index, mailbox in mailboxes.iterrows():
        mboxdata = dict()
        username = str(mailbox["Username"])
        forwardList = mailbox["emailForwardingAddresses"]
        saveCopy = str(mailbox["saveForwardedEmail"])
        mboxdata["name"] = username
        mboxdata["emailForwardingAddresses"] = forwardList
        mboxdata["saveForwardedEmail"] = saveCopy
        print("Adding forwarding for " + username + "...")
        try:            
            print(emailandapps.edit_mailboxrse(acct_num, '{}@{}'.format(username, domain), mboxdata))            
        except:
            print("Couldn't edit forwarding for " + username)
        time.sleep(2)
    print("All done!")
except FileNotFoundError:
    print("file {} does not exist".format(filename))