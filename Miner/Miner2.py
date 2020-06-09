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
        subreddit = "videos"
        if validate_input(subreddit) : break
    except Exception:
        print ("Error: Invalid subreddit.")


#setting y=0 to count the posts
y=0

#getting the current time so the API can use the most current possiable
post_time = int(time.time())

#loading up the API
posts_API= 'https://api.pushshift.io/reddit/search/submission/?subreddit=' + subreddit + '&metadata=true&size=0&before=' + str(post_time)
json_data = requests.get(posts_API).json()
post_amount = json_data['metadata']['total_results']

#as we are limited to 1000 submisisons at a time we must divide by 1000 to get the number of requests to do
loopsreq= (post_amount/1000)
#finding the mod of 1000 posts to see what is left for when we loop through the API
last_posts = (post_amount%1000)

#rounding down to get the interger amount
loopsreqint = math.ceil(loopsreq)

nloopsreq = loopsreqint
#opening the file to write into

print(loopsreqint)
print(last_posts)

def get_info(i):

    post_id = json_data['data'][i]['id']
    post_title = json_data['data'][i]['title']
    post_author = json_data['data'][i]['author']
    post_time = json_data['data'][i]['created_utc']
    post_fullurl = json_data['data'][i]['full_link']
    post_originalcontent = json_data['data'][i]['is_original_content']
    post_numcomments = json_data['data'][i]['num_comments']
    post_numcrossposts = json_data['data'][i]['num_crossposts']
    post_score = json_data['data'][i]['score']
    post_awards = json_data['data'][i]['total_awards_received']
    post_upvote_ratio = json_data['data'][i]['upvote_ratio']
    post_video_url = json_data['data'][i]['url']
    print('\n%s' %y)
    #writing to the csv
    filewrite.writerow([y, post_id, post_title, post_author, post_time, post_fullurl, post_originalcontent, post_numcomments, post_numcrossposts, post_score, post_awards, post_upvote_ratio, post_video_url])

with open(subreddit + '.csv', 'w', encoding='utf-8', newline='') as csvfile:

    filewrite=csv.writer(csvfile)
    filewrite.writerow(['Post Number', 'Post ID', 'Title', 'Post Author', 'Time', 'Full Url', 'Original Content', 'Comments Amount', 'Crossposts Amount', 'Post Score', 'Post Awards', 'Post Upvotes Ratio', 'Post Video Url'])

    #API limits to 1000 req so we need to loop through them all
    for x in range(0, loopsreqint):

        #Loading API, lopping through using the last submisisons time and then pulling the next 1000 from that
        main_API = 'https://api.pushshift.io/reddit/submission/search/?subreddit=' + subreddit + '&size=1000&before=' + str(post_time)
        json_data = requests.get(main_API).json()


        nloopsreq = (nloopsreq - 1)

        #seeing if there is a full page of 1000 results aviable, if there is loop through the 1000, if not use the mod variable to see
        if nloopsreq != 0:

            #Looping through to get the 1000 posts, getting the title and the time
            for i in range(1000):
                get_info(i)
                y = y + 1
        else:
            i=0
            for i in range(last_posts):
                get_info(i)
                y = y + 1
