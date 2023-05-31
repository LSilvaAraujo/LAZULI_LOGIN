import stripe
from db.QueryManager import QueryManager
from config import STRIPE_KEY


class StripeManager:
    def __init__(self):
        stripe.api_key = STRIPE_KEY
        self.data = self.get_products()
        self.store_products()

    @staticmethod
    def get_products():
        data = []
        products = stripe.Product.list(active=True)
        for product in products:
            data.append({"id_produto": product.id,
                         "estoque": product.metadata["estoque"],
                         "nome": product.name, "descricao": product.description
                         })
        return data

    def store_products(self):
        query_manager = QueryManager()
        for product in self.data:
            query_manager.register_product(product)
