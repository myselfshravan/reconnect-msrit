from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from flask_cors import CORS
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    data = {
        "url": "/sis",
        "method": "GET",
        "params": {
            "usn": "1MS18CS001",
            "dob": "2000-01-01",
            "endpoint": "newparents"
        },
        "description": "Get student data from SIS",
    }
    return jsonify(data), 200


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


@app.route("/sis", methods=["GET"])
def get_student_data():
    usn = request.args.get("usn", "").strip()
    dob = request.args.get("dob", "").strip()
    endpoint = request.args.get("endpoint", "").strip()
    base_url = f"https://parents.msrit.edu/{endpoint}"

    if not usn or not dob:
        return jsonify({"error": "Missing usn or dob parameter"}), 400

    try:
        yyyy, mm, dd = dob.split("-")
    except ValueError:
        return jsonify({"error": "DOB must be in YYYY-MM-DD format"}), 400

    login_url = f"{base_url}/index.php"

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
            f"{base_url}/"
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

        try:
            student_id_divs = soup.find_all("div", class_="cn-stu-data1")
            student_id = student_id_divs[1].find("h2").text.strip()
        except (IndexError, AttributeError):
            return jsonify({"error": "Could not retrieve student ID. Possibly incorrect DOB/USN."}), 404

        script_tag = soup.find("script", string=lambda text: "columns" in text if text else False)
        if not script_tag:
            return jsonify({"error": "Could not find CIE marks script tag."}), 404

        script_text = script_tag.string
        pattern = r'\["([^"]+)",(\d+)\]'
        cie_marks = re.findall(pattern, script_text)
        cie_dict = {code: int(mark) for code, mark in cie_marks}

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

                cie_score = cie_dict.get(course_code, "N/A")

                courses.append({
                    "CourseCode": course_code,
                    "CourseName": course_name,
                    "InternalScore": cie_score,
                    "attendance": attendance,
                })

        credit_mapping = {}
        feedback_url = f"{base_url}/index.php?option=com_coursefeedback&controller=feedbackentry&task=feedback"
        feedback_response = session.get(feedback_url, timeout=10)
        if feedback_response.status_code == 200:
            feedback_soup = BeautifulSoup(feedback_response.text, "html.parser")
            feedback_table = feedback_soup.find("table")
            if feedback_table:
                tbody = feedback_table.find("tbody")
                if tbody:
                    for row in tbody.find_all("tr"):
                        cells = row.find_all("td")
                        if len(cells) < 4:
                            continue
                        course_code_fb = cells[1].text.strip()
                        a_tag = cells[3].find("a", href=True)
                        if not a_tag:
                            continue
                        feedback_link = a_tag["href"]
                        if not feedback_link.startswith("http"):
                            feedback_link = f"{base_url}/" + feedback_link

                        course_feedback_response = session.get(feedback_link, timeout=10)
                        if course_feedback_response.status_code == 200:
                            course_feedback_soup = BeautifulSoup(course_feedback_response.text, "html.parser")
                            credit_div = course_feedback_soup.find("div",
                                                                   style=lambda s: s and "font-size:35px" in s)
                            if credit_div:
                                credit_value = credit_div.text.strip()
                                credit_mapping[course_code_fb] = credit_value

        for course in courses:
            code = course.get("CourseCode")
            if code:
                credit = credit_mapping.get(code)
                if credit:
                    course["credit"] = int(float(credit))
                else:
                    course["credit"] = 0

        last_updated_el = soup.find("p", class_="cn-last-update")
        if last_updated_el:
            last_updated = last_updated_el.text.replace("Last Updated On: ", "").strip()
        else:
            last_updated = ""

        data = {
            "name": student_name,
            "usn": student_id,
            "courses": courses,
            "lastUpdated": last_updated
        }

        return jsonify(data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network or request error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
