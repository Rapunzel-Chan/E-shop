import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.main import Category, Product, ProductIterator, create_objects_from_json, read_json, Smartphone, LawnGrass


def test_product_init(products):
    product1, product2, product3 = products
    assert product1.name == "Samsung Galaxy S23 Ultra"
    assert product1.description == "256GB, Серый цвет, 200MP камера"
    assert product1.price == 180000.0
    assert product1.quantity == 5

    assert product2.name == "Iphone 15"
    assert product2.description == "512GB, Gray space"
    assert product2.price == 210000.0
    assert product2.quantity == 8

    assert product3.name == "Xiaomi Redmi Note 11"
    assert product3.description == "1024GB, Синий"
    assert product3.price == 31000.0
    assert product3.quantity == 14


def test_new_product():
    product_data = {
        'name': 'Samsung Galaxy S23 Ultra',
        'description': '256GB, Серый цвет, 200MP камера',
        'price': 180000.0,
        'quantity': 5
    }
    product = Product.new_product(product_data)
    assert product.name == 'Samsung Galaxy S23 Ultra'
    assert product.description == '256GB, Серый цвет, 200MP камера'
    assert product.price == 180000.0
    assert product.quantity == 5


def test_get_price(product):
    assert product.price == 100.0


def test_set_price_increase(product):
    product.price = 150.0
    assert product.price == 150.0


def test_set_price_decrease_confirm(product):
    with patch('builtins.input', return_value='y'):
        product.price = 50.0
        assert product.price == 50.0


def test_set_price_decrease_cancel(product):
    with patch('builtins.input', return_value='n'):
        product.price = 50.0
        assert product.price == 100.0


def test_set_price_negative_value(product):
    product.price = -20.0
    assert product.price == 100.0


def test_set_price_zero_value(product):
    product.price = 0.0
    assert product.price == 100.0


def test_category_init(category):
    assert category.name == "Смартфоны"
    assert category.description.strip() == (
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни").strip()
    assert category.product_count == 3
    assert Category.category_count == 1


def test_add_product():
    product1 = Product("Samsung Galaxy S23", "Top-end smartphone", 100000.0, 10)
    product2 = Product("Iphone 14", "Latest iPhone model", 120000.0, 5)
    category = Category("Smartphones", "Latest smartphones", [product1, product2])
    assert category.product_count == 2, "Category should initially have 2 products."
    new_product = Product("Xiaomi Mi 12", "New Xiaomi smartphone", 70000.0, 15)
    category.add_product(new_product)
    assert new_product in category._Category__products, "New product should be in the category products."
    assert category.product_count == 3, "Category should have 3 products after adding a new product."
    assert category.products.count(new_product.name) == 1, "New product should be listed once in category products."


def test_products_string_format(category):
    expected_output = (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
        "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"
    )
    assert category.products == expected_output


def test_read_json():
    mock_data = {'categories': [{'name': 'Смартфоны', 'description': 'Описание категории смартфонов', 'products': []}]}
    mock_file = mock_open(read_data=json.dumps(mock_data))
    with patch('builtins.open', mock_file):
        result = read_json('fake_path.json')
    assert result == mock_data
    mock_file.assert_called_once_with(os.path.abspath('fake_path.json'), 'r', encoding='UTF-8')


def test_create_objects_from_json():
    mock_data = [
        {
            'name': 'Смартфоны',
            'description': 'Описание категории смартфонов',
            'products': [
                {'name': 'iPhone 13', 'description': 'Смартфон от Apple', 'price': 79900, 'quantity': 10},
                {'name': 'Samsung Galaxy S21', 'description': 'Смартфон от Samsung', 'price': 69900, 'quantity': 5}
            ]
        },
        {
            'name': 'Ноутбуки',
            'description': 'Описание категории ноутбуков',
            'products': [
                {'name': 'MacBook Pro', 'description': 'Ноутбук от Apple', 'price': 129900, 'quantity': 3}
            ]
        }
    ]

    categories = create_objects_from_json(mock_data)
    assert len(categories) == 2
    assert categories[0].name == 'Смартфоны'
    assert categories[0].description == 'Описание категории смартфонов'
    assert len(categories[0]._Category__products) == 2


def test_product_str_method(product):
    assert str(product) == "Test Product, 100.0 руб. Остаток: 10 шт."


def test_product_add_method():
    product_a = Product("Товар A", "Описание A", 100, 10)
    product_b = Product("Товар B", "Описание B", 200, 2)

    expected_total = (product_a.price * product_a.quantity) + (product_b.price * product_b.quantity)
    total_value = product_a + product_b
    assert total_value == expected_total


def test_category_str_method(category):
    assert str(category) == "Смартфоны, количество продуктов: 27 шт."


def test_product_iterator():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    iterator = ProductIterator(category1)
    products = [str(product) for product in iterator]

    assert len(products) == 3
    assert products[0] == str(product1)
    assert products[1] == str(product2)
    assert products[2] == str(product3)


def test_smartphone_init(product_smartphone1):
    assert product_smartphone1.name == "Samsung Galaxy S23 Ultra"
    assert product_smartphone1.description == "256GB, Серый цвет, 200MP камера"
    assert product_smartphone1.price == 180000.0
    assert product_smartphone1.quantity == 5
    assert product_smartphone1.efficiency == 95.5
    assert product_smartphone1.model == "S23 Ultra"
    assert product_smartphone1.memory == 256
    assert product_smartphone1.color == "Серый"


def test_smartphone_add(product_smartphone1, product_smartphone2):
    assert product_smartphone1 + product_smartphone2 == 2580000


def test_smartphone_add_error(product_smartphone1, product_smartphone2):
    with pytest.raises(TypeError):
        product_smartphone1 + 1


def test_lawngrass_init(product_lawngrass1):
    assert product_lawngrass1.name == "Газонная трава"
    assert product_lawngrass1.description == "Элитная трава для газона"
    assert product_lawngrass1.price == 500.0
    assert product_lawngrass1.quantity == 20
    assert product_lawngrass1.country == "Россия"
    assert product_lawngrass1.germination_period == "7 дней"
    assert product_lawngrass1.color == "Зеленый"


def test_lawngrass_add(product_lawngrass1, product_lawngrass2):
    assert product_lawngrass1 + product_lawngrass2 == 16750


def test_lawngrass_add_error(product_lawngrass1, product_lawngrass2):
    with pytest.raises(TypeError):
        product_lawngrass2 + 1

def test_print_mixin(capsys):
    Product(name='Test Product', description='Test Description', price=100.0, quantity=10)
    message = capsys.readouterr()
    assert message.out.strip() == "Product(Test Product, Test Description, 100.0, 10)"

    Smartphone("Iphone 15", "512GB, Gray space", 210000.0,
               8, 98.2, "15", 512, "Gray space")
    message = capsys.readouterr()
    assert message.out.strip() == "Smartphone(Iphone 15, 512GB, Gray space, 210000.0, 8)"

    LawnGrass("Газонная трава 3", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")
    message = capsys.readouterr()
    assert message.out.strip() == "LawnGrass(Газонная трава 3, Выносливая трава, 450.0, 15)"
