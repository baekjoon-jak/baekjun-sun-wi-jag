import requests
import csv
import os
import datetime
from pathlib import Path
from api.get_ranking import get_school_ranks, SchoolRank


def log_to_csv(ranks: list[SchoolRank]):
    """Log school ranks to CSV file with timestamp."""
    dir = str(Path(__file__).parent)
    file_path = os.path.join(dir, "boj-hs-rank-log.csv")
    file_exists = os.path.isfile(file_path)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)

        if not file_exists:
            csv_writer.writerow(["Timestamp", "School Name", "Rank"])

        for rank_obj in ranks:
            csv_writer.writerow([current_time, rank_obj.name, rank_obj.rank])


if __name__ == "__main__":
    session = requests.Session()
    ranks = get_school_ranks(session)
    if ranks:
        log_to_csv(ranks)
        print("School ranks logged to CSV.")
    else:
        print("Failed to retrieve school ranks.")
