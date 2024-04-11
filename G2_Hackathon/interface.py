import pymongo
import requests
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import matplotlib.pyplot as plt
import streamlit as st

# connect to mongodb atlas database that has all the details
uri = "mongodb+srv://ruchithavs2912:IXd9dHtkDPlSnvQP@g2-products.jq9o8sv.mongodb.net/?retryWrites=true&w=majority&appName=G2-products"
client = MongoClient(uri,server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment.You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#Creating dataframe for all the products that are listed on G2
database_name1 = "g2_hackathon"
collection_name1= "g2_listed_products"
db = client[database_name1]
collection = db[collection_name1]
cursor = collection.find({})
product_data = [(doc['attributes']['name'], doc['attributes']['description'],doc['attributes']['avg_rating'],doc['attributes']['product_url']) for doc in cursor]
listed_df = pd.DataFrame(product_data, columns=['Product Name', 'Description','Average Rating','Product URL'])

#Creating dataframe for all the products that are not listed on G2
database_name2 = "g2_hackathon"
collection_name2 = "g2_not_listed"
db = client[database_name2]
collection = db[collection_name2]
cursor = collection.find({})
product_data = [(doc['attributes']['name'], doc['attributes']['description'],doc['attributes']['avg_rating'],doc['attributes']['product_url']) for doc in cursor]
not_listed_df = pd.DataFrame(product_data, columns=['Product Name', 'Description','Average Rating','Product URL'])

# Round off rating to 2 decimal places
listed_df['Average Rating'] = listed_df['Average Rating'].astype(float).round(2)
not_listed_df['Average Rating'] = not_listed_df['Average Rating'].astype(float).round(2)

#Printing the number of products
num_listed = len(listed_df)
num_not_listed = len(not_listed_df)
print("Number of Products listed on G2:",num_listed)
print("Number of Products not listed on G2",num_not_listed)

def display_dataframe(df):
    st.write(df)


def filter_dataframe(df, min_avg_rating):
    filtered_df = df[df['Average Rating'] >= min_avg_rating]
    return filtered_df

def download_csv_button(df, button_label, file_name):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=button_label,
        data=csv,
        file_name=file_name,
        mime='text/csv'
    )

def main():
   
    # Sidebar
    page = st.sidebar.selectbox("G2 Hackathon", ["Home","Listed Products", "Not Listed Products"])

    if page == "Home":
        st.header("G2 Hackathon - Team: Data Pirates")
        st.subheader("Problem Statement 1:")
        st.write("Creating a system that proactively finds new generally available (GA) products and makes\
        sure they are listed on G2, the biggest software marketplace in the world, is the goal of this\
        project. The system aims to increase product visibility for vendors and help software buyers\
        make informed decisions by automating the processes of fetching new product data,\
        generating reports, and utilising API integration to check availability on G2.")

        st.subheader("Technology Stack:")
        st.markdown("""
        - Programming Language: Python
        - Web Scraping: Beautiful Soup
        - API Integration: Requests library
        - Tool: Postman (used for visualizing the returned json response)
        - Database: MongoDB Atlas (Cloud Database)
        - Interface: Streamlit
        - Cron: Automation (Weekly database update)
        """)

    

    elif page == "Listed Products":
        st.header("Listed Products")
        min_avg_rating_listed = st.slider("Minimum Average Rating", min_value=0.0, max_value=10.0, step=0.1, value=0.0)
        filtered_listed_df = filter_dataframe(listed_df, min_avg_rating_listed)
        st.write("Number of products:",len(filtered_listed_df))
        st.subheader("Filtered based on Average Rating")
        display_dataframe(filtered_listed_df)
        download_csv_button(filtered_listed_df, "Download Listed Products CSV", "listed_products.csv")

    elif page == "Not Listed Products":
        st.header("Not Listed Products")
        min_avg_rating_not_listed = st.slider("Minimum Average Rating", min_value=0.0, max_value=10.0, step=0.1, value=0.0)
        filtered_not_listed_df = filter_dataframe(not_listed_df, min_avg_rating_not_listed)
        st.write("Number of products:",len(filtered_not_listed_df))
        st.subheader("Filtered based on Average Rating")
        display_dataframe(filtered_not_listed_df)
        download_csv_button(filtered_not_listed_df, "Download Not Listed Products CSV", "not_listed_products.csv")


if __name__ == "__main__":
    main()
