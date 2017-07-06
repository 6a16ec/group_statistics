import time, vk_api
#input data
group_id =			# (!)filling required(!)
login = ''			# (!)filling required(!)
password = ''			# (!)filling required(!)
monitoring_hours = -1	# may required # 1 - 72 # -1 if only this day
number_of_posts = 50	# may required # 1 - 100
#authorization
vk = vk_api.VkApi(login = login, password = password)
vk.auth()
# variables for calculations
array_id = []
array_count = []
max_comments = 0
max_id = 0
#calcilation monitoring_seconds
if(monitoring_hours == -1):
	monitoring_seconds = time.localtime()[3]*60*60 + time.localtime()[4]*60 + time.localtime()[5]
	comments_monitoring_seconds = monitoring_seconds
else:
	monitoring_seconds = monitoring_hours*60*60
	comments_monitoring_seconds = 24*60*60

#receipt of all posts for the past 24 hours
posts = vk.method('newsfeed.get', {'filters': 'post', 'return_banned': 0, 'start_time': time.time() - monitoring_seconds, 'source_ids': group_id, 'count': number_of_posts})

for post in posts['items']:
	#getting the number of comments
	count_comments =  post['comments']['count']
	#getting id of a post
	post_id = post['post_id']
	#view all comments
	i = 0
	while(i <= count_comments/100):

		comments = vk.method('wall.getComments', {'owner_id': group_id, 'post_id': post_id, 'count': 100, 'offset': i*100})

		for comment in comments['items']:
			#if comment written last 24 hours/this day
			if(comment['date'] > time.time() - comments_monitoring_seconds):
				#id writer
				from_id = comment['from_id']
				#if writer is exist we increase the counter, otherwise we create writer
				exist = 0
				j = 0
				while (j < len(array_id)):
					if(array_id[j] == from_id):
						exist = 1
						array_count[j] += 1
						break
					j += 1
				if(exist == 0):
					array_id.append(from_id)
					array_count.append(1)

		i += 1

#find maximum of comments
i = 0
while(i < len(array_count)):
	if(array_count[i] > max_comments):
		max_comments = array_count[i]
		max_id = array_id[i]
	i += 1

#output data
print(max_id)
print(max_comments)
