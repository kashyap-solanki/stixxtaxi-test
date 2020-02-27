import pprint

from cabby import create_client


#Below is the list of feeds available at hailataxii's stix/taxii discovery service
HailATaxiiFeedList=[
    'guest.Abuse_ch',
    'guest.CyberCrime_Tracker',
    'guest.EmergingThreats_rules',
    'guest.Lehigh_edu',
    'guest.MalwareDomainList_Hostlist',
    'guest.blutmagie_de_torExits',
    'guest.dataForLast_7daysOnly',
    'guest.dshield_BlockList',
    'guest.phishtank_com'
]
#First we create the client we will be requesting feeds from.
#In this test case, we are going to pull the hailaTaxii collections over HTTP @ hailataxi.com/taxii-discovery-service
#To use HTTPs just set the use_https to True, and ensure you are accessing a feel that is HTTPS enabled
client = create_client(
    'hailataxii.com',
    use_https=False,
    discovery_path='/taxii-discovery-service')

# Using this defined "client", the taxii feed allows us to discover the service URLs which we will print names of in the console

print (": Discover_Collections:")
services = client.discover_services()
for service in services:
    print('Service type= {s.type} , address= {s.address}' .format(s=service))
    

#if you do not have a list of the collections predifed, use the service urls for collection_management to gather a list   
#print (": Get_Collections:")
#collections = client.get_collections(
#    uri='http://hailataxii.com/taxii-data')



#For each collection in our list, (manually defined above), we poll threat data and use a count to track how many we've pulled
#up to the count value and print the feed into a file with a name based on the collection
for collection_name in HailATaxiiFeedList:
    print ("Polling :", collection_name, ".. could take a while, please be patient..")
    file = open((collection_name + ".xml"), "w")
    content_blocks = client.poll(collection_name=collection_name)

    count =1
    for block in content_blocks:
        taxii_message=block.content.decode('utf-8')
        file.write(taxii_message)
        count+=1
        if count > 20: #DEFINE HOW MUCH OF THE FEED YOU WANT TO SAMPLE (based on value of 'count > x')
            break
    file.close()
