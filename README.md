# BandShare
A web app for musicians and bands written in Python using the Django framework.

# Notes

## Virtualenv
py -m venv localenv

## One-time
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

.\localenv\Scripts\Activate.ps1

py -m pip install -r requirements.txt

## Tests
py -m .\manage.py test 


## Migration
### Create
py manage.py makemigrations
