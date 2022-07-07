"# finale_blockchain" 

Welcome to this project that shows how a shoe auction site works.

Tools used: Python(3.10.2), Django, Redis, Web3, Infuria

Requirements: Python and Redis installed

Steps for run the project (Windows):

download the project

open the console inside the folder "finale_blockchain-main"

create a virtual environment -> "python -m venv myvenv"

run the virtual environment -> "myvenv\Scripts\activate"

install requirements.txt -> "pip install -r requirements.txt"

"python manage.py makemigrations"

"python manage.py migrate"

"python manage.py makemigrations app"

"python manage.py migrate app"

open Ubuntu and run "sudo service redis-server start"

run the project -> "python manage.py runserver"
