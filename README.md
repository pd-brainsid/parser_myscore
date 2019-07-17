# parser_myscore
There is parser for https://www.myscore.com.ua/

At this time, information on completed hockey and soccer games for today is provided.

For this app you should use Python3.6+

For install required packages use command:
$ pip install -r requirements.txt

Use the command to launch the application:
$ bash startapp.sh

This application has two parts:
1. Parser
2. App

A parser is required to obtain games information and store that information in a database.
App required to provide information about a particular sport.

for get info about games use GET request on addr "http://<your_addr>/api/games/<sport_name>'"
