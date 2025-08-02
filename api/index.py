import math
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from flask_cors import CORS
import random
import hashlib
import json

app = Flask(__name__)
CORS(app)

# Default endpoint configuration
DEFAULT_ENDPOINT = "newparentseven"


@app.route('/', methods=['GET'])
def home():
    data = {
        "endpoints": {
            "/sis": {
                "method": "GET",
                "params": {
                    "usn": "1MS18CS001",
                    "dob": "2000-01-01",
                    "endpoint": "newparents, oddparents, evenparents, newparentseven, newparentsodd, default"
                },
                "description": "Get student data from SIS"
            },
            "/endpoints": {
                "method": "GET",
                "params": {},
                "description": "Get list of active endpoints from https://parents.msrit.edu/webfiles/"
            },
            "/exam": {
                "method": "GET",
                "params": {
                    "usn": "1MS18CS001"
                },
                "description": "Get exam results for a student"
            },
            "/health": {
                "method": "GET",
                "params": {},
                "description": "Check API health status"
            },
            "/test": {
                "method": "GET",
                "params": {},
                "description": "Get sample test data"
            }
        }
    }
    return jsonify(data), 200


@app.route('/test', methods=['GET'])
def test():
    data = {
        "courses": [
            {
                "CourseCode": "CI71",
                "CourseName": "Multicore Architecture and programming",
                "InternalScore": 48,
                "attendance": 88,
                "credit": 4
            },
            {
                "CourseCode": "CI72",
                "CourseName": "Foundations of Computer Vision",
                "InternalScore": 47,
                "attendance": 86,
                "credit": 3
            },
            {
                "CourseCode": "CIL74",
                "CourseName": "Containerization Laboratory",
                "InternalScore": 46,
                "attendance": 90,
                "credit": 1
            },
            {
                "CourseCode": "CIL75",
                "CourseName": "Skill Enhancement Lab -Generative AI",
                "InternalScore": 45,
                "attendance": 86,
                "credit": 3
            },
            {
                "CourseCode": "CIE731",
                "CourseName": "Information Retrieval",
                "InternalScore": 44,
                "attendance": 76,
                "credit": 3
            },
            {
                "CourseCode": "ETOE02",
                "CourseName": "Wireless Sensor Networks",
                "InternalScore": 43,
                "attendance": 78,
                "credit": 3
            }
        ],
        "academicHistory": {
            "cumulative": {
                "cgpa": "9.99",
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
        "predictions": {
            "atleast": {
                "course_details": [
                    {
                        "CourseCode": "CI71",
                        "CourseName": "Multicore Architecture and programming",
                        "Credit": 4,
                        "GradePoints": 9,
                        "InternalScore_out_of_50": 48,
                        "LetterGrade": "A+",
                        "PredictedFinal_out_of_100": 72.6,
                        "Total_out_of_100": 84.3
                    },
                    {
                        "CourseCode": "CI72",
                        "CourseName": "Foundations of Computer Vision",
                        "Credit": 3,
                        "GradePoints": 7,
                        "InternalScore_out_of_50": 37,
                        "LetterGrade": "B+",
                        "PredictedFinal_out_of_100": 62.6,
                        "Total_out_of_100": 68.3
                    },
                    {
                        "CourseCode": "CIL74",
                        "CourseName": "Containerization Laboratory",
                        "Credit": 1,
                        "GradePoints": 9,
                        "InternalScore_out_of_50": 50,
                        "LetterGrade": "A+",
                        "PredictedFinal_out_of_100": 73.5,
                        "Total_out_of_100": 86.7
                    },
                    {
                        "CourseCode": "CIL75",
                        "CourseName": "Skill Enhancement Lab -Generative AI",
                        "Credit": 3,
                        "GradePoints": 9,
                        "InternalScore_out_of_50": 48,
                        "LetterGrade": "A+",
                        "PredictedFinal_out_of_100": 72.6,
                        "Total_out_of_100": 84.3
                    },
                    {
                        "CourseCode": "CIE731",
                        "CourseName": "Information Retrieval",
                        "Credit": 3,
                        "GradePoints": 6,
                        "InternalScore_out_of_50": 31,
                        "LetterGrade": "B",
                        "PredictedFinal_out_of_100": 52.7,
                        "Total_out_of_100": 57.3
                    },
                    {
                        "CourseCode": "ETOE02",
                        "CourseName": "Wireless Sensor Networks",
                        "Credit": 3,
                        "GradePoints": 8,
                        "InternalScore_out_of_50": 40,
                        "LetterGrade": "A",
                        "PredictedFinal_out_of_100": 66.5,
                        "Total_out_of_100": 73.2
                    }
                ],
                "predicted_sgpa": 7.94
            },
            "maxeffort": {
                "course_details": [
                    {
                        "CourseCode": "CI71",
                        "CourseName": "Multicore Architecture and programming",
                        "Credit": 4,
                        "GradePoints": 10,
                        "InternalScore_out_of_50": 48,
                        "LetterGrade": "O",
                        "PredictedFinal_out_of_100": 98.3,
                        "Total_out_of_100": 97.1
                    },
                    {
                        "CourseCode": "CI72",
                        "CourseName": "Foundations of Computer Vision",
                        "Credit": 3,
                        "GradePoints": 8,
                        "InternalScore_out_of_50": 37,
                        "LetterGrade": "A",
                        "PredictedFinal_out_of_100": 84.7,
                        "Total_out_of_100": 79.4
                    },
                    {
                        "CourseCode": "CIL74",
                        "CourseName": "Containerization Laboratory",
                        "Credit": 1,
                        "GradePoints": 10,
                        "InternalScore_out_of_50": 50,
                        "LetterGrade": "O",
                        "PredictedFinal_out_of_100": 99.4,
                        "Total_out_of_100": 99.7
                    },
                    {
                        "CourseCode": "CIL75",
                        "CourseName": "Skill Enhancement Lab -Generative AI",
                        "Credit": 3,
                        "GradePoints": 10,
                        "InternalScore_out_of_50": 48,
                        "LetterGrade": "O",
                        "PredictedFinal_out_of_100": 98.3,
                        "Total_out_of_100": 97.1
                    },
                    {
                        "CourseCode": "CIE731",
                        "CourseName": "Information Retrieval",
                        "Credit": 3,
                        "GradePoints": 7,
                        "InternalScore_out_of_50": 31,
                        "LetterGrade": "B+",
                        "PredictedFinal_out_of_100": 71.3,
                        "Total_out_of_100": 66.7
                    },
                    {
                        "CourseCode": "ETOE02",
                        "CourseName": "Wireless Sensor Networks",
                        "Credit": 3,
                        "GradePoints": 9,
                        "InternalScore_out_of_50": 40,
                        "LetterGrade": "A+",
                        "PredictedFinal_out_of_100": 89.9,
                        "Total_out_of_100": 85
                    }
                ],
                "predicted_sgpa": 8.94
            },
            "mostlikely": {
                "course_details": [
                    {
                        "CourseCode": "CI71",
                        "CourseName": "Multicore Architecture and programming",
                        "Credit": 4,
                        "GradePoints": 10,
                        "InternalScore_out_of_50": 48,
                        "LetterGrade": "O",
                        "PredictedFinal_out_of_100": 85.5,
                        "Total_out_of_100": 90.7
                    },
                    {
                        "CourseCode": "CI72",
                        "CourseName": "Foundations of Computer Vision",
                        "Credit": 3,
                        "GradePoints": 8,
                        "InternalScore_out_of_50": 37,
                        "LetterGrade": "A",
                        "PredictedFinal_out_of_100": 73.7,
                        "Total_out_of_100": 73.8
                    },
                    {
                        "CourseCode": "CIL74",
                        "CourseName": "Containerization Laboratory",
                        "Credit": 1,
                        "GradePoints": 10,
                        "InternalScore_out_of_50": 50,
                        "LetterGrade": "O",
                        "PredictedFinal_out_of_100": 86.5,
                        "Total_out_of_100": 93.2
                    },
                    {
                        "CourseCode": "CIL75",
                        "CourseName": "Skill Enhancement Lab -Generative AI",
                        "Credit": 3,
                        "GradePoints": 10,
                        "InternalScore_out_of_50": 48,
                        "LetterGrade": "O",
                        "PredictedFinal_out_of_100": 85.5,
                        "Total_out_of_100": 90.7
                    },
                    {
                        "CourseCode": "CIE731",
                        "CourseName": "Information Retrieval",
                        "Credit": 3,
                        "GradePoints": 7,
                        "InternalScore_out_of_50": 31,
                        "LetterGrade": "B+",
                        "PredictedFinal_out_of_100": 62,
                        "Total_out_of_100": 62
                    },
                    {
                        "CourseCode": "ETOE02",
                        "CourseName": "Wireless Sensor Networks",
                        "Credit": 3,
                        "GradePoints": 8,
                        "InternalScore_out_of_50": 40,
                        "LetterGrade": "A",
                        "PredictedFinal_out_of_100": 78.2,
                        "Total_out_of_100": 79.1
                    }
                ],
                "predicted_sgpa": 8.76
            }
        },
        "cgpa": "9.99",
        "lastUpdated": '11/02/2025',
        "name": 'TEST USER',
        "usn": '1MS21AB001',
        "fetched_sgpa": "8.81",
        "fetched_cgpa": "8.67",
        "semester": "Semester 7"
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


def predict_final_score(internal_score, scenario="mostlikely"):
    """
    Predict the final (out of 100) based on:
      - internal_score (out of 50),
      - scenario multipliers,
      - exponential decay above a base cap (70).
    """
    scenario_multipliers = {
        "atleast": 0.85,  # Conservative
        "mostlikely": 1.0,  # Expected
        "maxeffort": 1.15  # Best-case
    }

    # Base projection: double the internal (since internal is out of 50)
    base_projection = internal_score * 2

    # If base_projection > 70, apply exponential decay on the "excess".
    if base_projection > 70:
        excess = base_projection - 70
        scaled_excess = excess * math.exp(-excess / 50.0)  # exponential decay
        base_projection = 70 + scaled_excess

    # Multiply by scenario-based factor
    final_projection = base_projection * scenario_multipliers.get(scenario, 1.0)
    # Ensure final doesn't exceed 100
    return min(final_projection, 100.0)


def calculate_total_score(internal_score, predicted_final):
    """
    Convert internal (out of 50) + final (out of 100) → total out of 100.
    We do this by: internal_score + (predicted_final / 2).
    """
    return internal_score + (predicted_final / 2.0)


def letter_grade_from_100(score_out_of_100):
    """
    Given a score out of 100, assign a letter grade.
    Adjust thresholds if you prefer different cutoffs.
    """
    thresholds = [
        ("O", 90),
        ("A+", 80),
        ("A", 70),
        ("B+", 60),
        ("B", 55),
        ("C", 50),
        ("P", 40)
    ]
    for grade, cutoff in thresholds:
        if score_out_of_100 >= cutoff:
            return grade
    return "F"


def letter_grade_to_point(letter):
    """
    Map each letter grade to numeric grade–points.
    """
    mapping = {
        "O": 10,
        "A+": 9,
        "A": 8,
        "B+": 7,
        "B": 6,
        "C": 5,
        "P": 4,
        "F": 0
    }
    return mapping.get(letter, 0)


def predict_sgpa(data):
    """
    Incorporate the new final-exam prediction logic into an SGPA calculation
    across three scenarios: 'atleast', 'mostlikely', 'maxeffort'.

    Steps for each course & scenario:
      1. Predict final exam out of 100 (via predict_final_score).
      2. Compute total out of 100 (internal + final/2).
      3. Assign a letter grade (out of 100).
      4. Convert to grade-points.
      5. Multiply by course credit and accumulate.

    Finally, SGPA = ( sum(grade_point * credit) ) / ( sum of credits ).
    """
    scenarios = ["atleast", "mostlikely", "maxeffort"]
    courses = data.get("courses", [])

    # Safeguard: sum up the total credits
    total_credits = sum(float(course.get("credit", 0)) for course in courses)
    if total_credits == 0:
        return {
            scenario: {"predicted_sgpa": 0.0, "course_details": []}
            for scenario in scenarios
        }

    results = {}
    for scenario in scenarios:
        scenario_total_gp = 0.0
        course_details = []
        for course in courses:
            course_code = course.get("CourseCode", "")
            course_name = course.get("CourseName", "")
            credit = float(course.get("credit", 0))
            internal_score = course.get("InternalScore", 0)
            if internal_score == "N/A":
                internal_score = 0
            internal_score = float(internal_score)
            predicted_final = predict_final_score(internal_score, scenario)
            total_score_100 = calculate_total_score(internal_score, predicted_final)
            letter_grade = letter_grade_from_100(total_score_100)
            grade_points = letter_grade_to_point(letter_grade)
            scenario_total_gp += (grade_points * credit)

            course_details.append({
                "CourseCode": course_code,
                "CourseName": course_name,
                "InternalScore_out_of_50": internal_score,
                "PredictedFinal_out_of_100": round(predicted_final, 1),
                "Total_out_of_100": round(total_score_100, 1),
                "LetterGrade": letter_grade,
                "GradePoints": grade_points,
                "Credit": credit
            })

        scenario_sgpa = scenario_total_gp / total_credits
        results[scenario] = {
            "predicted_sgpa": round(scenario_sgpa, 2),
            "course_details": course_details
        }

    return results


def fetch_exam_results(usn):
    BASE_URL = "https://exam.msrit.edu/"
    url = f"{BASE_URL}"
    payload = {
        "usn": usn.upper(),
        "osolCatchaTxt": "",
        "osolCatchaTxtInst": "0",
        "option": "com_examresult",
        "task": "getResult",
    }
    year = usn[3:5]
    if year != "22":
        payload["examId"] = 57

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.45 Safari/537.36"
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Validate if result exists
        try:
            name = soup.find_all("h3")[0].text.strip()
            sgpa = soup.find_all("p")[3].text.strip()
            cgpa = soup.find_all("p")[4].text.strip()
            sem = soup.find("p").text.split(",")[-1].strip()

            return {"sgpa": sgpa, "cgpa": cgpa, "semester": sem, "name": name}
        except (IndexError, AttributeError):
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching exam results: {e}")
        return None


@app.route("/sis", methods=["GET"])
def get_student_data():
    usn = request.args.get("usn", "").strip()
    dob = request.args.get("dob", "").strip()
    endpoint = request.args.get("endpoint", "").strip()

    # Handle default endpoint
    if endpoint.lower() == "default":
        endpoint = DEFAULT_ENDPOINT

    base_url = f"https://parents.msrit.edu/{endpoint}"
    fast = request.args.get("fast", "false").lower() == "true"

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

    # Disable SSL verification warnings since we're using verify=False
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        login_response = session.post(login_url, data=login_data, timeout=10, verify=False)
        if login_response.status_code != 200:
            return jsonify({"error": "Login failed. Check credentials or site availability."}), 500

        dashboard_url = (
            f"{base_url}/"
            "index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard"
        )
        dashboard_response = session.get(dashboard_url, timeout=10, verify=False)
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
        if not fast:
            feedback_url = f"{base_url}/index.php?option=com_coursefeedback&controller=feedbackentry&task=feedback"
            feedback_response = session.get(feedback_url, timeout=10, verify=False)
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

                            course_feedback_response = session.get(feedback_link, timeout=10, verify=False)
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
        result_response = session.get(result_url, timeout=10, verify=False)
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

            def extract_number(text):
                match = re.search(r"([\d.]+)", text)
                return match.group(1) if match else None

            captions = result_soup.find_all("caption")
            for cap in captions:
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
        # Start the prediction
        # -------------------------------

        # Predict SGPA for three scenarios
        prediction_data = {
            "courses": courses
        }
        exam_result = fetch_exam_results(usn)
        fetched_sgpa = exam_result.get("sgpa") if exam_result else "N/A"
        prediction_results = predict_sgpa(prediction_data)
        fetched_cgpa = exam_result.get("cgpa") if exam_result else "N/A"

        # Calculate current semester based on academic history
        # Count regular semesters (exclude Supplementary and Back-Log)
        regular_semesters = [
            sem for sem in semesters
            if "Supplementary" not in sem.get("semester", "")
               and "Back-Log" not in sem.get("semester", "")
        ]
        current_semester_num = len(regular_semesters) + 1
        semester = f"Semester {current_semester_num}"

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
            },
            "predictions": prediction_results,
            "fetched_sgpa": fetched_sgpa,
            "fetched_cgpa": fetched_cgpa,
            "semester": semester
        }

        return jsonify(data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network or request error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/exam', methods=['GET'])
def get_exam_results():
    usn = request.args.get("usn", "").strip()
    if not usn:
        return jsonify({"error": "Missing usn parameter"}), 400

    result = fetch_exam_results(usn)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to fetch exam results"}), 500


@app.route('/endpoints', methods=['GET'])
def get_active_endpoints():
    """
    Fetch the list of active endpoints from https://parents.msrit.edu/webfiles/
    """
    try:
        url = "https://parents.msrit.edu/webfiles/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/96.0.4664.45 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        endpoints = []
        cards = soup.find_all("div", class_=lambda x: x and "uk-card" in x and "uk-card-default" in x)
        for card in cards:
            try:
                title_element = card.find("h2", class_="uk-card-title")
                if not title_element:
                    continue
                title = title_element.text.strip()
                footer = card.find("div", class_="uk-card-footer")
                if not footer:
                    continue
                link_element = footer.find("a", href=True)
                if not link_element:
                    continue

                href = link_element.get("href", "")
                endpoint_name = href.replace("../", "").rstrip("/")
                if endpoint_name:
                    endpoints.append({
                        "name": endpoint_name,
                        "title": title,
                        "url": href
                    })

            except Exception as e:
                print(f"Error parsing card: {e}")
                continue

        from datetime import datetime
        return jsonify({
            "active_endpoints": endpoints,
            "count": len(endpoints),
            "source_url": url,
            "fetched_at": datetime.now().isoformat(),
            "current": DEFAULT_ENDPOINT
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Failed to fetch endpoints from source: {str(e)}",
            "source_url": "https://parents.msrit.edu/webfiles"
        }), 502

    except Exception as e:
        return jsonify({
            "error": f"An error occurred while processing endpoints: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
