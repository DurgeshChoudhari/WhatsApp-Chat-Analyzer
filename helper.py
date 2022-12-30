import pandas as pd
from urlextract import URLExtract
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
	f = open('stop_hinglish.txt', 'r')
	stop_words = f.read()
	f.close()
	if selected_user!='Overall':
		df = df[df['user']==selected_user]
	num_msgs = df.shape[0]
	words = []
	media = 0
	extractor = URLExtract()
	urls = []
	most_common_words = []
	n_df = df[df['messages']!='<Media omitted>\n']
	for m in df['messages']:
		words.extend(m.split())
		urls.extend(extractor.find_urls(m))
		if m=='<Media omitted>\n':
			media+=1
	wrds = []
	for m in n_df['messages']:
		wrds.extend(m.split())

	for w in wrds:
		if w not in stop_words:
			most_common_words.append(w)

	most_common_word = pd.DataFrame(Counter(most_common_words).most_common(30))
	return num_msgs, len(words), media, len(urls), most_common_word

def most_busiest_person(df):
	x = df['user'].value_counts()
	new_df = round((x/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name', 'user':'Percent'})
	
	return x,new_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for msg in df['messages']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df, len(emojis)


def timeline_helper(selected_user,df):
	if selected_user != 'Overall':
		df = df[df['user'] == selected_user]
	df['month_num'] = df['date'].dt.month
	monthly_timeline = df.groupby(['year', 'month_num','month']).count()['messages'].reset_index()
	time = []
	for i in range(monthly_timeline.shape[0]):
		time.append(monthly_timeline['month'][i] + '-' + str(monthly_timeline['year'][i]))
	monthly_timeline['time'] = time

	df['dt'] = df['date'].dt.date
	daily_timeline = df.groupby('dt').count()['messages'].reset_index()
	df['day_name'] = df['date'].dt.day_name()
	df = df['day_name'].value_counts().reset_index()
	return monthly_timeline, daily_timeline, df

