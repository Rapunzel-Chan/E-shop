import pytest

from src.main import Category, LawnGrass, Product, Smartphone


@pytest.fixture
def products():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    return [product1, product2, product3]


@pytest.fixture
def category(products):
    return Category(
        name="Смартфоны",
        description="Смартфоны, как средство не только коммуникации, "
                    "но и получения дополнительных функций для удобства жизни",
        products=products
    )


@pytest.fixture
def test_data():
    return [
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


@pytest.fixture
def product():
    return Product(name='Test Product', description='Test Description', price=100.0, quantity=10)


@pytest.fixture
def product_smartphone1():
    return Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0,
                      5, 95.5,
                      "S23 Ultra", 256, "Серый")


@pytest.fixture
def product_smartphone2():
    return Smartphone("Iphone 15", "512GB, Gray space", 210000.0,
                      8, 98.2,
                      "15", 512, "Gray space")


@pytest.fixture
def product_lawngrass1():
    return LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")


@pytest.fixture
def product_lawngrass2():
    return LawnGrass("Газонная трава 3", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")


@pytest.fixture
def products2():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5),
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 0)
    return [product1, product3]


@pytest.fixture
def category_without_products():
    return Category(
            name="Смартфоны",
            description="Смартфоны, как средство не только коммуникации, "
                        "но и получения дополнительных функций для удобства жизни", products=[])
