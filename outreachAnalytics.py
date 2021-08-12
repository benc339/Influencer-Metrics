import csv
import os
import urllib
import re
from datetime import datetime, timedelta
#accounts = {channel:[avgViews,totalSales,email,palettesSent,firstOutreach,
#coldOutreachEmails,lastColdOutreach,lastColdOutreachTitle,firstResponse,addressReceived,
#firstVideo,dedicatedVideos,mentions,instagramPosts,code,videosLastMonth,percentEyeshadow
#percentCheapMakeup,percentDupes,avgIntentCheapMakeup,avgComments30,avgLikes30,country,

monthList = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def median(lst):
    n = len(lst)
    s = sorted(lst)
    return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None

def simplifyViews(avgViews):
    if not str(avgViews).isdigit():
        return avgViews
    avgViews=int(avgViews)
    if avgViews < 1000:
        avgViews = avgViews - avgViews % 100
    elif avgViews >20000:
        avgViews= avgViews - avgViews % 10000
    else:
        avgViews = avgViews - avgViews % 1000
    avgViews = str(avgViews)
    if avgViews[-3:]=='000':
        avgViews=avgViews[:-3]+'k'
    if len(avgViews)==5:
           avgViews = avgViews[0]+'.'+avgViews[1]+'M'
    
    return avgViews

def getEmailDate(emailContent):
    for line in emailContent.split('\n'):
        #print line
        if 'date: ' in line.lower() and ',' in line and 'content' not in line.lower():

            date = line.split(', ')[1]
            year = date.split()[2]
            monthCount=0
            for month in monthList:
                monthCount+=1
                if month.lower() in date.lower():
                    break
            month = monthCount
            day = date.split()[0]
            hour = date.split()[3].split(':')[0]
            minute = date.split()[3].split(':')[1]
            second =date.split()[3].split(':')[2]
            timeZone = int(date.split()[4][:3])
            #print timeZone,'timeZone'
            time = int(str(int(hour)-5-timeZone)+minute+second)
            
         
            
            break
    return [month,day,year,time]

def isBefore(date1,date2):

    
    if int(date1[2]) < int(date2[2]):
        return True
    
    elif int(date1[0]) < int(date2[0]) and int(date1[2]) == int(date2[2]):
        return True
    
    elif int(date1[1]) < int(date2[1]) and int(date1[0]) == int(date2[0]):     
        return True
    elif date1[3]<date2[3] and int(date1[1]) == int(date2[1]) and int(date1[0]) == int(date2[0]):   
        return True
    else:
        return False
####################################################################################
    ####################################################################################
    ####################################################################################
####################################################################################
accounts = {}

