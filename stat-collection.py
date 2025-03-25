from api.already_solved import get_school_solve
from api.get_ranking import get_school_rank
import requests
import csv
import os
import datetime


def log_to_csv(problems_count, school_rank):
    """
    Log data to CSV file with timestamp, problems count and school ranking
    """
    file_path = "./boj-swj-log.csv"
    file_exists = os.path.isfile(file_path)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header if file is being created for the first time
        if not file_exists:
            csv_writer.writerow(["Timestamp", "Problems Count", "School Ranking"])

        # Write the data
        csv_writer.writerow([current_time, problems_count, school_rank])


school_problems = get_school_solve(712)
rank = get_school_rank(requests.Session(), "한세사이버보안고등학교")

print(len(school_problems))
print(rank)

# Log the data to CSV file
log_to_csv(len(school_problems), rank)
