"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart

TEST_PRODUCTS = [{"name": "book",
                  "price": 100,
                  "description": "This is a book",
                  "quantity": 1000},
                 {"name": "pencil",
                  "price": 9.99,
                  "description": "This is a pencil",
                  "quantity": 10},
                 ]


@pytest.fixture
def product_1():
    return Product(TEST_PRODUCTS[0]["name"],
                   TEST_PRODUCTS[0]["price"],
                   TEST_PRODUCTS[0]["description"],
                   TEST_PRODUCTS[0]["quantity"])


@pytest.fixture
def product_2():
    return Product(TEST_PRODUCTS[1]["name"],
                   TEST_PRODUCTS[1]["price"],
                   TEST_PRODUCTS[1]["description"],
                   TEST_PRODUCTS[1]["quantity"])


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Класс группирует тесты на класс Product
    """

    def test_product_check_quantity_equal(self, product_1):
        assert product_1.check_quantity(TEST_PRODUCTS[0]["quantity"]) is True

    def test_product_check_quantity_less(self, product_1):
        assert product_1.check_quantity(TEST_PRODUCTS[0]["quantity"] - 1) is True

    def test_product_check_quantity_more(self, product_1):
        assert product_1.check_quantity(TEST_PRODUCTS[0]["quantity"] + 1) is False

    def test_product_buy_one(self, product_1):
        product_1.buy(1)
        assert product_1.quantity == TEST_PRODUCTS[0]["quantity"] - 1

    def test_product_buy_more_than_available(self, product_1):
        with pytest.raises(ValueError):
            product_1.buy(product_1.quantity + 1)


class TestCart:
    """
    Методы класса Cart
    """

    def test_add_first_product(self, cart, product_1):
        cart.add_product(product_1, buy_count=1)
        assert cart.products[product_1] == 1

    def test_add_second_product(self, cart, product_1, product_2):
        cart.add_product(product_1, buy_count=1)
        cart.add_product(product_2, buy_count=5)
        assert cart.products[product_2] == 5

    def test_remove_product(self, cart, product_2):
        cart.add_product(product_2, buy_count=5)
        cart.remove_product(product_2, remove_count=2)
        assert cart.products[product_2] == 3

    def test_remove_product_all(self, cart, product_2):
        cart.add_product(product_2, buy_count=5)
        cart.remove_product(product_2, remove_count=5)
        assert cart.products == {}

    def test_remove_product_more_then(self, cart, product_2):
        cart.add_product(product_2, buy_count=5)
        cart.remove_product(product_2, remove_count=6)
        assert cart.products == {}

    def test_clear_cart(self, cart, product_1, product_2):
        cart.add_product(product_1, buy_count=2)
        cart.add_product(product_2, buy_count=3)
        cart.clear()
        assert cart.products == {}

    def test_total_price(self, cart, product_1, product_2):
        cart.add_product(product_1, buy_count=2)
        cart.add_product(product_2, buy_count=3)
        assert cart.get_total_price() == ((product_1.price * product_1.quantity)
                                          + (product_2.price * product_2.quantity))

    def test_buy(self, cart, product_1):
        quantity_before = product_1.quantity
        cart.add_product(product_1, buy_count=5)
        cart.buy()
        assert product_1.quantity == quantity_before - 5

    def test_buy_error(self, cart, product_1, product_2):
        quantity_1_before = product_1.quantity
        quantity_2_before = product_2.quantity
        cart.add_product(product_1, buy_count=5)
        cart.add_product(product_2, buy_count=TEST_PRODUCTS[1]["quantity"] + 1)
        with pytest.raises(ValueError, match="Продуктов не хватает"):
            cart.buy()
        assert product_1.quantity == quantity_1_before - 5
        assert product_2.quantity == quantity_2_before
