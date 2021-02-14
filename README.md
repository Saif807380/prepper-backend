# Prepper

Preparing for travel can be a tedious task. Often the packing done before a trip turns out to be insufficient especially due to some unforeseen circumstances. Changes in the destination's weather can cause health problems to travellers that are sensitive to those conditions.

Prepper is a solution that can help you prep for your journey. Prepper provides you the functionality to create your custom travel plans for which it provides valuable insights. Knowing beforehand the weather conditions of the travel itinerary can help you pack all the necessary things and medicines. Additionally, Prepper sends you reminders about your medicines and also manages their stock for you.

## Features

1. User can create and view new travel plans
2. If user gets an SMS of some travel booking, that is detected and automatically a new travel plan is created
3. For every city in a travel plan, the user can view -
  - Weather Information like Temperature, Humidity, Air Pressure and Wind Speed
  - Pollen quantity in the air
  - Air quality index of the city
4. User gets travel suggestions based on the values of the above quantities
5. User can add pills to virtual medicine pouch and set reminders for them
6. Notifications about weather conditions of the cities

## Project Structure

```
.
├── requirements.txt
├── src
│   └── app
│       ├── __init__.py
│       ├── __pycache__
│       ├── database
│       ├── exceptions
│       ├── helpers
│       ├── main.py
│       ├── middleware
│       └── routers
└── tests
    ├── __init__.py
    ├── conftest.py
    └── test_auth.py

9 directories, 6 files
```

## Requirements

```
bcrypt==3.2.0
fastapi==0.63.0
passlib==1.7.4
psycopg2-binary==2.8.6
pydantic==1.7.3
pytest==6.2.1
python-crontab==2.5.1
python-dotenv==0.15.0
python-jose==3.2.0
python-multipart==0.0.5
requests==2.25.1
SQLAlchemy==1.3.22
starlette==0.13.6
uvicorn==0.13.3
```

## Support

Feel free to contact any of the maintainers. We're happy to help!
