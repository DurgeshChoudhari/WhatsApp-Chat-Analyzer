import streamlit as st
import pandas as pd
import preprocessor, helper
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title='WhatsApp Chat Analyzer', page_icon="📊", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.sidebar.title("WhatsApp Chat Analyzer")
st.title('Welcome to WhatsApp Chat Analyzer')
# st.write('Please select the Individual/Group chat text file')
# st.image('what.jfif', width=750)

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    data = uploaded_file.getvalue().decode("utf-8")
    # st.write(bytes_data)

    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    user_list = df.user.unique().tolist()
    try:
    	user_list.remove('group_notification')
    except:
    	pass
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    num_msgs, words, media, urls, most_common_word = helper.fetch_stats(selected_user, df)
    em_df, emojis = helper.emoji_helper(selected_user, df)
    monthly_timeline, daily_timeline, day_timeline = helper.timeline_helper(selected_user,df)

    	
    if st.sidebar.button("Show analysis"):
    	st.header('Total')
    	col1, col2, col3, col4, col5 = st.columns(5)
    	with col1:
    		st.subheader("Messages")
    		st.title(num_msgs)

    	with col2:
    		st.subheader("Words")
    		st.title(words)
    	with col3:
    		st.subheader("Media")
    		st.title(media)
    	with col4:
    		st.subheader("Link Shared")
    		st.title(urls)
    	with col5:
    		st.subheader("Emojis")
    		st.title(emojis)


    	st.title('Timeline')
    	col1, col2 = st.columns(2)
    	with col1:
    		st.subheader('Monthly Timeline')
    		fig4, ax4 = plt.subplots()
	    	ax4.plot(monthly_timeline['time'], monthly_timeline['messages'], color='black')
	    	plt.xticks(rotation='vertical')
	    	st.pyplot(fig4)

    	with col2:
	    	st.subheader('Daily Timeline')
	    	fig5, ax5 = plt.subplots()
	    	ax5.plot(daily_timeline['dt'], daily_timeline['messages'], color='blue')
	    	plt.xticks(rotation='vertical')
	    	st.pyplot(fig5)
    	col1, col2 = st.columns(2)
    	with col1:
    		st.subheader('Days Wise')
    		fig6, ax6 = plt.subplots()
	    	ax6.bar(day_timeline['index'], day_timeline['day_name'], color='orange')
	    	plt.xticks(rotation='vertical')
	    	st.pyplot(fig6)

    	with col2:
    		st.subheader('Month Wise')
	    	fig7, ax7 = plt.subplots()
	    	ax7.bar(monthly_timeline['month'], monthly_timeline['messages'], color='red')
	    	plt.xticks(rotation='vertical')
	    	st.pyplot(fig7)

    	st.title('Most Busiest')
    	x,new_df = helper.most_busiest_person(df)
    	fig, ax = plt.subplots()
    	col1, col2 = st.columns(2)
    	with col1:
    		st.subheader('Most Busiest Member')
    		ax.bar(x.index, x.values,color='purple')
    		plt.xticks(rotation='vertical')
    		st.pyplot(fig)
    	# with col2:
    	# 	st.dataframe(new_df)
    	with col2:
    		st.subheader('Most Common Words')
    		fig1, ax1 = plt.subplots()
    		ax1.barh(most_common_word[0], most_common_word[1])
    		plt.xticks(rotation='vertical')
    		st.pyplot(fig1)


    	fig3, ax3 = plt.subplots()
    	st.header('emojis')
    	col1, col3 = st.columns(2)
    	with col1:
    		st.subheader('All emojis')
    		st.dataframe(em_df)
    	with col3:
    		# fig1, ax1 = plt.subplots()
    		st.subheader('Top 10 Emojis')
    		ax3.pie(em_df[1].head(10), labels = em_df[0].head(10), autopct="%0.2f")
    		plt.xticks(rotation='vertical')
    		st.pyplot(fig3)
    # st.success('Click on show Analysis for analysis')
    st.subheader('Search by Date')
    date_list = df['dt'].unique().tolist()
    selected_date = st.selectbox("Select date", date_list)
    d_df = df[df['dt']==selected_date]
    st.dataframe(d_df.set_index('date')[[ 'user', 'messages']])
