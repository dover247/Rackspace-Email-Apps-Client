import emailandapps
import time

welcome = """
Welcome to the Domain Rename Script by John Pirtle!

This script currently supports provisioning the following:
RSE: mailboxes, aliases
HEX: mailboxes

Make sure API Keys are in a file named customer-config.txt in same directory as this script.

This script can accept a CSV input with three columns and supports mailbox renames:
SourceMailbox | DestinationMailbox | DestinationPassword

example inputs:
user1@domain1.com | user1@domain2.com | Password123
user2A@domain2.com | user2B@domain2.com | Password1234

"""
print(welcome)

acct_num = "all"
old_domain = input("Input old domain.\n")
new_domain = input("Input new domain.\n")

class CheckEm(object):

    def file_accessible(self, filepath, mode="r+"):
        
        try:
            f = open(filepath, mode)
            f.close()
            print("CSV data found.")
        except IOError:
            print("Cannot open file. Closing script.")
            quit()

    def yesno_checkinput(self, inp):

        if (inp != "Y" and inp != "y" and inp != "N" and inp != "n"):
            print("Invalid input. Closing script.")
            quit()

if __name__ == "__main__":

    domainRename = emailandapps.EmailandApps("customer-config.txt")
    check = CheckEm()
    apicounter = 0

    reseller_flag = input("Is this domain rename for a reseller account? (Y/N)\n")
    check.yesno_checkinput(reseller_flag)
    
    name_flag = input("Does the customer want to change any of the RSE usernames for the new domain's mailboxes? (Y/N)\n")
    check.yesno_checkinput(name_flag)

    csv_flag = input("Did the customer provide a CSV of new passwords to use? (Y/N)\n")
    check.yesno_checkinput(csv_flag)

    #set reseller variable
    if(reseller_flag == "Y" or reseller_flag =="y"):
        reseller = True
    else:
        reseller = False

    #logic for getting CSV data and passwords
    if(csv_flag == "Y" or csv_flag == "y" or name_flag == "Y" or name_flag == "y"):
        csv_filepath = input("Input CSV file path.\n")
        check.file_accessible(csv_filepath)
        credz = domainRename.import_csv(csv_filepath)
        pwdata = dict()
        namedata = dict()

        if(csv_flag == "Y" or csv_flag == "y"):
            for index, cred in credz.iterrows():
                name = cred["SourceMailbox"].split('@')
                pwdata[name[0]] = cred["DestinationPassword"]
        else:
            default_pw = input("Input default mailbox password.\n")
            #must meet security requirements        

        if(name_flag == "Y" or name_flag == "y"):
            for index, cred in credz.iterrows():
                old_name = cred["SourceMailbox"].split('@')
                new_name = cred["DestinationMailbox"].split('@')
                namedata[old_name[0]] = new_name[0]
    #print(namedata)#test
    #print(pwdata)#test
    else:
        default_pw = input("Input default mailbox password.\n")
        #must meet security requirements

    #test getting old domain info    
    try:
        getOldDomain = domainRename.get_domain(acct_num, old_domain)
        apicounter += 1
        #print(getOldDomain)#test
    except:
        print("Couldn't find old domain. Closing script.....")
        time.sleep(5)
        quit()

    acct_num = int(getOldDomain["Details"]["accountNumber"])
    domain_details = dict()

    arc_flag = getOldDomain["Details"]["archivingServiceEnabled"]
    service_type = getOldDomain["Details"]["serviceType"]
    pf_flag = getOldDomain["Details"]["publicFoldersEnabled"]
    if service_type == "rsemail" or service_type == "both":
        rseplus_flag = getOldDomain["Details"]["rsEmailProduct"]
        if rseplus_flag == "rse-plus":
            domain_details["rsEmailProduct"] = "rse-plus"
    
    print(domainRename.add_domain(acct_num, new_domain, arc_flag, reseller, domain_details, 0, 0, 25, service_type))
    apicounter += 1    

    adddomainfailflag = input("Verify if domain was added successfully. If not, please add manually in CP.\nReady to continue?(Y/N)")
    check.yesno_checkinput(adddomainfailflag)
    if(adddomainfailflag == "N" or csv_flag == "n"):
        quit()

    getNewDomain = domainRename.get_domain(acct_num, new_domain)#test
    apicounter += 1#test
    #print(getNewDomain)#test

    rsecounter = apicounter
    addrsefail = 0
    addrsefaillist = list()
    renamersefail = 0
    renamersefaillist = list()

    #RSE
    if service_type == "rsemail" or service_type == "both":
        #get mailboxes
        rs_mboxes = domainRename.get_mailboxes(acct_num, old_domain, "rs")        

        #Adding new domain RSE mailboxes
        for mailbox in rs_mboxes['name']:
            rse_mbox = domainRename.get_mailbox(acct_num, mailbox, "rs")
            #print(rse_mbox)#test
            rse_mboxdata = dict()

            #Get RSE mailbox details
            for index, details in rse_mbox.iterrows():
                rse_mboxdata[index] = details["Details"]

            #print(rse_mboxdata)#test

            #Format RSE mailbox details
            rse_mboxdata.pop("currentUsage", None)
            rse_mboxdata.pop("createdDate", None)
            rse_mboxdata.pop("lastLogin", None)            
            rse_mboxdata["businessCity"] = rse_mboxdata["contactInfo.businessCity"]
            rse_mboxdata.pop("contactInfo.businessCity", None)
            rse_mboxdata["businessCountry"] = rse_mboxdata["contactInfo.businessCountry"]
            rse_mboxdata.pop("contactInfo.businessCountry", None)
            rse_mboxdata["businessNumber"] = rse_mboxdata["contactInfo.businessNumber"]
            rse_mboxdata.pop("contactInfo.businessNumber", None)
            rse_mboxdata["businessPostalCode"] = rse_mboxdata["contactInfo.businessPostalCode"]
            rse_mboxdata.pop("contactInfo.businessPostalCode", None)
            rse_mboxdata["businessState"] = rse_mboxdata["contactInfo.businessState"]
            rse_mboxdata.pop("contactInfo.businessState", None)
            rse_mboxdata["businessStreet"] = rse_mboxdata["contactInfo.businessStreet"]
            rse_mboxdata.pop("contactInfo.businessStreet", None)
            rse_mboxdata["customID"] = rse_mboxdata["contactInfo.customID"]
            rse_mboxdata.pop("contactInfo.customID", None)
            rse_mboxdata["employeeType"] = rse_mboxdata["contactInfo.employeeType"]
            rse_mboxdata.pop("contactInfo.employeeType", None)
            rse_mboxdata["faxNumber"] = rse_mboxdata["contactInfo.faxNumber"]
            rse_mboxdata.pop("contactInfo.faxNumber", None)
            rse_mboxdata["firstName"] = rse_mboxdata["contactInfo.firstName"]
            rse_mboxdata.pop("contactInfo.firstName", None)
            rse_mboxdata["generationQualifier"] = rse_mboxdata["contactInfo.generationQualifier"]
            rse_mboxdata.pop("contactInfo.generationQualifier", None)
            rse_mboxdata["homeCity"] = rse_mboxdata["contactInfo.homeCity"]
            rse_mboxdata.pop("contactInfo.homeCity", None)
            rse_mboxdata["homeCountry"] = rse_mboxdata["contactInfo.homeCountry"]
            rse_mboxdata.pop("contactInfo.homeCountry", None)
            rse_mboxdata["homeFaxNumber"] = rse_mboxdata["contactInfo.homeFaxNumber"]
            rse_mboxdata.pop("contactInfo.homeFaxNumber", None)
            rse_mboxdata["homeNumber"] = rse_mboxdata["contactInfo.homeNumber"]
            rse_mboxdata.pop("contactInfo.homeNumber", None)
            rse_mboxdata["homePostalCode"] = rse_mboxdata["contactInfo.homePostalCode"]
            rse_mboxdata.pop("contactInfo.homePostalCode", None)
            rse_mboxdata["homeState"] = rse_mboxdata["contactInfo.homeState"]
            rse_mboxdata.pop("contactInfo.homeState", None)
            rse_mboxdata["homeStreet"] = rse_mboxdata["contactInfo.homeStreet"]
            rse_mboxdata.pop("contactInfo.homeStreet", None)
            rse_mboxdata["initials"] = rse_mboxdata["contactInfo.initials"]
            rse_mboxdata.pop("contactInfo.initials", None)
            rse_mboxdata["lastName"] = rse_mboxdata["contactInfo.lastName"]
            rse_mboxdata.pop("contactInfo.lastName", None)
            rse_mboxdata["mobileNumber"] = rse_mboxdata["contactInfo.mobileNumber"]
            rse_mboxdata.pop("contactInfo.mobileNumber", None)
            rse_mboxdata["notes"] = rse_mboxdata["contactInfo.notes"]
            rse_mboxdata.pop("contactInfo.notes", None)
            rse_mboxdata["organizationUnit"] = rse_mboxdata["contactInfo.organizationUnit"]
            rse_mboxdata.pop("contactInfo.organizationUnit", None)
            rse_mboxdata["organizationalStatus"] = rse_mboxdata["contactInfo.organizationalStatus"]
            rse_mboxdata.pop("contactInfo.organizationalStatus", None)
            rse_mboxdata["pagerNumber"] = rse_mboxdata["contactInfo.pagerNumber"]
            rse_mboxdata.pop("contactInfo.pagerNumber", None)
            rse_mboxdata["title"] = rse_mboxdata["contactInfo.title"]
            rse_mboxdata.pop("contactInfo.title", None)
            rse_mboxdata["userID"] = rse_mboxdata["contactInfo.userID"]
            rse_mboxdata.pop("contactInfo.userID", None)
            #Format forwarding list
            forwarding_list = list()
            for forward in rse_mboxdata["emailForwardingAddressList"]:
                    forwarding = forward.split('@')
                    if forwarding[1] == old_domain:            
                        forwarding_list.append("{}@{}".format(forwarding[0], new_domain))
                    else:
                        forwarding_list.append(forward)
            rse_mboxdata["emailForwardingAddresses"] = ','.join(forwarding_list)
            rse_mboxdata.pop("emailForwardingAddressList", None)

            username = rse_mboxdata["name"]

            try:                
                if(csv_flag == "Y" or csv_flag == "y"):                
                    print("Adding mailbox for " + username + "...")
                    #time.time
                    print(domainRename.add_mailboxrse(acct_num, '{}@{}'.format(username, new_domain), pwdata[username], rse_mboxdata))
                    #time.time
                    rsecounter += 1
                    print("Password: " + pwdata[username])

                else:
                    print("Adding mailbox for " + username + "...")
                    print(domainRename.add_mailboxrse(acct_num, '{}@{}'.format(username, new_domain), default_pw, rse_mboxdata))
                    rsecounter += 1
                    print("Password: " + default_pw)
            except:
                print("Couldn't add mailbox " + username)
                addrsefail += 1
                addrsefaillist.append(username)

            if(name_flag == "Y" or name_flag == "y"):
                try:
                    if(namedata[username] != username):
                        try:
                            print("Renaming mailbox to new name...")
                            print(domainRename.change_mailbox_username(acct_num, username + "@" + new_domain, namedata[username] + "@" + new_domain))
                            rsecounter += 1
                        except:
                            print("Couldn't rename " + username + " to " + namedata[username])
                            renamersefail += 1
                            renamersefaillist.append(username)
                            continue
                except:
                    continue
                    

            if(rsecounter >= 89):
                print("Pausing for a minute to bypass API throttling...")
                time.sleep(61)
                print("Resuming...")
                rsecounter = 0

        print("All RSE mailboxes added!")



        #create RSE aliases
        old_aliases = domainRename.get_aliases(acct_num, old_domain)
        rsealiasfail = 0
        rsealiasfaillist = list()

        #print(old_aliases)#test

        if old_aliases.empty == True:
            print("No RSE aliases.")
        else:
            for alias in old_aliases["name"]:
                old_alias = domainRename.get_alias(acct_num, alias + "@" + old_domain)
                memberlist = list()
                for member in old_alias["emailAddress"]:
                    new_alias = member.split('@')
                    if new_alias[1] == old_domain:            
                        memberlist.append("{}@{}".format(new_alias[0], new_domain))
                    else:
                        memberlist.append(member)
                try:
                    print(domainRename.add_alias(acct_num, alias + "@" + new_domain, memberlist))
                except:
                    print("Couldn't add alias " + alias)
                    rsealiasfail += 1
                    rsealiasfaillist.append(alias)

            print("All RSE aliases added!")

        #Known Issue: If destination alias name already exists, source alias members will not be transferred.

        #No API documentation for Group Lists


    #HEX
    addhexfail = 0
    addhexfaillist = list()
    addalthexfail = 0
    addalthexfaillist = list()

    if service_type == "exchange" or service_type == "both":
        
        if(service_type == "rsemail" or service_type == "both"):
            ex_mboxes = domainRename.get_mailboxes(acct_num, old_domain, "ex")
            hexcounter = rsecounter
        else:
            hexcounter = apicounter
        #print(ex_mboxes)#test

        for index, mailbox in ex_mboxes.iterrows():
            #print("ayyyyyy")#test
            #print(mailbox)#test
            hex_mbox = domainRename.get_mailbox(acct_num, mailbox["name"], "ex")
            #print("ayyyy22222")#test
            #print(hex_mbox)#test
            username = mailbox['name']
            #print("ayy233333")#test
            #print(username)#test
            user = username.split('@')        

            if(csv_flag == "Y" or csv_flag == "y"):
                if(name_flag == "Y" or name_flag == "y"):
                    if(namedata[user[0]] != user[0]):
                        try:
                            #print("if 1")#test
                            print("Adding mailbox for " + user[0] + "...")
                            print(domainRename.add_mailboxhex(acct_num, '{}@{}'.format(namedata[user[0]], new_domain), pwdata[user[0]], mailbox['displayName']))
                            print("Password: " + pwdata[user[0]])
                            #add alternate email address
                            try:
                                print(domainRename.add_mailbox_alternate_address(acct_num, "{}@{}".format(namedata[user[0]], new_domain), "{}@{}".format(namedata[user[0]], new_domain)))
                            except:
                                print("Couldn't add alternate email address " + namedata[user[0]] + " to mailbox " + user[0])
                                addalthexfail += 1
                                addalthexfaillist.append(namedata[user[0]])
                        except:
                            print("Couldn't add " + user[0])
                            addhexfail += 1
                            addhexfaillist.append(user[0])
                        try:
                            print("Renaming mailbox to new name...")
                            print(domainRename.change_mailbox_username(acct_num, username + "@" + new_domain, namedata[username] + "@" + new_domain))
                            rsecounter += 1
                        except:
                            print("Couldn't rename " + username + " to " + namedata[username])
                            renamersefail += 1
                            renamersefaillist.append(username)
                            continue

                        hexcounter += 1
                        
                    else:
                        try:
                        #print("if 2")#test
                            print("Adding mailbox for " + user[0] + "...")
                            print(domainRename.add_mailboxhex(acct_num, '{}@{}'.format(user[0], new_domain), pwdata[user[0]], mailbox['displayname']))
                            print("Password: " + pwdata[user[0]])
                        except:
                            print("Couldn't add " + user[0])
                            addhexfail += 1
                            addhexfaillist.append(user[0])
                        hexcounter += 1
                        
                else:
                    #print("if 3")#test
                    try:
                        print("Adding mailbox for " + user[0] + "...")
                        print(domainRename.add_mailboxhex(acct_num, '{}@{}'.format(user[0], new_domain), pwdata[user[0]], mailbox['displayname']))
                        print("Password: " + pwdata[user[0]])
                    except:
                        print("Couldn't add " + user[0])
                        addhexfail += 1
                        addhexfaillist.append(user[0])
                    hexcounter += 1
            else:
                #print("if 4")#test
                try:
                    print("Adding mailbox for " + username + "...")
                    print(domainRename.add_mailboxhex(acct_num, '{}@{}'.format(username, new_domain), default_pw, mailbox['displayname']))
                    print("Password: " + default_pw)
                except:
                    print("Couldn't add " + user[0])
                    addhexfail += 1
                    addhexfaillist.append(user[0])
                hexcounter += 1

            if(hexcounter >= 89):
                    print("Pausing for a minute to bypass API throttling...")
                    time.sleep(61)
                    print("Resuming...")
                    hexcounter = 0


        #create HEX contacts
            #get old contacts
            #format data
            #add new contacts
        
        #create HEX resources
            #get old resources
            #format data
            #add new resources
        
        #create HEX DLs
            #get old DLs
            #format data
            #add new DLs

        #enable PFs
    
    #error reporting
    print("Errors adding RSE mailboxes: " + str(addrsefail))
    print(addrsefaillist)
    print("Errors adding RSE aliases: " + str(rsealiasfail))
    print(rsealiasfaillist)
    print("Errors renaming RSE mailboxes: " + str(renamersefail))
    print(renamersefaillist)
    print("Errors adding HEX mailboxes: "+ str(addhexfail))
    print(addhexfaillist)

    #putemdown = input("ready to delete?")
    #print("deleting")
    #print(domainRename.delete_domain(acct_num, new_domain))
    #print("deleted")

    #except:
    #    print("Sorry, something went wrong.")