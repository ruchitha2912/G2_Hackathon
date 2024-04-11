# G2 Products Monitoring System


**Overview:**

The G2 Products Monitoring System is a Python application that periodically identifies new General Availability (GA) products and compares them with products listed on G2, a software review platform. The system stores product details in a MongoDB database and creates a separate collection for products not listed on G2.

 1.**Postman for API Visualization:** We used Postman to visualize and understand the JSON response from the API call. It provides a user-friendly interface to interact with APIs and inspect the data returned.

2. **Web Scraping with Beautiful Soup and Requests:** We have scraped the products URL using Beautiful Soup and Requests which allows you to gather product data efficiently. By scraping the competitors' URLs as well,we were able to retrieve additional products that might not be listed directly on the website, broadening the dataset.

3. **MongoDB Atlas for Cloud Database:** We stored all the fetched data, including both the scraped and API-retrieved information, in MongoDB Atlas which ensures that the data is securely stored and easily accessible from anywhere.

4. **Data Processing with Python DataFrames:** We used python dataframes to organize and manipulate the scraped data. We created separate dataframes for "listed" and "not_listed" products that helps in categorizing and managing the products efficiently.

5. **Streamlit Interface:** We built a streamlit interface to display the dataframes which provides a user-friendly way to interact with the data (the dataframes can be downloaded as well). It allows the users to filter products based on "avreage_rating" of the products listed,enabling users to find relevant products more easily..

6. **Automation with Cron Jobs:** We used Cron to automate the scraping process by running the script on a weekly basis to update the cloud database.

   

**Configuration:**
1. MongoDB URI: Set the MongoDB connection URI in main.py. (we have used our deployment, which can still be accessed)
2. G2 API Token: Set the G2 API token in main.py.


**Installations:**

1. Install streamlit library -> pip install streamlit
2. Install pymongo -> pip install pymongo 

**Run the script:**
1. To update the database run the automate.py -> python automate.py (database is already updated - last_update: 11-04-2024)
2. To view the data: run the streamlit app using the command -> python -m streamlit run interface.py
