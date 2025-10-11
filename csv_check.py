import requests
import csv
import re
import time
import json
import os

# Constants
usn_regex = r'^1ms\d{2}[a-z]{2}\d{3}$'
departments = ["AD", "AI", "AT", "BT", "CH", "CI", "CS", "CV", "CY", "EC", "EE", "ET", "IS", "ME"]
BATCH = "21"
API_URL = "http://127.0.0.1:8000/exam?usn="
OUTPUT_DIR = "dept_csvs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

college_data = {}


def is_valid_usn(usn):
    return re.match(usn_regex, usn, re.IGNORECASE)


def fetch_exam_data(usn):
    try:
        response = requests.get(f"{API_URL}{usn}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching {usn}: {e}")
    return None


def generate_data_per_dept():
    for dept in departments:
        print(f"\n🔍 Processing department: {dept}")
        dept_records = []
        last_valid_usn = ""
        consecutive_nulls = 0
        usn_counter = 1
        buffer = []

        csv_file_path = os.path.join(OUTPUT_DIR, f"exam_{dept}.csv")
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["USN", "Name", "Semester", "SGPA", "CGPA", "Valid"])

            while True:
                usn = f"1ms{BATCH}{dept.lower()}{str(usn_counter).zfill(3)}"
                if not is_valid_usn(usn):
                    print(f"⚠️ Skipping invalid USN: {usn}")
                    usn_counter += 1
                    continue

                data = fetch_exam_data(usn)
                is_valid = bool(data and data.get("name"))
                record = {
                    "usn": usn,
                    "name": data.get("name") if data else None,
                    "semester": data.get("semester") if data else None,
                    "sgpa": data.get("sgpa") if data else None,
                    "cgpa": data.get("cgpa") if data else None,
                    "valid": is_valid
                }

                writer.writerow([usn, record["name"], record["semester"], record["sgpa"], record["cgpa"],
                                 "Yes" if is_valid else "No"])
                buffer.append(record)

                if is_valid:
                    last_valid_usn = usn
                    consecutive_nulls = 0
                    dept_records.extend(buffer)
                    buffer = []
                else:
                    consecutive_nulls += 1

                print(f"USN: {usn} | Valid: {'Yes' if is_valid else 'No'} | Consecutive Nulls: {consecutive_nulls}")

                if consecutive_nulls >= 5:
                    print(f"✅ Found last USN for {dept}: {last_valid_usn}")
                    break

                usn_counter += 1
                time.sleep(0.2)

        # Add to college-wide JSON after trimming last 5 invalids
        if consecutive_nulls >= 5:
            dept_records = dept_records[:-5]
        college_data[dept] = dept_records

    # Save full JSON
    with open("college_exam_results.json", "w") as jf:
        json.dump(college_data, jf, indent=4)
    print("\n🎉 All department files and full JSON generated.")


if __name__ == "__main__":
    generate_data_per_dept()
