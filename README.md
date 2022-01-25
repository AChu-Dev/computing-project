# Computing Project:
---
COM617 (Industrial Computing Project) - SnowCore Web App (Group 1)

## Dependencies: 
---
- Python 3 Module Django
- Python 3 Module Dotenv

## How to run: 
---
Please ensure you have the needed Dependencies installed on either your system or Python 3 Virtual Environment, after that add a `.env` file to the root of the servers dir with your Django key. The following commands detail the steps:

```
cd ./experimental/snowcore/ 
touch .env 
echo 'DJANGOKEY="YOUR-KEY-HERE"' > .env 
python manage.py runserver

```

Then access the servers webpages on [http://localhost:8000/](http://localhost:8000/). If you then decide you want to host this to the internet you'll need to see how to port forward your localhost port 8000 through your internet router.

## Download:
---
You can download our latest release or git clone the current development version from the main branch of this repo.

## License:
---
Apache License Version 2.0 
