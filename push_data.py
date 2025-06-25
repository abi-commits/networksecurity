import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            logging.info("MongoDB client initialized successfully.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convert(self, file_path: str):
        """
        Reads a CSV and converts it to JSON (list of dicts)
        """
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.to_json(orient="records"))
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, collection_name: str, database_name: str):
        """
        Inserts records into the specified MongoDB collection.
        """
        try:
            db = self.mongo_client[database_name]
            collection = db[collection_name]

            result = collection.insert_many(records)
            logging.info(f"Inserted {len(result.inserted_ids)} records into {collection_name}")
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    try:
        FILE_PATH = "network_data/phisingData.csv"
        DATABASE = "abiml"
        COLLECTION = "network_data"

        networkobj = NetworkDataExtract()
        records = networkobj.csv_to_json_convert(file_path=FILE_PATH)
        inserted_count = networkobj.insert_data_mongodb(records=records, collection_name=COLLECTION, database_name=DATABASE)

        logging.info(f"Data ingestion complete. Total records inserted: {inserted_count}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
