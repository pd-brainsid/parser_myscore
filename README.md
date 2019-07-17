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

To get game information, you need to take these steps:
1. curl -H "Content-Type: application/json" -X POST -d '{"username":"user","password":"1111"}' http://<addr>/auth - to get a token
2. curl -X GET http://<addr>/api/v1/games/<sport_name> -H "Authorization: JWT <token token from the last step>" - to get information
