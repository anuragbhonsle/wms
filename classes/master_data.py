import sql
from db import fetch_all


class MasterData:
    def get_all_sellers(self):
        return fetch_all(sql.GET_SELLERS)

    def get_all_skus(self):
        return fetch_all(sql.GET_SKUS)
