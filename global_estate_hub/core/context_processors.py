import os

from django.middleware.csrf import get_token
from properties.models import Property, Category, City
from django.db.models import Count


def generate_token(request) -> dict:
    """
    Generating CSRF middleware tokens for all forms in the project.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        'csrf_token': get_token(request=request)
    }


def properties_types(request) -> dict:
    """
    Returns all available property categories along with information such as category name,
    image source, URL address, and the number of properties in each category.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        'get_category_properties_info': list(
            zip(
                [category.name for category in Category.objects.all().order_by('-name')],
                [category.image.url for category in Category.objects.all().order_by('-name')],
                [category.get_absolute_url() for category in Category.objects.all().order_by('-name')],
                [Property.objects.filter(category=category).count() for category in
                 Category.objects.all().order_by('-name')]
            )
        ),
    }


def explore_cities(request) -> dict:
    """
    Returns all available property cities along with information such as city name,
    image source, URL address, and the number of properties in each city.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        'get_cities_info': list(
            zip(
                [city.name for city in City.objects.all().order_by('-name')],
                [city.image.url for city in City.objects.all().order_by('-name')],
                [city.get_absolute_url() for city in City.objects.all().order_by('-name')],
                [Property.objects.filter(city=city).count() for city in
                 City.objects.all().order_by('-name')]
            )
        ),
    }


def discover_cities(request) -> dict:
    """
    Returns the most frequently occurring cities in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    first_names = ['Emily', 'Alexander', 'Sophia', 'Diego', 'Mia', 'Liam', 'Isabella', 'Noah', 'Ava', 'Oliver',
                   'Charlotte',
                   'William', 'Mia', 'Ethan', 'Amelia', 'Benjamin', 'Lily', 'Lucas', 'Harper', 'Aiden', 'Emma', 'Liam',
                   'Sophia', 'Noah', 'Olivia', 'Oliver', 'Mia', 'Ethan', 'Ava', 'Lucas', 'Charlotte', 'William',
                   'Isabella',
                   'Liam', 'Mia', 'Alexander', 'Sophia', 'Oliver', 'Emma', 'Noah', 'Isabella', 'Liam', 'Sophia',
                   'Lucas',
                   'Mia', 'Olivia', 'Liam', 'Mia', 'Alexander', 'Emma']

    last_names = ['Johnson', 'Lee', 'Petrov', 'Santos', 'Chen', 'Murphy', 'Rossi', 'Andersen', 'Martinez', 'Wong',
                  'Schneider', 'Patel', 'Kim', 'Nguyen', 'Lopez', 'Kovač', 'Wong', 'Santos', 'Smith', 'Brown', 'Müller',
                  "O'Connor", 'Wong', 'Jansen', 'Garcia', 'Kim', 'Hernandez', 'Nguyen', 'Bianchi', 'Silva', 'Dupont',
                  'Schmidt', 'Rossi', 'Müller', 'Petrova', 'Ivanov', 'Nielsen', 'Schmidt', 'Smith', 'Andersen',
                  'Bianchi', 'Johnson', 'Rodriguez', 'Nguyen', 'Garcia', 'Lee', 'Murphy', 'Hansen', 'Petrov', 'Nielsen']

    genders = ['Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female',
               'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male',
               'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female',
               'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male',
               'Female', 'Female', 'Male', 'Female', 'Male', 'Female']

    countries = ['Australia', 'Canada', 'Russia', 'Brasil', 'China', 'Ireland', 'Italy', 'Denmark', 'Spain',
                 'Singapore', 'Germany', 'India', 'South Korea', 'Vietnam', 'Spain', 'Croatia', 'Malaysia', 'Portugal',
                 'United States', 'United Kingdom', 'Germany', 'Ireland', 'Singapore', 'Netherlands', 'Spain',
                 'South Korea', 'Mexico', 'Vietnam', 'Italy', 'Brasil', 'France', 'Germany', 'Italy', 'Germany',
                 'Bulgaria', 'Russia', 'Denmark', 'Germany', 'Canada', 'Denmark', 'Italy', 'Australia', 'Spain',
                 'Vietnam', 'Spain', 'Singapore', 'Ireland', 'Denmark', 'Russia', 'Denmark']

    provinces = ['Queensland', 'Ontario', 'Moscow', 'São Paulo', 'Shanghai', 'Dublin', 'Lombardy', '', 'Catalonia',
                 'Central', 'Bavaria', 'Maharashtra', 'Seoul', 'Ho Chi Minh', 'Andalusia', 'Zagreb',
                 'Wilayah Persekutuan Kuala Lumpur', 'Lisbon', 'California', 'England', 'Köln', 'Leinster', 'Central',
                 'North Holland', 'Catalonia', 'Seoul', 'Ciudad de México', 'Hanoi', 'Lombardy', 'São Paulo',
                 'Île-de-France', 'Bavaria', 'Lombardy', 'North Rhine-Westphalia', 'Sofia', 'Moscow', 'Zealand',
                 'Bavaria', 'Ontario', 'Capital Region', 'Lombardy', 'New South Wales', 'Catalonia', 'Ho Chi Minh',
                 'Catalonia', 'Central', 'Leinster', 'Jutland', 'Moscow', 'Zealand']

    cities = ['Brisbane', 'Toronto', 'Moscow', 'São Paulo', 'Shanghai', 'Dublin', 'Mediolan', 'Copenhagen', 'Barcelona',
              'Singapore', 'Munich', 'Mumbai', 'Seoul', 'Ho Chi Minh', 'Seville', 'Zagreb', 'Kuala Lumpur', 'Lisbon',
              'Los Angeles', 'London', 'Köln', 'Dublin', 'Singapore', 'Amsterdam', 'Barcelona', 'Seoul', 'Mexico',
              'Hanoi', 'Mediolan', 'São Paulo', 'Paris', 'Munich', 'Mediolan', 'Köln', 'Sofia', 'Moscow', 'Copenhagen',
              'Munich', 'Toronto', 'Copenhagen', 'Mediolan', 'Sydney', 'Barcelona', 'Ho Chi Minh', 'Barcelona',
              'Singapore', 'Dublin', 'Aarhus', 'Moscow', 'Copenhagen']

    streets = ['Ocean Avenue', 'Maple Street', 'Pushkin Street', 'Avenida Paulista', 'Nanjing Road', 'Abbey Street',
               'Via Montenapoleone', 'Strøget', 'Passeig de Gràcia', 'Orchard Road', 'Maximilianstraße', 'Marine Drive',
               'Gangnam-daero', 'Đồng Khởi', 'Calle Sierpes', 'Ilica', 'Jalan Bukit Bintang', 'Avenida da Liberdade',
               'Hollywood Boulevard', 'Oxford Street', 'Hohe Straße', 'Grafton Street', 'Clarke Quay', 'Keizersgracht',
               'Rambla de Catalunya', 'Myeongdong-gil', 'Paseo de la Reforma', 'Phố cổ Hà Nội', 'Corso Buenos Aires',
               'Rua Oscar Freire', 'hamps-Élysées', 'Marienplatz', 'Via Montenapoleone', 'Hohe Straße',
               'Vitosha Boulevard', 'Tverskaya Street', 'Strøget', 'Ludwigstraße', 'Yonge Street', 'Nyhavn',
               'Corso Vittorio Emanuele II', 'George Street', 'Passeig de Gràcia', 'Nguyễn Huệ', 'Carrer de Balmes',
               'Orchard Road', 'Temple Bar', 'Vestergade', 'Arbat Street', 'Nørrebrogade']

    postal_codes = ['4000', 'M5A 1S1', '101000', '01310-200', '200000', 'D01 P6X8', '20121', '1160', '08007', '238857',
                    '80539', '400020', '06000', '700000', '41004', '10000', '55100', '1250-096', '90028', 'W1D 1BS',
                    '50667', 'D02 F294', '179023', '1015 CT', '08007', '04537', '06600', '100000', '20124', '01426-001',
                    '75008', '80331', '20121', '50667', '1000', '125009', '1160', '80539', 'M5B 1L6', '1051', '20121',
                    '2000', '08007', '700000', '08007', '238857', 'D02 YK53', '8000', '119002', '2200']

    phone_numbers = ['+61 1234 5678', '+1 416-555-1234', '+7 495 123-45-67', '+55 11 98765-4321', '+86 21 8765 4321',
                     '+353 1 234 5678', '+39 02 87654321', '+45 12 34 56 78', '+34 93 123 45 67', '+65 9876 5432',
                     '+49 89 12345678', '+91 22 8765 4321', '+82 2 9876 5432', '+84 28 1234 5678', '+34 955 123 456',
                     '+385 1 2345 678', '+60 3-1234 5678', '+351 21 987 6543', '+1 213-555-6789', '+44 20 1234 5678',
                     '+49 221 87654321', '+353 1 987 6543', '+65 8765 4321', '+31 20 123 4567', '+34 93 876 5432',
                     '+82 2 1234 5678', '+52 55 9876 5432', '+84 24 8765 4321', '+39 02 1234567', '+55 11 98765-4321',
                     '+33 1 2345 6789', '+49 89 12345678', '+39 02 87654321', '+49 221 98765432', '+359 2 123 4567',
                     '+7 495 987-6543', '+45 12 34 56 78', '+49 89 87654321', '+1 416-555-6789', '+45 12 34 56 78',
                     '+39 02 9876543', '61 2 8765 4321', '+34 93 987 6543', '+84 28 1234 5678', '+34 93 876 5432',
                     '+65 9876 5432', '+353 1 234 5678', '+45 87 65 43 21', '+7 495 123-45-67', '+45 45 67 89 01']

    urls = ['https://www.emilyjohnson.com.au', 'https://www.alexanderlee.ca', 'https://www.sofiapetrov.ru',
            'https://www.diegosantos.com.br',
            'https://www.miachen.cn',
            'https://www.liammurphy.ie', 'https://www.isabellarossi.it', 'https://www.noahandersen.dk',
            'https://www.avamartinez.es',
            'https://www.oliverwong.sg', 'https://www.charlotteschneider.de', 'https://www.williampatel.in',
            'https://www.miakim.kr',
            'https://www.ethannguyen.vn', 'https://www.amelialopez.es', 'https://www.benjaminkovac.hr',
            'https://www.lilywong.my', 'https://www.lucassantos.pt',
            'https://www.harpersmith.us', 'https://www.aidenbrown.co.uk', 'https://www.emmamueller.de',
            'https://www.liamoconnor.ie',
            'https://www.sophiawong.sg', 'https://www.noahjansen.nl', 'https://www.oliviagarcia.es',
            'https://www.oliverkim.kr',
            'https://www.miahernandez.com.mx', 'https://www.ethannguyen.vn', 'https://www.avabianchi.it',
            'https://www.lucassilva.com.br',
            'https://www.charlottedupont.fr', 'https://www.williamschmidt.de', 'https://www.isabellarossi.it',
            'https://www.liammueller.de',
            'https://www.miapetrova.bg', 'https://www.alexanderivanov.ru', 'https://www.sophianielsen.dk',
            'https://www.oliverschmidt.de',
            'https://www.emmasmith.ca', 'https://www.noahandersen.dk', 'https://www.isabellabianchi.it',
            'https://www.liamjohnson.com.au',
            'https://www.sofiarodriguez.es', 'https://www.lucasnguyen.vn', 'https://www.miagarcia.es',
            'https://www.olivialee.sg', 'https://www.liammurphy.ie',
            'https://www.miahansen.dk', 'https://www.alexanderpetrov.ru', 'https://www.emmanielsen.dk']

    facebook_urls = [
        "https://www.facebook.com/emilyjohnsonbrisbane",
        "https://www.facebook.com/alexanderleetoronto",
        "https://www.facebook.com/sofiapetrov.moscow",
        "https://www.facebook.com/diegosantos.saopaulo",
        "https://www.facebook.com/miachen.shanghai",
        "https://www.facebook.com/liammurphy.dublin",
        "https://www.facebook.com/isabellarossi.milan",
        "https://www.facebook.com/noahandersen.copenhagen",
        "https://www.facebook.com/avamartinez.barcelona",
        "https://www.facebook.com/oliverwong.singapore",
        "https://www.facebook.com/harpersmith.la",
        "https://www.facebook.com/aidenbrown.london",
        "https://www.facebook.com/emmamueller.cologne",
        "https://www.facebook.com/oliverschmidt.munich",
        "https://www.facebook.com/olivialee.singapore",
        "https://www.facebook.com/liammurphy.dublin",
        "https://www.facebook.com/sophianielsen.copenhagen",
        "https://www.facebook.com/noahandersen.copenhagen",
        "https://www.facebook.com/liamurphy.dublin",
        "https://www.facebook.com/emmamueller.cologne",
        "https://www.facebook.com/williamschmidt.munich",
        "https://www.facebook.com/oliverschmidt.munich",
        "https://www.facebook.com/oliverkim.seoul",
        "https://www.facebook.com/miahernandez.mexico",
        "https://www.facebook.com/ethannguyen.hanoi",
        "https://www.facebook.com/miapetrova.sofia",
        "https://www.facebook.com/alexanderivanov.moscow",
        "https://www.facebook.com/olivialee.singapore",
        "https://www.facebook.com/liammurphy.dublin",
        "https://www.facebook.com/miahansen.aarhus",
        "https://www.facebook.com/alexanderpetrov.moscow",
        "https://www.facebook.com/emmanielsen.copenhagen"
    ]

    instagram_urls = [
        "https://www.instagram.com/emilybrisbane",
        "https://www.instagram.com/alexander_toronto",
        "https://www.instagram.com/sofiapetrov_moscow",
        "https://www.instagram.com/diegosantos_sp",
        "https://www.instagram.com/miachen_sh",
        "https://www.instagram.com/liamm_dublin",
        "https://www.instagram.com/isabellar_milan",
        "https://www.instagram.com/noah_copenhagen",
        "https://www.instagram.com/avam_barcelona",
        "https://www.instagram.com/oliverw_singapore",
        "https://www.instagram.com/harper_la",
        "https://www.instagram.com/aidenbrown_london",
        "https://www.instagram.com/charlotte_paris",
        "https://www.instagram.com/oliver_munich",
        "https://www.instagram.com/olivialee_sg",
        "https://www.instagram.com/liamm_dublin",
        "https://www.instagram.com/sophia_copenhagen",
        "https://www.instagram.com/noah_copenhagen",
        "https://www.instagram.com/liamm_dublin",
        "https://www.instagram.com/emma_copenhagen",
        "https://www.instagram.com/williams_munich",
        "https://www.instagram.com/oliver_munich",
        "https://www.instagram.com/oliverk_seoul",
        "https://www.instagram.com/miah_mexico",
        "https://www.instagram.com/ethanng_hanoi",
        "https://www.instagram.com/miap_sofia",
        "https://www.instagram.com/alex_petrov_moscow",
        "https://www.instagram.com/olivialee_sg",
        "https://www.instagram.com/liamm_dublin",
        "https://www.instagram.com/mia_aarhus",
        "https://www.instagram.com/alex_petrov_moscow",
        "https://www.instagram.com/emma_copenhagen"
    ]

    linkedin_urls = [
        "https://www.linkedin.com/in/emilyjohnsonbrisbane",
        "https://www.linkedin.com/in/alexanderleetoronto",
        "https://www.linkedin.com/in/sofiapetrov_moscow",
        "https://www.linkedin.com/in/diegosantos_saopaulo",
        "https://www.linkedin.com/in/miachen_shanghai",
        "https://www.linkedin.com/in/liammurphy_dublin",
        "https://www.linkedin.com/in/isabellarossi_milan",
        "https://www.linkedin.com/in/noahandersen_copenhagen",
        "https://www.linkedin.com/in/avamartinez_barcelona",
        "https://www.linkedin.com/in/oliverwong_singapore",
        "https://www.linkedin.com/in/harpersmith_la",
        "https://www.linkedin.com/in/aidenbrown_london",
        "https://www.linkedin.com/in/charlottedupont_paris",
        "https://www.linkedin.com/in/oliverschmidt_munich",
        "https://www.linkedin.com/in/olivialee_singapore",
        "https://www.linkedin.com/in/liammurphy_dublin",
        "https://www.linkedin.com/in/sophianielsen_copenhagen",
        "https://www.linkedin.com/in/noahandersen_copenhagen",
        "https://www.linkedin.com/in/liammurphy_dublin",
        "https://www.linkedin.com/in/emmamueller_cologne",
        "https://www.linkedin.com/in/williamschmidt_munich",
        "https://www.linkedin.com/in/oliverschmidt_munich",
        "https://www.linkedin.com/in/oliverkim_seoul",
        "https://www.linkedin.com/in/miahernandez_mexico",
        "https://www.linkedin.com/in/ethannguyen_hanoi",
        "https://www.linkedin.com/in/miapetrova_sofia",
        "https://www.linkedin.com/in/alexanderivanov_moscow",
        "https://www.linkedin.com/in/olivialee_singapore",
        "https://www.linkedin.com/in/liammurphy_dublin",
        "https://www.linkedin.com/in/miahansen_aarhus",
        "https://www.linkedin.com/in/alexanderpetrov_moscow",
        "https://www.linkedin.com/in/emmanielsen_copenhagen"
    ]

    return {
        'discover_cities': [City.objects.get(name=obj.city.name) for obj in
                            Property.objects.annotate(city_count=Count('city'))][:8],
    }
