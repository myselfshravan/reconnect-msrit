from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    data = {
        "url": "/sis",
        "method": "GET",
        "params": {
            "usn": "1MS18CS001",
            "dob": "2000-01-01",
            "endpoint": "newparents, oddparents, evenparents"
        },
        "description": "Get student data from SIS",
    }
    return jsonify(data), 200


@app.route('/test', methods=['GET'])
def test():
    data = {
        "courses": [
            {
                "CourseCode": 'CI71',
                "CourseName": 'Multicore Architecture and programming',
                "InternalScore": 41,
                "attendance": 87,
                "credit": 4,
            },
            {
                "CourseCode": 'CI72',
                "CourseName": 'Foundations of Computer Vision',
                "InternalScore": 37,
                "attendance": 86,
                "credit": 3,
            },
            {
                "CourseCode": 'CIL74',
                "CourseName": 'Containerization Laboratory',
                "InternalScore": 40,
                "attendance": 90,
                "credit": 1,
            },
            {
                "CourseCode": 'CIL75',
                "CourseName": 'Skill Enhancement Lab -Generative AI',
                "InternalScore": 46,
                "attendance": 86,
                "credit": 3,
            },
            {
                "CourseCode": 'CIE731',
                "CourseName": 'Information Retrieval',
                "InternalScore": 31,
                "attendance": 76,
                "credit": 3,
            },
            {
                "CourseCode": 'MEOE07',
                "CourseName": 'Product Design and Manufacturing',
                "InternalScore": 37,
                "attendance": 88,
                "credit": 3,
            },
        ],
        "academicHistory": {
            "cumulative": {
                "cgpa": "8.80",
                "creditsEarned": "126",
                "creditsToBeEarned": "34"
            },
            "semesters": [
                {
                    "cgpa": 0,
                    "creditsEarned": "20",
                    "creditsRegistered": "20",
                    "semester": "Feb / Mar 2022",
                    "sgpa": "8.75"
                },
                {
                    "cgpa": "8.77",
                    "creditsEarned": "16",
                    "creditsRegistered": "20",
                    "semester": "July 2022",
                    "sgpa": "7.05"
                },
                {
                    "cgpa": "8.59",
                    "creditsEarned": "21",
                    "creditsRegistered": "21",
                    "semester": "Jan 2023",
                    "sgpa": "8.28"
                },
                {
                    "cgpa": "8.72",
                    "creditsEarned": "22",
                    "creditsRegistered": "22",
                    "semester": "May/June 2023",
                    "sgpa": "9.04"
                },
                {
                    "cgpa": "8.68",
                    "creditsEarned": "4",
                    "creditsRegistered": "4",
                    "semester": "Supplementary Semester July / August 2023",
                    "sgpa": "8"
                },
                {
                    "cgpa": "8.69",
                    "creditsEarned": "21",
                    "creditsRegistered": "21",
                    "semester": "ODD - December 2023",
                    "sgpa": "8.71"
                },
                {
                    "cgpa": "8.80",
                    "creditsEarned": "22",
                    "creditsRegistered": "22",
                    "semester": "EVEN - May 2024",
                    "sgpa": "9.31"
                }
            ]
        },
        "cgpa": "8.80",
        "lastUpdated": '01/02/2025',
        "name": 'NISHA S',
        "usn": '1MS21CI035',
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

        result_url = f"{base_url}/index.php?option=com_history&task=getResult"
        result_response = session.get(result_url, timeout=10)
        cumulative_data = {}
        semesters = []

        if result_response.status_code == 200:
            result_soup = BeautifulSoup(result_response.text, "html.parser")

            # Parse the cumulative history cards (Credits Earned, Credits to be Earned, CGPA)
            cumulative_div = result_soup.find("div", class_="detail3")
            if cumulative_div:
                cards = cumulative_div.find_all("div", class_="uk-card")
                for card in cards:
                    header = card.find("h3").get_text(strip=True) if card.find("h3") else ""
                    value = card.find("p").get_text(strip=True) if card.find("p") else ""
                    if "Credits Earned" in header:
                        cumulative_data["creditsEarned"] = value
                    elif "Credits to be" in header:
                        cumulative_data["creditsToBeEarned"] = value
                    elif header == "CGPA":
                        cumulative_data["cgpa"] = value

            # Helper to extract a number (integer or float) from a text string
            def extract_number(text):
                match = re.search(r"([\d.]+)", text)
                return match.group(1) if match else None

            # Parse semester-wise results using the table captions
            # (each caption contains the semester name and spans with Credits Registered, Credits Earned, SGPA, and CGPA)
            captions = result_soup.find_all("caption")
            for cap in captions:
                # The first text node in the caption is assumed to be the semester name
                semester_name = cap.find(text=True, recursive=False)
                semester_name = semester_name.strip() if semester_name else ""
                registered = earned = sgpa = cgpa = None
                for span in cap.find_all("span"):
                    span_text = span.get_text(strip=True)
                    if "Credits Registered" in span_text:
                        registered = extract_number(span_text)
                    elif "Credits Earned" in span_text:
                        earned = extract_number(span_text)
                    elif "SGPA" in span_text:
                        sgpa = extract_number(span_text)
                    elif "CGPA" in span_text:
                        cgpa = extract_number(span_text)
                if semester_name:
                    semesters.append({
                        "semester": semester_name,
                        "creditsRegistered": registered,
                        "creditsEarned": earned,
                        "sgpa": sgpa,
                        "cgpa": cgpa,
                    })
        # -------------------------------
        # End additional academic history parsing
        # -------------------------------

        # Build final data structure
        data = {
            "name": student_name,
            "usn": student_id,
            "courses": courses,
            "lastUpdated": last_updated,
            "cgpa": cumulative_data.get("cgpa"),
            "academicHistory": {
                "cumulative": cumulative_data,
                "semesters": semesters
            }
        }

        return jsonify(data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network or request error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
