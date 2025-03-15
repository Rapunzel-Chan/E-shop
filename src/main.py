import json
import os


class Product:
    """Класс для формирования списка продуктов"""
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict):
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    @property
    def price(self):
        """Геттер для получения цены продукта."""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Сеттер для установки новой цены продукта"""
        if new_price <= 0.0:
            print('Цена не должна быть нулевая или отрицательная')
            return
        if new_price < self.__price:
            user_input = input('Вы точно хотите понизить стоимость? y/n: ').lower()
            if user_input == "y":
                self.__price = new_price
                print(f'Цена успешно изменена на {self.__price} руб.')
            else:
                print('Изменение цены отменено.')
        else:
            self.__price = new_price
            print(f'Цена успешно изменена на {self.__price} руб.')
    def __str__(self):
        return f'{self.name}, {self.__price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
        total = self.__price * self.quantity + other.price * other.quantity
        return total

class Category:
    """Класс для подсчета количества товаров и категорий указанных продуктов"""
    name: str
    description: str
    products: list
    product_count = 0
    category_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products if products else []
        self.product_count = len(self.__products)
        Category.product_count += self.product_count
        Category.category_count += 1


    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f'{self.name}, количество продуктов: {total_quantity} шт.'

    def __iter__(self):
        return ProductIterator(self)

    def add_product(self, product):
        """Cпециальный метод добавления товара"""
        if isinstance(product, Product):
            for existing_product in self.__products:
                if existing_product.name == product.name:
                    existing_product.quantity += product.quantity
                    if product.price > existing_product.price:
                        existing_product.price = product.price
                    return
            self.__products.append(product)
            Category.product_count += 1
            self.product_count += 1
        else:
            raise ValueError("Only Product instances can be added.")

    @property
    def products(self):
        """Геттер для получения списка продуктов в формате строки."""
        products = ''
        for product in self.__products:
            products += f"{str(product)}\n"
        return products


def read_json(path: str) -> dict:
    """Функция по считыванию данных из json-файла"""
    full_path = os.path.abspath(path)
    with open(full_path, 'r', encoding="UTF-8") as file:
        data = json.load(file)
    return data


def create_objects_from_json(data: dict) -> list:
    categories = []
    for category_data in data:
        products = []
        for product_data in category_data['products']:
            products.append(Product.new_product(product_data))
        categories.append(Category(name=category_data['name'],
                                   description=category_data['description'],
                                   products=products))
    return categories

class ProductIterator:
    """Класс для перебора продуктов"""
    def __init__(self, category):
        self.category = category
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.category.products):
            product = self.category.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration

if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(category1.products)
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.products)
    print(category1.product_count)

    existing_products = category1.products
    print(existing_products)

    new_product = Product.new_product(
        {"name": "Samsung Galaxy S23 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 180000.0,
         "quantity": 5})
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)

    raw_data = read_json("../data/products.json")
    categories_data = create_objects_from_json(raw_data)
    print(categories_data[0].name)
    print(categories_data[1].name)

    print(str(product1))
    print(str(product2))
    print(str(product3))
    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)

    for product in categories_data:
        print(product)
