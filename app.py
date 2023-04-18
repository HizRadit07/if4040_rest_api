import psycopg2
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

dbhost = "localhost"
dbname = "if4040"
dbtable = "social_media"

# connect to postgresql server
dbconn = psycopg2.connect(
        host=dbhost,
        database=dbname)

@app.get('/streamapi')
def getstreamdata():
    start_time = request.args.get('start')
    end_time = request.args.get('end')
    social_media = request.args.get('social_media', default=None)
    if start_time is None or end_time is None:
        return "Invalid request", 500
    SQL_GET_STREAM_CMD = f"""SELECT timestamp, count, unique_count
                             FROM {dbtable}
                             WHERE timestamp BETWEEN \'{start_time}\' AND \'{end_time}\'"""
    if social_media is not None:
        SQL_GET_STREAM_CMD += f""" AND social_media LIKE \'{social_media}\'"""
    SQL_GET_STREAM_CMD += ";"
    with dbconn.cursor() as cursor:
        cursor.execute(SQL_GET_STREAM_CMD)
        query_result = cursor.fetchone()
    total_count = query_result[0]
    total_unique_count = query_result[1]
    return jsonify(
            count=total_count,
            unique_count=total_unique_count
            )

