from pymongo import MongoClient


class MongoDBOpen:
    """
    Контекстный менеджер для работы с MongoDB.
    """
    def __init__(self, host: str, db_name: str):
        self.host = host
        self.db_name = db_name

    def __enter__(self):
        self.client = MongoClient(self.host)
        self.db = self.client[self.db_name]
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


def get_doc(host: str, db_name: str, collection_name: str, query: dict) -> dict | None:
    """
    Функция для получения документа из MongoDB.
    host - путь для подключения к базе данных.
    db_name - название базы данных.
    collection_name - название коллекции
    query - запрос к базе данных.

    document - найденный документ.
    """
    with MongoDBOpen(host, db_name) as db:
        collections = db[collection_name]
        document = collections.find_one(query)
        return document
