# TesteDSIN

## Setup

``` 
git clone https://github.com/marcoshronzani/TesteDSIN.git
cd TesteDSIN
copy contrib\env-sample .env
python -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt
python manage.py loaddata initial_data.json
```