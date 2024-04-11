# G2 Products Monitoring System

**Overview**

The G2 Products Monitoring System is a Python application that periodically identifies new General Availability (GA) products and compares them with products listed on G2, a software review platform. The system stores product details in a MongoDB database and creates a separate collection for products not listed on G2.

We have used MonogDB atlas for storing the product details. The system first fetches the products stored in G2 using the provided G2 API. Then scrapes the various websites for identifying new GA products. Newly identified products are then compared with the G2 products and the products that are not listed in G2 are stored in the database. 

**Configuration**

MongoDB URI: Set the MongoDB connection URI in main.py.
G2 API Token: Set the G2 API token in main.py.

**Usage: **

Run the main script using the command - python main.py
