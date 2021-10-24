import pandas as pd
data = pd.read_csv("USvideo_no_error.csv")

# Delete the columns unnecessary
del data['thumbnail_link']
del data['comments_disabled']
del data['ratings_disabled']
del data['video_error_or_removed']

# Calculate how many days a video has been in the top trending 
## Turn trending_date and publish_time into date format
data["trending_date"] = pd.to_datetime(data["trending_date"], format = "%y.%d.%m")
data["publish_time"] =  pd.to_datetime(data["publish_time"], format = "%Y-%m-%dT%H:%M:%S.%fZ")

## Calculate the days in the origin data 
data["Days_in_TopTrending"] = (data["trending_date"] - data["publish_time"]).dt.days

## The data shows that there are some videos are listed before being published, which is impossible
# Find and delete data with this error
i = 0 # loop variable
error_index = [] # in order to drop multiple rows at one time
count = 0  # To record how many rows have been deleted

while i < len(data):
    if data["Days_in_TopTrending"][i] < 0:
        error_index.append(i)
        count = count + 1
    i = i + 1

data = data.drop(error_index) # drop the rows with errors
print("There are", count, "errors have been deleted")

## sort the data by Days_in_TopTrending, then we can remove duplicates and keep the one with the longest days
data = data.sort_values("Days_in_TopTrending", ascending=False)
data = data.drop_duplicates(subset = 'video_id', keep='first')

# reset the index of the data. Set as 0 to 6167 from the top to buttom
data = data.reset_index()

# Add some more variables
data['like_rate'] = ''  # how many viewers enjoy the videos, among those who have voted 'like' and 'dislike'

i = 0 #loop variable
while i < len(data):
    if data['likes'][i] == 0 and data['dislikes'][i] == 0:
        data['like_rate'][i] = 0
    else: data['like_rate'][i] = data['likes'][i]/(data['likes'][i] + data['dislikes'][i])
    i = i + 1

data['willing_to_like'] = (data['likes'] + data['dislikes']) / data['views']  # viewers' willingness to vote 'like' or 'dislike'
data['willing_to_comment'] = data['comment_count']/data['views'] # viewers' willingness to make a comment about the video
data['like_or_not'] = ''  # A empty column prepared to insert value



# Determine whether the video is highly-liked based on like_rate
i = 0 # loop variables
while i < len(data):
    if data['willing_to_like'][i] != 0 and data['like_rate'][i] >= 0.9:  
        data['like_or_not'][i] = 1
    else: data['like_or_not'][i] = 0
    # For the videos the has no one like/dislike, or not achieve the threshold,  they will be determined as '0 = not like'
    i = i + 1

data.to_csv('test4.csv')
