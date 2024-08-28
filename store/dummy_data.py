from faker import Faker
import random
# from .models import Category, Brand, Product, Size, Color, SubProduct, Media
from store.models import *

fake = Faker()

# Generate Faker data for Category model
def create_fake_category():
    title = fake.word()
    type_choice = random.choice(['parent', 'child', 'subchild'])
    keywords = ', '.join(fake.words(5))
    slug = fake.slug()
    image = 'category_images/' + fake.file_name(category='image', extension='jpg')
    is_active = fake.boolean()
    return Category.objects.create(title=title, type=type_choice, keywords=keywords, slug=slug, image=image, is_active=is_active)

# Generate Faker data for Brand model
def create_fake_brand():
    title = fake.company()
    image = 'brand_images/' + fake.file_name(category='image', extension='jpg')
    description = fake.text()
    is_active = fake.boolean()
    return Brand.objects.create(title=title, image=image, description=description, is_active=is_active)

# Generate Faker data for Product model
def create_fake_product(category, brand):
    title = fake.catch_phrase()
    keywords = ', '.join(fake.words(5))
    price = round(random.uniform(10, 1000), 2)
    description = fake.text()
    slug = fake.slug()
    is_featured = fake.boolean()
    is_active = fake.boolean()
    image = 'product_images/' + fake.file_name(category='image', extension='jpg')
    return Product.objects.create(category=category, brand=brand, title=title, keywords=keywords, price=price,
                                  description=description, slug=slug, is_featured=is_featured, is_active=is_active, image=image)

# Generate Faker data for Size model
def create_fake_size():
    title = fake.word()
    code = fake.random_int(min=100, max=999)
    is_active = fake.boolean()
    return Size.objects.create(title=title, code=code, is_active=is_active)

# Generate Faker data for Color model
def create_fake_color():
    title = fake.color_name()
    code = fake.hex_color()
    is_active = fake.boolean()
    return Color.objects.create(title=title, code=code, is_active=is_active)

# Generate Faker data for SubProduct model
def create_fake_subproduct(product, color, size):
    sku = fake.uuid4()
    stock_price = round(random.uniform(10, 500), 2)
    retail_price = round(stock_price * 1.5, 2)
    sale_price = round(stock_price * 0.8, 2)
    stock_qty = fake.random_int(min=0, max=100)
    is_active = fake.boolean()
    return SubProduct.objects.create(product=product, color=color, size=size, sku=sku, stock_price=stock_price,
                                      retail_price=retail_price, sale_price=sale_price, stock_qty=stock_qty, is_active=is_active)

# Generate Faker data for Media model
def create_fake_media(subproduct):
    image = 'product_images/' + fake.file_name(category='image', extension='jpg')
    is_active = fake.boolean()
    return Media.objects.create(image=image, subproduct=subproduct, is_active=is_active)

# Generate Faker data using the functions above
fake_category = create_fake_category()
fake_brand = create_fake_brand()
fake_product = create_fake_product(fake_category, fake_brand)
fake_size = create_fake_size()
fake_color = create_fake_color()
fake_subproduct = create_fake_subproduct(fake_product, fake_color, fake_size)
fake_media = create_fake_media(fake_subproduct)
