import psycopg2
from psycopg2.extras import RealDictCursor
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

@app.get('/precomputed_view')
def get_precomputed_view():
    start_time = request.args.get('start')
    end_time = request.args.get('end')
    social_media = request.args.get('social_media', default=None)
    if start_time is None or end_time is None:
        return "Invalid request", 501
    else:
        try:
            datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            datetime.strptime(end_time, '%Y-%m-%d %H:%M')
        except ValueError:
            return "Invalid time parameters (must be in YYYY-MM-DD HH:MM format)", 501
    SQL_GET_STREAM_CMD = f"""SELECT timestamp, count, unique_count
                             FROM {dbtable}
                             WHERE timestamp BETWEEN \'{start_time}\' AND \'{end_time}\'"""
    if social_media is not None:
        SQL_GET_STREAM_CMD += f""" AND LOWER(social_media) LIKE LOWER(\'{social_media}\')"""
    SQL_GET_STREAM_CMD += ";"
    with dbconn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(SQL_GET_STREAM_CMD)
        query_result = cursor.fetchall()
    return jsonify(result=query_result)
