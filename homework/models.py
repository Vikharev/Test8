from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def check_quantity(self, quantity) -> bool:
        """
        Возвращает True, если количество продукта больше или равно запрашиваемому,
        и False в обратном случае
        """
        return quantity <= self.quantity

    def buy(self, quantity):
        """
        Метод покупки
        Проверяет количество продукта, используя метод check_quantity
        Если продуктов не хватает, то вызывает исключение ValueError
        """
        if self.check_quantity(quantity):
            self.quantity -= quantity
        else:
            raise ValueError('Продуктов не хватает')

    def __hash__(self):
        return hash(self.name + self.description)


@dataclass
class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """
    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if not remove_count or remove_count >= self.products[product]:
            del self.products[product]
        else:
            self.products[product] -= remove_count

    def clear(self):
        """
        Метод очистки корзины
        """
        self.products = {}

    def get_total_price(self) -> float:
        """
        Метод получения стоимости товаров в корзине
        """
        total_price = 0
        for element in self.products:
            total_price += element.price * element.quantity
        return total_price

    def buy(self):
        """
        Метод покупки.
        Если товаров не хватает на складе, выбрасывается исключение ValueError
        """
        for element in self.products:
            if not element.check_quantity(self.products[element]):
                raise ValueError(f'Товара {element.name} не хватает на складе')
        for element in self.products:
            element.buy(self.products[element])
