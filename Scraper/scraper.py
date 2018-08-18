import requests
import re
import csv
import time
import math

#checking if the API sends any data back when the user inputs the subreddit
def validate_input(subreddit):
    varification_API = 'https://api.pushshift.io/reddit/submission/search/?subreddit=' + subreddit
    json_data = requests.get(varification_API).json()
    test = json_data['data']
    if str(test) != '[]':
        return True
    return False


while True:
    try:
        subreddit = input("Input in the subreddit you'd like to scrape: ")
        if validate_input(subreddit) : break
    except Exception:
        print ("Error: Invalid subreddit.")


#setting y=0 to count the posts
y=0

#getting the current time so the API can use the most current possiable
post_time = int(time.time())

#loading up the API
posts_API= 'https://api.pushshift.io/reddit/search/submission/?subreddit=wallstreetbets&metadata=true&size=0&before=' + str(post_time)
json_data = requests.get(posts_API).json()
post_amount = json_data['metadata']['total_results']

#as we are limited to 1000 submisisons at a time we must divide by 1000 to get the number of requests to do
loopsreq= (post_amount/1000)

#rounding down to get the interger amount
loopsreqint = math.floor(loopsreq)

#opening the file to write into
with open(subreddit + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
    filewrite=csv.writer(csvfile)
    filewrite.writerow(['Post Number', 'Post ID', 'Title', 'Post Auther', 'Time'])

    #API limits to 1000 req so we need to loop through them all
    for x in range(post_amount):

        #Loading API, lopping through using the last submisisons time and then pulling the next 1000 from that
        main_API = 'https://api.pushshift.io/reddit/submission/search/?subreddit=' + subreddit + '&size=1000&before=' + str(post_time)
        json_data = requests.get(main_API).json()

        #Looping through to get the 1000 posts, getting the title and the time
        for i in range(1000):

            try:
                post_id = json_data['data'][i]['id']
                post_title = json_data['data'][i]['title']
                post_author = json_data['data'][i]['author']
                post_time = json_data['data'][i]['created_utc']
                y = y + 1
                print('\n%s' %y)
                #writing to the csv
                filewrite.writerow([y, post_id, post_title, post_author, post_time])
            except Exception as e:
                print(e)
