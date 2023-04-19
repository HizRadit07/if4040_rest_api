import psycopg2
from datetime import datetime
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

dbhost = "localhost"
dbname = "if4040"
dbtable = "social_media"
# dbuser = "postgres"
# dbpwd = "postgres"

# connect to postgresql server
dbconn = psycopg2.connect(
        host=dbhost,
        database=dbname,
        # user=dbuser,
        # password=dbpwd
        )

@app.get('/streamapi')
def getstreamdata():
    start_time = request.args.get('start')
    end_time = request.args.get('end')
    social_media = request.args.get('social_media', default=None)
    if start_time is None or end_time is None:
        return "Invalid request", 500
    else:
        try:
            datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            datetime.strptime(end_time, '%Y-%m-%d %H:%M')
        except ValueError:
            return "Invalid time parameters (must be in YYYY-MM-DD HH:MM format)", 500
    SQL_GET_STREAM_CMD = f"""SELECT timestamp, count, unique_count
                             FROM {dbtable}
                             WHERE timestamp BETWEEN \'{start_time}\' AND \'{end_time}\'"""
    if social_media is not None:
        SQL_GET_STREAM_CMD += f""" AND social_media LIKE \'{social_media}\'"""
    SQL_GET_STREAM_CMD += ";"
    with dbconn.cursor() as cursor:
        cursor.execute(SQL_GET_STREAM_CMD)
        query_result = cursor.fetchone()
    if query_result is not None:
        total_count = query_result[0]
        total_unique_count = query_result[1]
    else:
        total_count = 0
        total_unique_count = 0
    return jsonify(
            count=total_count,
            unique_count=total_unique_count
            )
