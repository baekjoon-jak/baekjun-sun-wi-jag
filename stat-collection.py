import requests
import os
import datetime
from api.get_ranking import get_school_ranks, SchoolRank
from api.already_solved import get_school_solve
from influxdb import InfluxDBClient
from dotenv import load_dotenv

load_dotenv()


def log_to_influxdb(ranks: list[SchoolRank], solved_problems: int):
    """Log school ranks to InfluxDB."""
    # InfluxDB connection parameters
    host = os.environ.get("INFLUXDB_HOST")
    port = int(os.environ.get("INFLUXDB_PORT", 8086))
    user = os.environ.get("INFLUXDB_USER", "admin")
    password = os.environ.get("INFLUXDB_PASSWORD", "admin")
    dbname = os.environ.get("INFLUXDB_DATABASE", "boj")

    # Connect to InfluxDB
    client = InfluxDBClient(
        host=host, port=port, username=user, password=password, database=dbname
    )

    # Create database if it doesn't exist
    dbs = client.get_list_database()
    if not any(db["name"] == dbname for db in dbs):
        client.create_database(dbname)
        client.switch_database(dbname)

    # Prepare data points
    current_time = datetime.datetime.now(datetime.UTC).isoformat()
    points = []

    for rank_obj in ranks:
        point = {
            "measurement": "school_ranks",
            "tags": {"school_name": rank_obj.name},
            "time": current_time,
            "fields": {"rank": int(rank_obj.rank)},  # 또는 float(rank_obj.rank)
        }
        points.append(point)

    "measurement: hschs_solved_problems를 만들어서 기록"
    point = {
        "measurement": "hschs_solved_problems",
        "tags": {
            "school_id": os.getenv("SCHOOL_ID"),
            "school_name": "한세사이버보안고등학교",
        },
        "time": current_time,
        "fields": {"solved_problems": solved_problems},
    }
    points.append(point)

    # Write data to InfluxDB
    client.write_points(points)


if __name__ == "__main__":
    session = requests.Session()
    ranks = get_school_ranks(session)

    school_id = os.getenv("SCHOOL_ID")
    solved_problems = get_school_solve(school_id)
    if ranks:
        log_to_influxdb(ranks, len(solved_problems))
        print("School ranks logged to InfluxDB.")
    else:
        print("Failed to retrieve school ranks.")
