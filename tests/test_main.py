
import json
import os
import tempfile

from src.main import create_objects_from_json, read_json


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


def test_category_init(category):
    assert category.name == "Смартфоны"
    assert category.description.strip() == ("Смартфоны, как средство не только коммуникации, "
                                            "но и получения дополнительных функций для удобства жизни").strip()
    assert len(category.products) == 3
    assert category.category_count == 1
    assert category.product_count == 3


def test_read_json():
    """Тестирование функции read_json с использованием временного файла."""
    test_data = [
        {
            "name": "Смартфоны",
            "description": "Описание категории смартфонов",
            "products": [
                {
                    "name": "Samsung Galaxy S23 Ultra",
                    "description": "256GB, Серый цвет, 200MP камера",
                    "price": 180000.0,
                    "quantity": 5
                },
                {
                    "name": "Iphone 15",
                    "description": "512GB, Gray space",
                    "price": 210000.0,
                    "quantity": 8
                }
            ]
        }
    ]

    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.json') as temp_file:
        json.dump(test_data, temp_file, ensure_ascii=False, indent=4)
        temp_file_path = temp_file.name
    result = read_json(temp_file_path)
    assert result == test_data
    os.remove(temp_file_path)


def test_create_objects_from_json():
    """Тестирование функции create_objects_from_json."""
    test_data = [
        {
            "name": "Смартфоны",
            "description": "Описание категории смартфонов",
            "products": [
                {
                    "name": "Samsung Galaxy S23 Ultra",
                    "description": "256GB, Серый цвет, 200MP камера",
                    "price": 180000.0,
                    "quantity": 5
                },
                {
                    "name": "Iphone 15",
                    "description": "512GB, Gray space",
                    "price": 210000.0,
                    "quantity": 8
                }
            ]
        }
    ]

    categories = create_objects_from_json(test_data)
    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"
    assert categories[0].description == "Описание категории смартфонов"
    assert len(categories[0].products) == 2
    assert categories[0].products[0].name == "Samsung Galaxy S23 Ultra"
    assert categories[0].products[1].name == "Iphone 15"