#loop through phantom channels (every makeup influencer)
endCount = 0
phantomResults = csv.reader(open('results.csv'))
rowCount=0
addedChannels = []
for row in phantomResults:
    channel = row[0]
    if 'Lisa' not in channel:
        continue
        
    if channel in open('finalResults2.txt').read():
        continue
    print channel
    endCount+=1

    rowCount+=1
    
    if channel == 'channelName':
        continue
    if len(channel) < 2:
        continue
    if channel in addedChannels:
        continue

    print channel
    addedChannels.append(channel)
    #append youtubeStats
    ####################
    found=False
    for channelStats in open('youtubeStats.txt').read().split('\n'):
        if channel in channelStats:
            found=True

            break
    if not found:

        channelStats='\t'*30

    try:
        channelLink = row[12]
    except:
        print 'row 12 exception'
        continue
    try:
        country = row[5]
        if country == 'United States':
            country = 'US'
        
        
        
        accounts[channel]=[avgViews,'','','','','','','','','','','','','','','','','',channelStats.split('\t')[2],\
                      channelStats.split('\t')[1],channelStats.split('\t')[3],channelStats.split('\t')[7],channelStats.split('\t')[5],\
                      channelStats.split('\t')[6],row[6],row[9],row[1],'',row[12],country,row[10],row[11],row[15],'','','','','','','','','']
    except:
        accounts[channel]=['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',\
                           '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
        print 'account exception'

    
    #get email
    ####################
    found = False
    ourEmail=''
    for channelEmail in open('youtubeEmails2.txt').read().split('\n'):
        if channel in channelEmail:
            found=True
            ourEmail=channelEmail.split('\t')[3].replace('"','')

            break



    youtubeDescriptionEmail = row[3]
    if '@' not in youtubeDescriptionEmail:
        youtubeDescriptionEmail = row[12]

    if '@' not in youtubeDescriptionEmail:
        youtubeDescriptionEmail=''
    
    
    videoCount=0
    viewCount=0
    if ourEmail == 'mailFound':
        continue
    if '@' not in ourEmail:
        ourEmail =''
    
    print youtubeDescriptionEmail
    print ourEmail

    #get country
    if country == '' or country.isdigit():
        countries = open('influencerCountry.txt').read()
        for line in countries.split('\n'):
            if channel in line:
                country = line.split('\t')[0]
                print 'country',country
                
               
    
    #######################################
    #get email stats
    #######################################
    if ourEmail <> '':
        checkEmail = ourEmail
    elif youtubeDescriptionEmail <> '':
        checkEmail = youtubeDescriptionEmail
    else:
        open('finalResults2.txt','a').write(channel+'\temail not found\n')
        continue
    #get first email from influencer    
    try:
        content = open('AllEmailContent2/'+channel+'-emailContent.txt').read()
    except:
        content =''
    lowestDate = [12,30,2030,242424]
    allEmailContent = []

    for emailContent in content.split('X-Gmail-Labels:'):
       
        if checkEmail in emailContent:
            allEmailContent.append(emailContent)
            try:
                #open(channel+'emailContent.txt','a').write(emailContent+'\n')
                pass
            except:
                #open(channel+'emailContent.txt','w').write(emailContent+'\n')
                pass
            #os.system('emailCOntent.txt')
    
    for emailContent in allEmailContent:
  
        for line in emailContent.split('\n'):
            
            if 'From: ' in line and checkEmail.lower() in line.lower():
         
                date = getEmailDate(emailContent)
          
                if isBefore(date,lowestDate):            
                    lowestDate = date
    lowestFromDate=lowestDate
    firstResponse= lowestFromDate
    print 'firstResponse',lowestFromDate

    #get first cold email
    ####################
    lowestToDate = ''
    lowestDate = [12,30,2030,242424]
    for emailContent in allEmailContent:
         for line in emailContent.split('\n'):
            if 'to: ' in line.lower() and checkEmail.lower() in line.lower():
                date = getEmailDate(emailContent)
          
                if isBefore(date,lowestDate):            
                    lowestDate = date
    if isBefore(lowestDate, lowestFromDate):
        lowestToDate=lowestDate


    firstColdEmail = lowestToDate
    print 'firstColdEmail',firstColdEmail

    #get last cold email 
    ####################
    highestDate = [1,1,1]
    subject = ''
    for emailContent in allEmailContent:
        #emailContent = emailContent.lower()
        for line in emailContent.split('\n'):
            if 'to: ' in line.lower() and checkEmail.lower() in line.lower():
                date = getEmailDate(emailContent)
                print date
                if isBefore(date,lowestFromDate) and isBefore(highestDate,date):            
                    highestDate = date
                    subject = emailContent.split('Subject: ')[1].split('From:')[0].strip()

    if highestDate == [1,1,1]:
        lastColdEmail =''
    else:
        lastColdEmail = highestDate
    print 'lastColdEmail',lastColdEmail
    print subject
    

    addressRecievedDate=''
    #get address received date
    ####################
    address=''
    if isBefore(lowestFromDate,[12,30,2030,242424]):
        lowestDate = [12,30,2030,242424]
        for emailContent in allEmailContent:
            #emailContent = emailContent.lower()
            if 'Content-Type: text/plain;' not in emailContent:
                continue
            for word in emailContent.split('Content-Type: text/plain;')[1].split('Content-Type:')[0].split():
                if len(word) == 5 and word.isdigit():
                    addressRecievedDate = getEmailDate(emailContent)
                    regexp = "[0-9]{1,3} .+, .+, [A-Z]{2} [0-9]{5}"
                    address = re.findall(regexp, emailContent)
    print 'addressRecievedDate',addressRecievedDate
    print address
    
    #get code
    ####################
    code = ''
    foundcode=False
    for emailContent in allEmailContent:
        if 'The code is: ' in emailContent:
            code = emailContent.split('The code is: ')[1].split()[0].replace('(','')\
                   .replace('"','').replace(')','').replace('.','')
        elif '10% code: ' in emailContent:
            code = emailContent.split('10% code: ')[1].split()[0].replace('(','')\
                   .replace('"','').replace(')','').replace('.','')
        elif 'discount code is ' in emailContent:
            code = emailContent.split('discount code is ')[1].split()[0].replace('(','')\
                   .replace('"','').replace(')','').replace('.','')
        elif 'code "' in emailContent:
            code = emailContent.split('code "')[1].split('"')[0]
        
                
    print 'code',code
    

    #get total sales
    ####################
    sales = ''
    for row in csv.reader(open('discounts.csv')):
        if code.lower() in str(row).lower():
            sales = row[3]
    print 'sales',sales


    
    content = csv.reader(open('videos.csv'))
    #get avg views 60 days
    ####################
    try:
        avgViewsContent = open('avgViews2.txt').read().split(channel)[1].split('\n')[0]
        avgViews = avgViewsContent.split('\t')[1]
    
        totalVideosLastTwoMonths = avgViewsContent.split('\t')[2]
    except:
        avgViews = 'not found'
        totalVideosLastTwoMonths = 'not found'
    print avgViews
    print totalVideosLastTwoMonths
    #get influencer alter ego videos
    try:
        alterEgoContent = open('alterEgoViews2.txt').read().split(channel)[1].split('\n')[0]
        alterEgoViews = alterEgoContent.split('\t')[2]
        alterEgoVideos = alterEgoContent.split('\t')[1]
        print alterEgoViews
        print alterEgoVideos
    except:
        alterEgoViews = 'not found'
        alterEgoVideos = 'not found'
        
    #videoDetails.append([videoLink,publishDate,views])
    #number of cold outreaches
    try:
        if isBefore(firstColdEmail,lastColdEmail):
            coldOutreachs='2+'
        else:
            coldOutreachs='1'
    except:
        coldOutreachs='0'
    
    #append outreach stats

    firstVideoDate=''
    
    if lastColdEmail <> '':
        lastColdEmail = str(lastColdEmail[0])+'-'+str(lastColdEmail[1])+'-'+str(lastColdEmail[2])
    if firstColdEmail <> '':
        firstColdEmail = str(firstColdEmail[0])+'-'+str(firstColdEmail[1])+'-'+str(firstColdEmail[2])
    if firstResponse <> '':
        firstResponse = str(firstResponse[0])+'-'+str(firstResponse[1])+'-'+str(firstResponse[2])
    if firstResponse=='12-30-2030':
        firstResponse=''
    if firstVideoDate <> '':
        firstVideoDate = str(firstVideoDate[0])+'-'+str(firstVideoDate[1])+'-'+str(firstVideoDate[2])
    if len(subject) > 40:
        subject = subject[:40]

    if addressRecievedDate <> '':
        addressRecievedDate = str(addressRecievedDate[0])+'-'+str(addressRecievedDate[1])+'-'+str(addressRecievedDate[2])

    
    accounts[channel][1]=sales
    accounts[channel][8]=subject.replace('\n','')
    accounts[channel][16]=code
    accounts[channel][10]=addressRecievedDate
    accounts[channel][7]=lastColdEmail
    accounts[channel][5]=firstColdEmail
    accounts[channel][9]=firstResponse
    #accounts[channel][36]= str(videoDetails)
    accounts[channel][11] = firstVideoDate
    accounts[channel][17]=totalVideosLastTwoMonths
    accounts[channel][0] = avgViews
    accounts[channel][6]=str(coldOutreachs)
    accounts[channel][34] = alterEgoVideos
    alterEgoViews = simplifyViews(alterEgoViews)
    accounts[channel][35] = alterEgoViews
    accounts[channel][37] = youtubeDescriptionEmail
    accounts[channel][38] = ourEmail
    if ourEmail <> youtubeDescriptionEmail:
        accounts[channel][39] = 'no'

    text = channel+'\t'
    for column in accounts[channel]:
        text+=str(column)+'\t'
    open('finalResults2.txt','a').write(text+'\n')
    open('appendedChannels2.txt','a').write(channel+'\n')
        
#print results
####################
finalText =''
for account in accounts:
    text = account+'\t'
    for column in accounts[account]:
        text+=str(column)+'\t'
    finalText+=text+'\n'

open('finalResults3.txt','w').write(finalText)
print rowCount
os.system('finalResults2.txt')
