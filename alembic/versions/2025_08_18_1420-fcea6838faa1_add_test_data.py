"""add_test_data.

Revision ID: fcea6838faa1
Revises: 16dd19e2a44a
Create Date: 2025-08-18 14:20:00.000000

"""

from decimal import Decimal
from uuid import uuid4

from alembic import op

# revision identifiers, used by Alembic.
revision = 'fcea6838faa1'
down_revision = '16dd19e2a44a'
branch_labels = None
depends_on = None


def upgrade() -> None:  # noqa: PLR0914
    # Create test data for all tables

    # 1. Add activity types (activities)
    activities_data = [
        # Parent categories
        {
            'id': str(uuid4()),
            'name': 'Торговля',
            'description': 'Розничная и оптовая торговля',
            'parent_id': None,
        },
        {
            'id': str(uuid4()),
            'name': 'Услуги',
            'description': 'Различные виды услуг',
            'parent_id': None,
        },
        {
            'id': str(uuid4()),
            'name': 'Образование',
            'description': 'Образовательные учреждения',
            'parent_id': None,
        },
        {
            'id': str(uuid4()),
            'name': 'Медицина',
            'description': 'Медицинские услуги',
            'parent_id': None,
        },
        {
            'id': str(uuid4()),
            'name': 'Рестораны и кафе',
            'description': 'Общественное питание',
            'parent_id': None,
        },
        {
            'id': str(uuid4()),
            'name': 'Финансы',
            'description': 'Финансовые услуги',
            'parent_id': None,
        },
        {
            'id': str(uuid4()),
            'name': 'Спорт',
            'description': 'Спортивные услуги',
            'parent_id': None,
        },
        {
            'id': str(uuid4()),
            'name': 'Красота',
            'description': 'Услуги красоты',
            'parent_id': None,
        },
    ]

    # Get parent category IDs for creating children
    trade_id = activities_data[0]['id']
    services_id = activities_data[1]['id']
    education_id = activities_data[2]['id']
    medicine_id = activities_data[3]['id']
    restaurants_id = activities_data[4]['id']
    finance_id = activities_data[5]['id']
    sport_id = activities_data[6]['id']
    beauty_id = activities_data[7]['id']

    # Child categories
    child_activities = [
        # Trade
        {
            'id': str(uuid4()),
            'name': 'Продуктовый магазин',
            'description': 'Продажа продуктов питания',
            'parent_id': trade_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Одежда и обувь',
            'description': 'Магазины одежды и обуви',
            'parent_id': trade_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Электроника',
            'description': 'Магазины электроники',
            'parent_id': trade_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Книги',
            'description': 'Книжные магазины',
            'parent_id': trade_id,
        },
        # Services
        {
            'id': str(uuid4()),
            'name': 'Ремонт техники',
            'description': 'Ремонт бытовой техники',
            'parent_id': services_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Химчистка',
            'description': 'Химчистка одежды',
            'parent_id': services_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Фотостудия',
            'description': 'Фотографические услуги',
            'parent_id': services_id,
        },
        # Education
        {
            'id': str(uuid4()),
            'name': 'Языковые курсы',
            'description': 'Изучение иностранных языков',
            'parent_id': education_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Музыкальная школа',
            'description': 'Обучение музыке',
            'parent_id': education_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Программирование',
            'description': 'IT образование',
            'parent_id': education_id,
        },
        # Medicine
        {
            'id': str(uuid4()),
            'name': 'Стоматология',
            'description': 'Стоматологические услуги',
            'parent_id': medicine_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Медицинская клиника',
            'description': 'Общие медицинские услуги',
            'parent_id': medicine_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Аптека',
            'description': 'Продажа лекарств',
            'parent_id': medicine_id,
        },
        # Restaurants
        {
            'id': str(uuid4()),
            'name': 'Ресторан',
            'description': 'Ресторан с полным обслуживанием',  # noqa: RUF001
            'parent_id': restaurants_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Кафе',
            'description': 'Небольшое кафе',
            'parent_id': restaurants_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Пиццерия',
            'description': 'Ресторан пиццы',
            'parent_id': restaurants_id,
        },
        # Finance
        {
            'id': str(uuid4()),
            'name': 'Банк',
            'description': 'Банковские услуги',
            'parent_id': finance_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Страховая компания',
            'description': 'Страховые услуги',
            'parent_id': finance_id,
        },
        # Sport
        {
            'id': str(uuid4()),
            'name': 'Фитнес-клуб',
            'description': 'Спортивный зал',
            'parent_id': sport_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Бассейн',
            'description': 'Плавательный бассейн',
            'parent_id': sport_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Теннисный корт',
            'description': 'Теннисные корты',
            'parent_id': sport_id,
        },
        # Beauty
        {
            'id': str(uuid4()),
            'name': 'Салон красоты',
            'description': 'Услуги красоты',
            'parent_id': beauty_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Парикмахерская',
            'description': 'Стрижки и укладки',
            'parent_id': beauty_id,
        },
        {
            'id': str(uuid4()),
            'name': 'Маникюрный салон',
            'description': 'Маникюр и педикюр',
            'parent_id': beauty_id,
        },
    ]

    activities_data.extend(child_activities)

    # Insert all activity types
    for activity in activities_data:
        parent_id_sql = f"'{activity['parent_id']}'" if activity['parent_id'] else 'NULL'
        op.execute(
            f"INSERT INTO activity (id, name, description, parent_id) VALUES ('{activity['id']}', '{activity['name']}', '{activity['description']}', {parent_id_sql})"
        )

    # 2. Add buildings (buildings) - different locations in Moscow
    buildings_data = [
        # Moscow Center
        {
            'id': str(uuid4()),
            'name': 'ТЦ Европейский',
            'address': 'пл. Киевского Вокзала, 2, Москва',
            'latitude': Decimal('55.7445'),
            'longitude': Decimal('37.5654'),
            'description': 'Крупный торговый центр',
        },
        {
            'id': str(uuid4()),
            'name': 'ТЦ Афимолл',
            'address': 'Пресненская наб., 2, Москва',
            'latitude': Decimal('55.7485'),
            'longitude': Decimal('37.5371'),
            'description': 'Торговый центр в Москва-Сити',
        },
        {
            'id': str(uuid4()),
            'name': 'ТЦ Метрополис',
            'address': 'Ленинградское ш., 39А, Москва',  # noqa: RUF001
            'latitude': Decimal('55.8776'),
            'longitude': Decimal('37.4527'),
            'description': 'Торговый центр на севере Москвы',
        },
        # South Moscow
        {
            'id': str(uuid4()),
            'name': 'ТЦ Южный',
            'address': 'ул. Домодедовская, 20, Москва',
            'latitude': Decimal('55.6123'),
            'longitude': Decimal('37.6012'),
            'description': 'Торговый центр на юге',
        },
        {
            'id': str(uuid4()),
            'name': 'ТЦ Галерея',
            'address': 'Липецкая ул., 26, Москва',
            'latitude': Decimal('55.6345'),
            'longitude': Decimal('37.5891'),
            'description': 'Торговый центр',
        },
        # West Moscow
        {
            'id': str(uuid4()),
            'name': 'ТЦ Вегас',  # noqa: RUF001
            'address': 'МКАД, 24-й км, Москва',
            'latitude': Decimal('55.7234'),
            'longitude': Decimal('37.4123'),
            'description': 'Крупный торговый центр',
        },
        {
            'id': str(uuid4()),
            'name': 'ТЦ Ривьера',
            'address': 'Автозаводская ул., 18, Москва',
            'latitude': Decimal('55.7012'),
            'longitude': Decimal('37.6543'),
            'description': 'Торговый центр',
        },
        # East Moscow
        {
            'id': str(uuid4()),
            'name': 'ТЦ Золотой Вавилон',
            'address': 'ул. Краснобогатырская, 2, Москва',
            'latitude': Decimal('55.7891'),
            'longitude': Decimal('37.7234'),
            'description': 'Торговый центр',
        },
        {
            'id': str(uuid4()),
            'name': 'ТЦ Персей',
            'address': 'ул. Первомайская, 42, Москва',
            'latitude': Decimal('55.8123'),
            'longitude': Decimal('37.7891'),
            'description': 'Торговый центр',
        },
        # North Moscow
        {
            'id': str(uuid4()),
            'name': 'ТЦ Северный',
            'address': 'Дмитровское ш., 89, Москва',
            'latitude': Decimal('55.9234'),
            'longitude': Decimal('37.5123'),
            'description': 'Торговый центр',
        },
        {
            'id': str(uuid4()),
            'name': 'ТЦ Лобня',
            'address': 'ул. Ленина, 15, Лобня',
            'latitude': Decimal('56.0123'),
            'longitude': Decimal('37.4567'),
            'description': 'Торговый центр в Лобне',
        },
        # Business Centers
        {
            'id': str(uuid4()),
            'name': 'БЦ Москва-Сити',
            'address': 'Пресненская наб., 8, Москва',
            'latitude': Decimal('55.7485'),
            'longitude': Decimal('37.5371'),
            'description': 'Бизнес-центр',
        },
        {
            'id': str(uuid4()),
            'name': 'БЦ Лефортово',
            'address': 'ул. Лефортовский Вал, 3, Москва',
            'latitude': Decimal('55.7567'),
            'longitude': Decimal('37.7234'),
            'description': 'Бизнес-центр',
        },
        {
            'id': str(uuid4()),
            'name': 'БЦ Сколково',
            'address': 'ул. Нобеля, 1, Сколково',
            'latitude': Decimal('55.6987'),
            'longitude': Decimal('37.3567'),
            'description': 'Бизнес-центр',
        },
        {
            'id': str(uuid4()),
            'name': 'БЦ Парк Плейс',
            'address': 'ул. Тверская, 3, Москва',
            'latitude': Decimal('55.7567'),
            'longitude': Decimal('37.6178'),
            'description': 'Бизнес-центр',
        },
        {
            'id': str(uuid4()),
            'name': 'БЦ Омега Плаза',
            'address': 'Садовая-Спасская ул., 21, Москва',
            'latitude': Decimal('55.7734'),
            'longitude': Decimal('37.6345'),
            'description': 'Бизнес-центр',
        },
        {
            'id': str(uuid4()),
            'name': 'БЦ Северная Башня',
            'address': 'Ленинградский пр., 80, Москва',
            'latitude': Decimal('55.8234'),
            'longitude': Decimal('37.4567'),
            'description': 'Бизнес-центр',
        },
        {
            'id': str(uuid4()),
            'name': 'БЦ Медицинский',
            'address': 'ул. Покровка, 47, Москва',
            'latitude': Decimal('55.7567'),
            'longitude': Decimal('37.6345'),
            'description': 'Бизнес-центр',
        },
        {
            'id': str(uuid4()),
            'name': 'БЦ Образовательный',
            'address': 'ул. Арбат, 10, Москва',
            'latitude': Decimal('55.7485'),
            'longitude': Decimal('37.5891'),
            'description': 'Бизнес-центр',
        },
        {
            'id': str(uuid4()),
            'name': 'БЦ Спортивный',
            'address': 'Лужнецкая наб., 2, Москва',
            'latitude': Decimal('55.7234'),
            'longitude': Decimal('37.5678'),
            'description': 'Бизнес-центр',
        },
        {
            'id': str(uuid4()),
            'name': 'БЦ Красота',
            'address': 'Кутузовский пр., 30, Москва',
            'latitude': Decimal('55.7456'),
            'longitude': Decimal('37.5234'),
            'description': 'Бизнес-центр',
        },
    ]

    # Insert all buildings
    for building in buildings_data:
        op.execute(
            f"INSERT INTO building (id, name, address, latitude, longitude, description) VALUES ('{building['id']}', '{building['name']}', '{building['address']}', {building['latitude']}, {building['longitude']}, '{building['description']}')"
        )

    # 3. Add organizations (organizations)
    organizations_data = [
        # Grocery stores
        {
            'id': str(uuid4()),
            'name': 'Магнит',
            'building_id': buildings_data[0]['id'],
            'description': 'Сеть продуктовых магазинов',
            'website': 'https://magnit.ru',
            'email': 'info@magnit.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Пятёрочка',
            'building_id': buildings_data[1]['id'],
            'description': 'Сеть продуктовых магазинов',
            'website': 'https://5ka.ru',
            'email': 'info@5ka.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'М.Видео',  # noqa: RUF001
            'building_id': buildings_data[2]['id'],
            'description': 'Магазин электроники',
            'website': 'https://mvideo.ru',
            'email': 'info@mvideo.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Эльдорадо',
            'building_id': buildings_data[3]['id'],
            'description': 'Магазин бытовой техники',
            'website': 'https://eldorado.ru',
            'email': 'info@eldorado.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Спортмастер',
            'building_id': buildings_data[4]['id'],
            'description': 'Магазин спортивных товаров',
            'website': 'https://sportmaster.ru',
            'email': 'info@sportmaster.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Лента',
            'building_id': buildings_data[5]['id'],
            'description': 'Гипермаркет',
            'website': 'https://lenta.com',
            'email': 'info@lenta.com',
        },
        {
            'id': str(uuid4()),
            'name': 'Ашан',
            'building_id': buildings_data[6]['id'],
            'description': 'Гипермаркет',
            'website': 'https://auchan.ru',
            'email': 'info@auchan.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Перекрёсток',
            'building_id': buildings_data[7]['id'],
            'description': 'Продуктовый магазин',
            'website': 'https://perekrestok.ru',
            'email': 'info@perekrestok.ru',
        },
        # Restaurants and Cafes
        {
            'id': str(uuid4()),
            'name': 'Макдональдс',
            'building_id': buildings_data[8]['id'],
            'description': 'Ресторан быстрого питания',
            'website': 'https://mcdonalds.ru',
            'email': 'info@mcdonalds.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'KFC',
            'building_id': buildings_data[9]['id'],
            'description': 'Ресторан быстрого питания',
            'website': 'https://kfc.ru',
            'email': 'info@kfc.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Додо Пицца',
            'building_id': buildings_data[10]['id'],
            'description': 'Пиццерия',
            'website': 'https://dodopizza.ru',
            'email': 'info@dodopizza.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Старбакс',
            'building_id': buildings_data[11]['id'],
            'description': 'Кофейня',
            'website': 'https://starbucks.ru',
            'email': 'info@starbucks.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Шоколадница',
            'building_id': buildings_data[12]['id'],
            'description': 'Кофейня',
            'website': 'https://chocolate.ru',
            'email': 'info@chocolate.ru',
        },
        # Banks
        {
            'id': str(uuid4()),
            'name': 'Сбербанк',
            'building_id': buildings_data[13]['id'],
            'description': 'Банк',
            'website': 'https://sberbank.ru',
            'email': 'info@sberbank.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'ВТБ',
            'building_id': buildings_data[14]['id'],
            'description': 'Банк',
            'website': 'https://vtb.ru',
            'email': 'info@vtb.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Альфа-Банк',
            'building_id': buildings_data[15]['id'],
            'description': 'Банк',
            'website': 'https://alfabank.ru',
            'email': 'info@alfabank.ru',
        },
        # Medical Institutions
        {
            'id': str(uuid4()),
            'name': 'Медицинский центр ЕМС',  # noqa: RUF001
            'building_id': buildings_data[16]['id'],
            'description': 'Медицинская клиника',
            'website': 'https://emcmos.ru',
            'email': 'info@emcmos.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Клиника Семейная',
            'building_id': buildings_data[17]['id'],
            'description': 'Медицинская клиника',
            'website': 'https://semeynaya.ru',
            'email': 'info@semeynaya.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Аптека 36.6',
            'building_id': buildings_data[0]['id'],
            'description': 'Аптека',
            'website': 'https://366.ru',
            'email': 'info@366.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Аптека Ригла',
            'building_id': buildings_data[1]['id'],
            'description': 'Аптека',
            'website': 'https://rigla.ru',
            'email': 'info@rigla.ru',
        },
        # Education
        {
            'id': str(uuid4()),
            'name': 'Языковая школа English First',
            'building_id': buildings_data[2]['id'],
            'description': 'Изучение английского языка',
            'website': 'https://englishfirst.ru',
            'email': 'info@englishfirst.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Школа программирования GeekBrains',
            'building_id': buildings_data[3]['id'],
            'description': 'IT образование',
            'website': 'https://geekbrains.ru',
            'email': 'info@geekbrains.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Музыкальная школа',
            'building_id': buildings_data[4]['id'],
            'description': 'Обучение музыке',
            'website': None,
            'email': 'info@music-school.ru',
        },
        # Sport
        {
            'id': str(uuid4()),
            'name': 'Фитнес-клуб World Class',
            'building_id': buildings_data[5]['id'],
            'description': 'Спортивный зал',
            'website': 'https://worldclass.ru',
            'email': 'info@worldclass.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Фитнес-клуб Фитнес Прайм',
            'building_id': buildings_data[6]['id'],
            'description': 'Спортивный зал',
            'website': 'https://fitnessprime.ru',
            'email': 'info@fitnessprime.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Бассейн Олимпийский',
            'building_id': buildings_data[7]['id'],
            'description': 'Плавательный бассейн',
            'website': 'https://olympic-pool.ru',
            'email': 'info@olympic-pool.ru',
        },
        # Beauty
        {
            'id': str(uuid4()),
            'name': 'Салон красоты Престиж',
            'building_id': buildings_data[8]['id'],
            'description': 'Услуги красоты',
            'website': 'https://prestige-beauty.ru',
            'email': 'info@prestige-beauty.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Парикмахерская Стиль',
            'building_id': buildings_data[9]['id'],
            'description': 'Стрижки и укладки',
            'website': 'https://style-hair.ru',
            'email': 'info@style-hair.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Маникюрный салон Красота',
            'building_id': buildings_data[10]['id'],
            'description': 'Маникюр и педикюр',
            'website': 'https://beauty-nails.ru',
            'email': 'info@beauty-nails.ru',
        },
        # Services
        {
            'id': str(uuid4()),
            'name': 'Химчистка Чистота',
            'building_id': buildings_data[11]['id'],
            'description': 'Химчистка одежды',
            'website': 'https://chistota.ru',
            'email': 'info@chistota.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Ремонт техники Сервис',
            'building_id': buildings_data[12]['id'],
            'description': 'Ремонт бытовой техники',
            'website': 'https://service-repair.ru',
            'email': 'info@service-repair.ru',
        },
        {
            'id': str(uuid4()),
            'name': 'Фотостудия Момент',
            'building_id': buildings_data[13]['id'],
            'description': 'Фотографические услуги',
            'website': 'https://moment-photo.ru',
            'email': 'info@moment-photo.ru',
        },
    ]

    # Insert all organizations
    for org in organizations_data:
        website_sql = f"'{org['website']}'" if org['website'] else 'NULL'
        op.execute(
            f"INSERT INTO organization (id, name, building_id, description, website, email) VALUES ('{org['id']}', '{org['name']}', '{org['building_id']}', '{org['description']}', {website_sql}, '{org['email']}')"
        )

    # 4. Add phones (phones)
    phones_data = [
        {
            'id': str(uuid4()),
            'number': '+7 (495) 123-45-67',
            'organization_id': organizations_data[0]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 123-45-68',
            'organization_id': organizations_data[0]['id'],
            'description': 'Факс',
            'is_primary': False,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 234-56-78',
            'organization_id': organizations_data[1]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 345-67-89',
            'organization_id': organizations_data[2]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 456-78-90',
            'organization_id': organizations_data[3]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 567-89-01',
            'organization_id': organizations_data[4]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 678-90-12',
            'organization_id': organizations_data[5]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 789-01-23',
            'organization_id': organizations_data[6]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 890-12-34',
            'organization_id': organizations_data[7]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 901-23-45',
            'organization_id': organizations_data[8]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 012-34-56',
            'organization_id': organizations_data[9]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 111-22-33',
            'organization_id': organizations_data[10]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 222-33-44',
            'organization_id': organizations_data[11]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 333-44-55',
            'organization_id': organizations_data[12]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 444-55-66',
            'organization_id': organizations_data[13]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 555-66-77',
            'organization_id': organizations_data[14]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 666-77-88',
            'organization_id': organizations_data[15]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 777-88-99',
            'organization_id': organizations_data[16]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 888-99-00',
            'organization_id': organizations_data[17]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 999-00-11',
            'organization_id': organizations_data[18]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 000-11-22',
            'organization_id': organizations_data[19]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 111-11-11',
            'organization_id': organizations_data[20]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 222-22-22',
            'organization_id': organizations_data[21]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 333-33-33',
            'organization_id': organizations_data[22]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 444-44-44',
            'organization_id': organizations_data[23]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 555-55-55',
            'organization_id': organizations_data[24]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 666-66-66',
            'organization_id': organizations_data[25]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 777-77-77',
            'organization_id': organizations_data[26]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 888-88-88',
            'organization_id': organizations_data[27]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 999-99-99',
            'organization_id': organizations_data[28]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 000-00-00',
            'organization_id': organizations_data[29]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 111-00-11',
            'organization_id': organizations_data[30]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
        {
            'id': str(uuid4()),
            'number': '+7 (495) 222-00-22',
            'organization_id': organizations_data[31]['id'],
            'description': 'Основной телефон',
            'is_primary': True,
        },
    ]

    for phone in phones_data:
        description_sql = f"'{phone['description']}'" if phone['description'] else 'NULL'
        op.execute(
            f"INSERT INTO phone (id, number, organization_id, description, is_primary) VALUES ('{phone['id']}', '{phone['number']}', '{phone['organization_id']}', {description_sql}, {phone['is_primary']})"
        )

    # 5. organization_activity
    grocery_id = child_activities[0]['id']
    electronics_id = child_activities[2]['id']
    repair_id = child_activities[4]['id']
    dry_cleaning_id = child_activities[5]['id']
    photo_id = child_activities[6]['id']
    language_id = child_activities[7]['id']
    music_id = child_activities[8]['id']
    programming_id = child_activities[9]['id']
    clinic_id = child_activities[11]['id']
    pharmacy_id = child_activities[12]['id']
    restaurant_id = child_activities[13]['id']
    cafe_id = child_activities[14]['id']
    pizza_id = child_activities[15]['id']
    bank_id = child_activities[16]['id']
    fitness_id = child_activities[18]['id']
    pool_id = child_activities[19]['id']
    beauty_salon_id = child_activities[21]['id']
    hairdresser_id = child_activities[22]['id']
    manicure_id = child_activities[23]['id']

    organization_activity_data = [
        {'organization_id': organizations_data[0]['id'], 'activity_id': grocery_id},
        {'organization_id': organizations_data[1]['id'], 'activity_id': grocery_id},
        {'organization_id': organizations_data[6]['id'], 'activity_id': grocery_id},
        {'organization_id': organizations_data[7]['id'], 'activity_id': grocery_id},
        {'organization_id': organizations_data[2]['id'], 'activity_id': electronics_id},
        {
            'organization_id': organizations_data[3]['id'],
            'activity_id': electronics_id,
        },
        {'organization_id': organizations_data[4]['id'], 'activity_id': fitness_id},
        {
            'organization_id': organizations_data[8]['id'],
            'activity_id': restaurant_id,
        },
        {'organization_id': organizations_data[9]['id'], 'activity_id': restaurant_id},
        {'organization_id': organizations_data[10]['id'], 'activity_id': pizza_id},
        {'organization_id': organizations_data[11]['id'], 'activity_id': cafe_id},
        {'organization_id': organizations_data[12]['id'], 'activity_id': cafe_id},
        {'organization_id': organizations_data[13]['id'], 'activity_id': bank_id},
        {'organization_id': organizations_data[14]['id'], 'activity_id': bank_id},
        {'organization_id': organizations_data[15]['id'], 'activity_id': bank_id},
        {
            'organization_id': organizations_data[16]['id'],
            'activity_id': clinic_id,
        },
        {
            'organization_id': organizations_data[17]['id'],
            'activity_id': clinic_id,
        },
        {
            'organization_id': organizations_data[18]['id'],
            'activity_id': pharmacy_id,
        },
        {
            'organization_id': organizations_data[19]['id'],
            'activity_id': pharmacy_id,
        },
        {
            'organization_id': organizations_data[20]['id'],
            'activity_id': language_id,
        },
        {
            'organization_id': organizations_data[21]['id'],
            'activity_id': programming_id,
        },
        {
            'organization_id': organizations_data[22]['id'],
            'activity_id': music_id,
        },
        {
            'organization_id': organizations_data[23]['id'],
            'activity_id': fitness_id,
        },
        {
            'organization_id': organizations_data[24]['id'],
            'activity_id': fitness_id,
        },
        {
            'organization_id': organizations_data[25]['id'],
            'activity_id': pool_id,
        },
        {
            'organization_id': organizations_data[26]['id'],
            'activity_id': beauty_salon_id,
        },
        {
            'organization_id': organizations_data[27]['id'],
            'activity_id': hairdresser_id,
        },
        {
            'organization_id': organizations_data[28]['id'],
            'activity_id': manicure_id,
        },
        {
            'organization_id': organizations_data[29]['id'],
            'activity_id': dry_cleaning_id,
        },
        {
            'organization_id': organizations_data[30]['id'],
            'activity_id': repair_id,
        },
        {
            'organization_id': organizations_data[31]['id'],
            'activity_id': photo_id,
        },
        {
            'organization_id': organizations_data[0]['id'],
            'activity_id': trade_id,
        },
        {
            'organization_id': organizations_data[2]['id'],
            'activity_id': trade_id,
        },
        {
            'organization_id': organizations_data[8]['id'],
            'activity_id': restaurants_id,
        },
        {
            'organization_id': organizations_data[13]['id'],
            'activity_id': finance_id,
        },
        {
            'organization_id': organizations_data[16]['id'],
            'activity_id': medicine_id,
        },
        {
            'organization_id': organizations_data[20]['id'],
            'activity_id': education_id,
        },
        {
            'organization_id': organizations_data[23]['id'],
            'activity_id': sport_id,
        },
        {
            'organization_id': organizations_data[26]['id'],
            'activity_id': beauty_id,
        },
    ]

    for org_activity in organization_activity_data:
        op.execute(
            f"INSERT INTO organization_activity (organization_id, activity_id) VALUES ('{org_activity['organization_id']}', '{org_activity['activity_id']}')"
        )


def downgrade() -> None:
    op.execute('DELETE FROM organization_activity')
    op.execute('DELETE FROM phone')
    op.execute('DELETE FROM organization')
    op.execute('DELETE FROM building')
    op.execute('DELETE FROM activity')
