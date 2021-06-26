import streamlit as st
import pandas as pd
from collections import defaultdict
import json

import warnings # supress warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

#------title for App-----
st.title('Book Recommendation App')

#---load dataset
data = pd.read_csv('book_final_data.csv')
top_n = json.load(open(r"top_n.jsn","r"))

#create sidebar
st.sidebar.title("PLEASE SELECT YOUR USER PROFILE")

#---fetch all unique user id from dataset and put it on selectbox-----
u_data = data['user_id']
u_data = u_data.drop_duplicates()
u_array = u_data.to_list()
u_list = [str(element) for element in u_array]
user_id = st.sidebar.selectbox("User Id",u_list)
uid = int(user_id)
#-----Select User Id using dropdown button-----

# User reading history
def get_history(userid):

        ratings = data.loc[data['user_id'] == userid]
        ratings = ratings[['book_title', 'rating']]
        ratings.rename(columns={'book_title': 'Book_title', 'rating': 'Rating'}, inplace=True)
        if ratings.empty:
            print('Sorry your recommendation bucket is empty as you did not rate any books yet')
        else:
            df_reset=ratings.set_index('Book_title')
            df_reset1=df_reset.sort_values(by='Rating', ascending=False)
            return(df_reset1)
        

# Recommender 
def get_reco_list(userid):
        reading_list = defaultdict(list)
      
        for n in top_n[str(userid)]:
            book, rating = n
            title = data.loc[data.isbn==book].book_title.unique()[0]
            reading_list[title] = rating
            
        example_reading_list = reading_list.items()
        df = pd.DataFrame([(k,v) for k, v in example_reading_list], columns = ["Book_name","Rating"])
        df_set=df.set_index('Book_name')
        df_set1=df_set.sort_values(by='Rating', ascending=False).head(5)
        
        return(df_set1)
    
    
if st.button('SHOW ME MY READING HISTORY!'):
    result = get_history (uid)
    st.write('MY READING HISTORY:', result)
                                 
if st.button ("RECOMMEND ME 5 NEW BOOKS!"):
    result2 = get_reco_list (uid)
    st.write('HERE WE GO, YOUR RECOMMENDATIONS:', result2)
