from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import json

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def handle_get():
    data = {
        "message": "API is up and running"
    }
    return jsonify(data), 200


@app.route('/status', methods=['POST'])
def handle_post():
    request_data = request.json
    response_data = {
        "message": "API is up and running",
        "data": request_data.get("data", "No data provided"),
        "status": request_data.get("status", "No status provided")
    }
    return jsonify(response_data), 200


@app.route("/get_student_data", methods=["GET"])
def get_student_data():
    usn = request.args.get("usn", "").strip()
    dob = request.args.get("dob", "").strip()

    if not usn or not dob:
        return jsonify({"error": "Missing usn or dob parameter"}), 400

    try:
        yyyy, mm, dd = dob.split("-")
    except ValueError:
        return jsonify({"error": "DOB must be in YYYY-MM-DD format"}), 400

    login_url = "https://parents.msrit.edu/newparents/index.php"

    login_data = {
        "username": usn,
        "dd": dd,
        "mm": mm,
        "yyyy": yyyy,
        "passwd": dob,
        "remember": "No",
        "option": "com_user",
        "task": "login",
        "return": "",
        "958d8408014b5d49cad60943434949ff": "1"
    }

    session = requests.Session()

    try:
        login_response = session.post(login_url, data=login_data, timeout=10)
        if login_response.status_code != 200:
            return jsonify({"error": "Login failed. Check credentials or site availability."}), 500

        dashboard_url = (
            "https://parents.msrit.edu/newparents/"
            "index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard"
        )
        dashboard_response = session.get(dashboard_url, timeout=10)
        if dashboard_response.status_code != 200:
            return jsonify({"error": "Failed to retrieve dashboard. Possibly invalid credentials or site error."}), 500

        soup = BeautifulSoup(dashboard_response.text, "html.parser")

        try:
            student_name = soup.find("div", class_="cn-stu-data") \
                .find("h3").text.strip()
        except AttributeError:
            return jsonify({"error": "Could not retrieve student name. Possibly incorrect DOB/USN."}), 404

        # Extract student ID
        try:
            student_id_divs = soup.find_all("div", class_="cn-stu-data1")
            # The second such div typically has the ID
            student_id = student_id_divs[1].find("h2").text.strip()
        except (IndexError, AttributeError):
            return jsonify({"error": "Could not retrieve student ID. Possibly incorrect DOB/USN."}), 404

        # Retrieve marks from the inline script
        script_tag = soup.find("script", string=lambda text: "columns" in text if text else False)
        if not script_tag:
            return jsonify({"error": "Could not find CIE marks script tag."}), 404

        script_text = script_tag.string
        pattern = r'\["([^"]+)",(\d+)\]'
        cie_marks = re.findall(pattern, script_text)
        cie_dict = {code: int(mark) for code, mark in cie_marks}

        # --- Step 6: Extract courses and attendance ---
        courses = []
        course_table = soup.find("table", class_="cn-pay-table")
        if course_table and course_table.find("tbody"):
            for row in course_table.find("tbody").find_all("tr"):
                cols = row.find_all("td")
                if len(cols) < 6:
                    continue

                course_code = cols[0].text.strip()
                course_name = cols[1].text.strip()
                attendance_str = cols[4].text.strip()

                try:
                    attendance = int(attendance_str)
                except ValueError:
                    attendance = None

                cie_link_tag = cols[5].find("a")
                cie_link = cie_link_tag["href"] if cie_link_tag else None
                cie_score = cie_dict.get(course_code, "N/A")

                courses.append({
                    "Course Code": course_code,
                    "Course Name": course_name,
                    "CIE Score": cie_score,
                    "Attendance": attendance,
                    "CIE Link": cie_link
                })

        last_updated_el = soup.find("p", class_="cn-last-update")
        if last_updated_el:
            last_updated = last_updated_el.text.replace("Last Updated On: ", "").strip()
        else:
            last_updated = ""

        data = {
            "Student Name": student_name,
            "Student ID": student_id,
            "Courses": courses,
            "Last Updated": last_updated
        }

        return jsonify(data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network or request error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
