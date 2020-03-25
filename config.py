from flask import request
from datetime import datetime
import json
import uuid
import pymysql
from flask import Flask, send_from_directory, abort                
from flask_cors import CORS


def Connection():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='OHAvgawzUw##32',
                                db='medParliament',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    #cursor = connection.cursor()
    return connection
