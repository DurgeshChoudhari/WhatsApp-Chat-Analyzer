import re
import pandas as pd

def preprocess(data):
	pattern = '\d+/\d+\/\d+,\s\d+:\d+\s\w+\s-\s'

	messages = re.split(pattern, data)[1:]
	dates = re.findall(pattern, data)

	df = pd.DataFrame({'user_messages':messages, 'date':dates})
	df['date'] = pd.to_datetime(df['date'], format = "%d/%m/%y, %H:%M %p - ")
	# df.head()
	users = []
	messeges = []

	for message in df['user_messages']:
	    entry = re.split('([\w\W]+?):\s', message)
	    if entry[1:]:
	        users.append(entry[1])
	        messeges.append(entry[2])
	    else:
	        users.append('group_notification')
	        messeges.append(entry[0])
	df['user'] = users
	df['messages'] = messeges
	df.drop(columns=['user_messages'], inplace=True)
	# df.head()


	df['year'] = df['date'].dt.year
	df['month'] = df['date'].dt.month_name()
	df['day'] = df['date'].dt.day
	df['hours'] = df['date'].dt.hour
	df['minute'] = df['date'].dt.minute
	# df.head()
	return df
