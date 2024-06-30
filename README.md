<p align="center">
  <img src="https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/f10da377-497c-434b-a84b-9c9b1f593fda" width="25%">
</p>
<img src="https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/712f1c95-eab5-457c-9ba7-d0eb09709f38">

<br/>

## Global Estate Hub

Global Estate Hub is an online platform that enables users to browse property listings for both rental and sale purposes. This project aims to create a central hub for real estate advertisements from around the world, providing users with easy access to a wide range of information about available properties on the market.

<br/>

## Live Preview

[ Global Estate Hub](https://globalestatehub.com.pl)

https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/c8d1be33-6094-4002-98bd-28fd13870889

You can log in to the [Admin Panel](https://globalestatehub.com.pl/admin) with the following credentials:

Login: admin@<i></i>gmail.com<br/>
Password: admin

You can log in to the website via [Login](https://globalestatehub.com.pl/login){:target="_blank"} using the following credentials:

Login: homeseeker22@<i></i>example.com<br/>
Password: !1Qwerty

<br/>

## Features

**1. Accounts**

- Registration verified by an activation link.
- User account management (changing login, password, profile photo, location, social media links, etc.).
- Password recovery verified by a one-time code during the user session.

**2. Blog**

- Ability to search for articles by categories, tags, and keywords.
- Comment system with nested replies (allowing editing, deletion, liking, and disliking).

**3. Properties**

- Ability to add a new real estate listing.
- Property sorting options.
- Property search by keyword.
- Ability to contact and schedule a meeting with the agent offering a specific property.
- Review system for property listings.

<br/>

## Implemented Languages and Frameworks
<div>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/192158954-f88b5814-d510-4564-b285-dff7d6400dad.png" alt="HTML" title="HTML"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/183898674-75a4a1b1-f960-4ea9-abcb-637170a00a75.png" alt="CSS" title="CSS"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/117447155-6a868a00-af3d-11eb-9cfe-245df15c9f3f.png" alt="JavaScript" title="JavaScript"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" alt="Python" title="Python"/></code>
	<code><img width="50" src="https://github.com/marwin1991/profile-technology-icons/assets/62091613/9bf5650b-e534-4eae-8a26-8379d076f3b4" alt="Django" title="Django"/></code>
  <code><img width="50" src="https://user-images.githubusercontent.com/25181517/192107858-fe19f043-c502-4009-8c47-476fc89718ad.png" alt="REST" title="REST"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/192108372-f71d70ac-7ae6-4c0d-8395-51d8870c2ef0.png" alt="Git" title="Git"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/189715289-df3ee512-6eca-463f-a0f4-c10d94a06b2f.png" alt="Figma" title="Figma"/></code>
</div>

<br/>

## File Structure

```
django_global_estate_hub
├── core
│   ├── templatetags
│   │   ├── __init__.py
│   │   └── core_filters.py
│   ├── models.py
│   ├── __init__.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── admin.py
│   ├── api
│   │   ├── serializers.py
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── templates
│   │   └── core
│   │       ├── newsletter_mail.html
│   │       ├── offcanvas.html
│   │       ├── page-title.html
│   │       ├── index.html
│   │       ├── about.html
│   │       ├── privacy-policy.html
│   │       ├── base.html
│   │       ├── contact.html
│   │       ├── rodo-rules.html
│   │       ├── main-menu.html
│   │       ├── footer.html
│   │       ├── properties-results.html
│   │       ├── top-agents.html
│   │       ├── header.html
│   │       ├── error.html
│   │       ├── faq.html
│   │       └── contact_mail.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
├── db.sqlite3
├── blog
│   ├── templatetags
│   │   ├── __init__.py
│   │   └── pagination_tag.py
│   ├── models.py
│   ├── __init__.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── admin.py
│   ├── api
│   │   ├── serializers.py
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── templates
│   │   └── blog
│   │       ├── blog.html
│   │       ├── pagination.html
│   │       ├── blog-results.html
│   │       ├── article-categories.html
│   │       ├── article-details.html
│   │       ├── article-tags.html
│   │       ├── comments-section.html
│   │       └── sidebar.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── README.md
├── properties
│   ├── templatetags
│   │   ├── property_filters.py
│   │   └── __init__.py
│   ├── models.py
│   ├── __init__.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── admin.py
│   ├── api
│   │   ├── serializers.py
│   │   ├── __init__.py
│   │   ├── permissions.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── templates
│   │   └── properties
│   │       ├── pagination.html
│   │       ├── properties-category.html
│   │       ├── properties-cities.html
│   │       ├── properties.html
│   │       ├── schedule_mail.html
│   │       ├── property-details.html
│   │       ├── sidebar.html
│   │       └── add-property.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── accounts
│   ├── signals.py
│   ├── models.py
│   ├── __init__.py
│   ├── tokens.py
│   ├── apps.py
│   ├── admin.py
│   ├── api
│   │   ├── serializers.py
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── templates
│   │   └── accounts
│   │       ├── forget-password.html
│   │       ├── register.html
│   │       ├── login.html
│   │       ├── activation_email.html
│   │       ├── account-details.html
│   │       ├── password_reset_email.html
│   │       └── account-settings.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static
│   ├── css
│   │   └── styles.css
│   └── js
│       ├── user.js
│       ├── animations.js
│       ├── blog.js
│       ├── scripts.js
│       ├── general.js
│       ├── add-property.js
│       └── fslightbox.js
├── manage.py
└── global_estate_hub
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

<br/>

## API Reference

| Method | URL     | Description                |
| :-------- | :------- | :------------------------- |
| `GET` | `api/v1` | All endpoints. |
| `GET` | `api/v1/newsletters` | Retrieve all newsletters. |
| `GET` | `api/v1/users` | Retrieve all users. |
| `GET` | `api/v1/users/<int:pk>` | Retrieve user with a specific ID. |
| `GET` | `api/v1/users?account_type={account_type}` | Retrieve all users with a specific account type. |
| `GET` | `api/v1/users?is_agent={is_agent}` | Retrieve all users who are agents. |
| `GET` | `api/v1/users?is_verified={is_verified}` | Retrieve all verified users. |
| `GET` | `api/v1/users/individuals` | Retrieve all individual profiles. |
| `GET` | `api/v1/users/individuals/<int:pk>` | Retrieve user's individual profile with a specific ID. |
| `GET` | `api/v1/users/individuals?gender={gender}` | Retrieve all individual user profiles with a specific gender. |
| `GET` | `api/v1/users/individuals?country={country}` | Retrieve all individual user profiles with a specific country. |
| `GET` | `api/v1/users/individuals?province={province}` | Retrieve all individual user profiles with a specific province. |
| `GET` | `api/v1/users/individuals?city={city}` | Retrieve all individual user profiles with a specific city. |
| `GET` | `api/v1/users/business` | Retrieve all business profiles. |
| `GET` | `api/v1/users/business/<int:pk>` | Retrieve user's business profile with a specific ID. |
| `GET` | `api/v1/users/business?country={country}` | Retrieve all business user profiles with a specific country. |
| `GET` | `api/v1/users/business?province={province}` | Retrieve all business user profiles with a specific province. |
| `GET` | `api/v1/users/business?city={city}` | Retrieve all business user profiles with a specific city. |
| `GET` | `api/v1/articles` | Retrieve all articles. |
| `GET` | `api/v1/articles/<int:pk>` | Retrieve article with a specific ID. |
| `GET` | `api/v1/articles?category__id={category.id}` | Retrieve all articles with a specific category ID. |
| `GET` | `api/v1/articles?category__name={category.name}` | Retrieve all articles with a specific category name. |
| `GET` | `api/v1/comments` | Retrieve all comments. |
| `GET` | `api/v1/comments/<int:pk>` | Retrieve comment with a specific ID. |
| `GET` | `api/v1/users/comments?user__id={user.id}` | Retrieve comments posted by a specific user ID. |
| `GET` | `api/v1/users/comments?user__username={user.username}` | Retrieve comments posted by a specific user username. |
| `GET` | `api/v1/users/comments?active={active}` | Retrieve all active comments. |
| `GET` | `api/v1/users/comments?level={level}` | Retrieve comments by a specific level. |
| `GET` | `api/v1/users/comments?article__id={article.id}` | Retrieve comments under an article with a specific ID. |
| `GET` | `api/v1/users/comments?article__title={article.title}` | Retrieve comments under an article with a specific title. |
| `GET` | `api/v1/properties` | Retrieve all properties. |
| `GET` | `api/v1/properties/<int:pk>` | Retrieve property with a specific ID. |
| `GET` | `api/v1/properties/search={keyword}` | Search and retrieve properties by title using a keyword. |
| `GET` | `api/v1/properties/ordering=title` | Sorts properties by title using the chosen method (ascending, descending) and retrieves them. |
| `GET` | `api/v1/properties/ordering=price` | Sorts properties by price using the chosen method (ascending, descending) and retrieves them. |
| `GET` | `api/v1/properties/ordering=featured` | Sorts properties by featured using the chosen method (ascending, descending) and retrieves them. |
| `GET` | `api/v1/properties/user__id={user.id}` | Retrieve properties posted by a specific user ID. |
| `GET` | `api/v1/properties/user__username={user.username}` | Retrieve properties posted by a specific user username. |
| `GET` | `api/v1/properties/listing_status__id={listing_status.id}` | Retrieve properties with a specific listing status ID. |
| `GET` | `api/v1/properties/listing_status__name={listing_status.id}` | Retrieve properties with a specific listing status name. |
| `GET` | `api/v1/properties/category__id={category.id}` | Retrieve properties with a specific category ID. |
| `GET` | `api/v1/properties/category__name={category.name}` | Retrieve properties with a specific category name. |
| `GET` | `api/v1/properties/year_of_built={year_of_built}` | Retrieve properties with a specific year of built. |
| `GET` | `api/v1/properties/max_year={year_of_built}` | Retrieve all properties up to a specified maximum year of built. |
| `GET` | `api/v1/properties/min_year={year_of_built}` | Retrieve all properties from a specified minimum year of built. |
| `GET` | `api/v1/properties/min_year={year_of_built}&max_year={year_of_built}` | Retrieve all properties within the specified ranges of construction year. |
| `GET` | `api/v1/properties/price={price}` | Retrieve properties with a specific price. |
| `GET` | `api/v1/properties/max_price={price}` | Retrieve all properties up to a specified maximum price. |
| `GET` | `api/v1/properties/min_price={price}` | Retrieve all properties from a specified minimum price. |
| `GET` | `api/v1/properties/min_price={price}&max_price={price}` | Retrieve all properties within the specified ranges of price. |
| `GET` | `api/v1/properties/number_of_bedrooms={number_of_bedrooms}` | Retrieve properties with a specific number of bedrooms. |
| `GET` | `api/v1/properties/max_bedrooms={number_of_bedrooms}` | Retrieve all properties up to a specified maximum number of bedrooms. |
| `GET` | `api/v1/properties/min_bedrooms={number_of_bedrooms}` | Retrieve all properties from a specified minimum number of bedrooms. |
| `GET` | `api/v1/properties/min_bedrooms={number_of_bedrooms}&max_bedrooms={number_of_bedrooms}` | Retrieve all properties within the specified ranges of number of bedrooms. |
| `GET` | `api/v1/properties/number_of_bathrooms={number_of_bathrooms}` | Retrieve properties with a specific number of bathrooms. |
| `GET` | `api/v1/properties/max_bathrooms={number_of_bathrooms}` | Retrieve all properties up to a specified maximum number of bathrooms. |
| `GET` | `api/v1/properties/min_bathrooms={number_of_bathrooms}` | Retrieve all properties from a specified minimum number of bathrooms. |
| `GET` | `api/v1/properties/min_bathrooms={number_of_bathrooms}&max_bathrooms={number_of_bathrooms}` | Retrieve all properties within the specified ranges of number of bathrooms. |
| `GET` | `api/v1/properties/square_meters={square_meters}` | Retrieve properties with a specific square meters. |
| `GET` | `api/v1/properties/max_square={square_meters}` | Retrieve all properties up to a specified maximum square meters. |
| `GET` | `api/v1/properties/min_square={square_meters}` | Retrieve all properties from a specified minimum square meters. |
| `GET` | `api/v1/properties/min_square={square_meters}&max_square={square_meters}` | Retrieve all properties within the specified ranges of square meters. |
| `GET` | `api/v1/properties/parking_space={parking_space}` | Retrieve properties with a specific parking space. |
| `GET` | `api/v1/properties/max_space={parking_space}` | Retrieve all properties up to a specified maximum parking space. |
| `GET` | `api/v1/properties/min_space={parking_space}` | Retrieve all properties from a specified minimum parking space. |
| `GET` | `api/v1/properties/min_space={parking_space}&max_space={parking_space}` | Retrieve all properties within the specified ranges of parking space. |
| `GET` | `api/v1/properties/city__id={city.id}` | Retrieve properties with a specific city ID. |
| `GET` | `api/v1/properties/city__name={city.name}` | Retrieve properties with a specific city name. |
| `GET` | `api/v1/properties/province={province}` | Retrieve properties with a specific province. |
| `GET` | `api/v1/properties/country={country}` | Retrieve properties with a specific country. |
| `GET` | `api/v1/properties/is_featured={is_featured}` | Retrieve featured or non-featured properties. |
| `GET` | `api/v1/reviews` | Retrieve all reviews. |
| `GET` | `api/v1/reviews/<int:pk>` | Retrieve review with a specific ID. |
| `GET` | `api/v1/reviews/user__id={user.id}` | Retrieve reviews posted by a specific user ID. |
| `GET` | `api/v1/reviews/user__username={user.username}` | Retrieve reviews posted by a specific user username. |
| `GET` | `api/v1/reviews/property__id={property.id}` | Retrieve reviews for a property with a specific ID. |
| `GET` | `api/v1/reviews/property__title={property.title}` | Retrieve reviews for a property with a specific property title. |
| `GET` | `api/v1/tour-schedules` | Retrieve all tour schedules. |
| `GET` | `api/v1/tour-schedules/<int:pk>` | Retrieve tour schedule with a specific ID. |
| `GET` | `api/v1/tour-schedules/customer__id={customer.id}` | Retrieve tour schedules requested by a specific user ID. |
| `GET` | `api/v1/tour-schedules/customer__username={customer.username}` | Retrieve tour schedules requested by a specific user username. |
| `GET` | `api/v1/tour-schedules/property__id={property.id}` | Retrieve tour schedules related to the property ID. |
| `GET` | `api/v1/tour-schedules/property__title={property.title}` | Retrieve tour schedules related to the property title. |

<br/>

## Installation

Install Python 3.10 and clone the GitHub repository.

```bash
$ git clone https://github.com/hubertrykala93/django_global_estate_hub.git
$ cd django_global_estate_hub
```

Create a virtual environment to install dependencies in and activate it:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Install the dependencies:

```bash
(venv)$ pip3 install -r requirements.txt
```

Run the project.

```bash
(venv)$ python3 manage.py runserver
```

And then navigate to ```http://127.0.0.1:8000``` or ```http://localhost:8000```.

<br/>

## Authors

- [Hubert Rykała - Backend Developer](https://github.com/hubertrykala93)
- [Szymon Lewandowski - Frontend Developer](https://github.com/Szymon-Levy)

<br/>
  
## Screenshots and Videos

![login](https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/01781d87-672a-4166-8c9b-c0b256fcb54e)

![sign_up](https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/c71ad3b1-8360-4657-89f3-7ea0a5ee1ef6)

https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/c7c6c3e4-10b3-4084-ac9a-50324acb62ea

https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/083530fc-18f1-4a21-8906-7e995666e38c

https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/ea3cbc5c-343e-47ba-afbd-f883eb1d8b0f

https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/ad4a8ead-3682-4198-b5e6-d72f650daf8c

https://github.com/hubertrykala93/django_global_estate_hub/assets/94188186/bceef524-69b3-4def-858c-2010673893c4










