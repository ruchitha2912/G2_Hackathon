import requests

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://ruchithavs2912:IXd9dHtkDPlSnvQP@g2-products.jq9o8sv.mongodb.net/?retryWrites=true&w=majority&appName=G2-products"


# Create a new client and connect to the server

client = MongoClient(uri, server_api=ServerApi('1'))


# Send a ping to confirm a successful connection

try:

    client.admin.command('ping')

    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:

    print(e)


db = client["g2_hackathon"]


collection1 = db["g2_listed_products"]

collection1.delete_many({})


g2_api_endpoint = "https://data.g2.com/api/v1/products"

secret_token = "df6b82dbc9c4cb39830e29ed7e335546116c60ffa1d6a4948bb3cb9dc3e6abb8"


def fetch_g2_products():

    headers = {"Authorization": f"Bearer {secret_token}"}

    response = requests.get(g2_api_endpoint, headers=headers)

    if response.status_code == 200:

        return response.json()['data']
    else:

        print("Failed to fetch G2 products.")

        return []


def add_products_to_mongodb(products):
    if products:

        collection1.insert_many(products)

        print("Products added to MongoDB successfully.")
    else:

        print("No products to add.")


collection2 = db["g2_competitors"]  # Create a new collection for competitors


g2_api_endpoint = "https://data.g2.com/api/v1/products"

secret_token = "df6b82dbc9c4cb39830e29ed7e335546116c60ffa1d6a4948bb3cb9dc3e6abb8"


def fetch_g2_competitors(product_id):

    competitor_url = f"{g2_api_endpoint}/{product_id}/competitors"

    headers = {"Authorization": f"Bearer {secret_token}"}

    response = requests.get(competitor_url, headers=headers)

    if response.status_code == 200:

        return response.json()['data']
    else:

        print(f"Failed to fetch competitors for product ID: {product_id}")

        return []


def add_competitors_to_mongodb(product_id, competitors):
    if competitors:
        for competitor in competitors:

            # Add product_id to each competitor document
            competitor['product_id'] = product_id

        collection2.insert_many(competitors)

        print(
            f"Competitors for product ID {product_id} added to MongoDB successfully.")
    else:

        print(f"No competitors found for product ID: {product_id}")


def compare_products():

    collection3 = db["g2_not_listed"]

    collection3.delete_many({})

    pipeline = [

        {

            "$match": {

                # Filter out documents without the "attributes" field
                "attributes": {"$exists": True}

            }

        },

        {

            "$lookup": {

                "from": "collection1",

                "let": {"product_name": "$attributes.product_name"},

                "pipeline": [

                    {

                        "$match": {

                            "$expr": {"$eq": ["$$product_name", "$attributes.product_name"]}

                        }

                    }

                ],

                "as": "matching_products"

            }

        },

        {

            "$match": {

                # Filter out documents without matches in collection1
                "matching_products": {"$eq": []}

            }

        },

        {

            "$project": {

                "_id": 0,  # Exclude _id field if not needed

                "attributes": 1,  # Include other relevant fields as needed

                # Include other fields from collection2 as needed

            }

        },

        {

            "$out": "g2_not_listed"  # Insert filtered documents into a new collection

        }

    ]

    # Execute the aggregation pipeline

    collection2.aggregate(pipeline)


if __name__ == "__main__":

    g2_products = fetch_g2_products()

    add_products_to_mongodb(g2_products)

    for product in g2_products:

        product_id = product.get('id')

        competitors = fetch_g2_competitors(product_id)

        add_competitors_to_mongodb(product_id, competitors)

    compare_products()
