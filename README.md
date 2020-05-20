# summit-mail
A program to automate the mass sending of emails after fairs/conferences/events. 
## how to run
install python3.7 & pipenv
```
$ cd myproject
$ pipenv install
$ cp .env.example .env
```
Set environment variables in `.env` 
* `SENDER_EMAIL = [email you want to send from]`
* `SENDER_EMAIL_PASSWORD = [app password of the email (not user password)]`
* `TEST_EMAIL = [if you want to send your email to an address to check the format, enter it here]`  

`$ pipenv run python main.py`
