# Reconnect MSRIT API (Parent Portal API)

This project provides a serverless Flask API deployed on Vercel to help MSRIT students access their academic information. It fetches data from the college's portals and offers features like viewing CIE marks, attendance, academic history, and predicted SGPA based on different performance scenarios.

## Features ✨

-   **Fetch Student Data:** Retrieves student details, CIE marks, and attendance from the MSRIT student portal.
-   **Academic History:** Provides a history of semester-wise SGPA and CGPA, along with cumulative credits information.
-   **SGPA Prediction:** Predicts the Semester Grade Point Average (SGPA) under three scenarios:
    -   **At Least:** A conservative prediction.
    -   **Most Likely:** An expected prediction, influenced by a consistent offset based on past SGPA.
    -   **Max Effort:** A best-case scenario prediction.
-   **Exam Results:** Fetches recent semester exam results (SGPA, CGPA, semester name).
-   **CORS Enabled:** Allows cross-origin requests for wider accessibility.
-   **Serverless Deployment:** Hosted on Vercel for scalability and ease of use.

## Endpoints ⚙️

-   `/`: Returns a basic description of the `/sis` endpoint.
-   `/test`: Returns sample student data in JSON format for testing purposes.
-   `/health`: Returns a JSON response indicating the API is running.
-   `/status`: Accepts POST requests and echoes back the provided data and status.
-   `/sis`: (GET) Fetches comprehensive student data from the MSRIT parent portal. Requires `usn`, `dob`, and `endpoint` as query parameters. The `endpoint` can be one of `newparents`, `oddparents`, or `evenparents`. An optional `fast=true` parameter can skip fetching course credits from the feedback portal.
    -   **Parameters:**
        -   `usn`: University Seat Number of the student (e.g., `1MS18CS001`).
        -   `dob`: Date of Birth of the student in `YYYY-MM-DD` format (e.g., `2000-01-01`).
        -   `endpoint`: The specific parent portal endpoint to use (`newparents`, `oddparents`, `evenparents`).
        -   `fast` (optional): If set to `true`, skips fetching detailed course credits, potentially speeding up the response. Defaults to `false`.
-   `/exam`: (GET) Fetches the latest exam results (SGPA, CGPA, semester) for a given USN from the MSRIT exam portal. Requires `usn` as a query parameter.
    -   **Parameter:**
        -   `usn`: University Seat Number of the student.

## How to Use 🚀

1.  **Deployment:** This API is designed to be deployed on Vercel. The `vercel.json` file configures the rewrites to direct all requests to the `api/index.py` file.
2.  **Prerequisites:** Ensure you have Python installed if you want to run it locally for development (though it's intended for serverless deployment). The `requirements.txt` file (non-text in this case, likely empty or standard Vercel dependencies) lists any Python dependencies.
3.  **Making Requests:** Use any HTTP client (like `curl`, `Postman`, or a web browser for GET requests) to interact with the API endpoints.

    **Example `/sis` request:**
    ```bash
    curl "https://reconnect-msrit.vercel.app/sis?usn=1MS18CS001&dob=2000-01-01&endpoint=newparents"
    ```

    **Example `/exam` request:**
    ```bash
    curl "https://reconnect-msrit.vercel.app/exam?usn=1MS18CS001"
    ```

## Files Included 📂

-   `README.md`: This file, providing an overview of the project.
-   `requirements.txt`: Lists Python dependencies (likely empty or managed by Vercel).
-   `vercel.json`: Configuration file for Vercel deployment, defining rewrites and function settings.
-   `api/index.py`: The main Flask application code containing the API endpoints and logic.

## Tech Stack 🛠️

-   Python
-   Flask: A micro web framework for Python.
-   Requests: For making HTTP requests to fetch data from MSRIT portals.
-   Beautiful Soup 4 (bs4): For parsing HTML content.
-   re: For regular expressions, used for data extraction.
-   Flask-CORS: For handling Cross-Origin Resource Sharing.
-   hashlib: For generating consistent offsets based on SGPA.
-   Vercel: For serverless deployment and hosting.

## Important Notes ⚠️

-   This API relies on the structure and availability of the MSRIT student and parent portals. Any changes to these portals might break the API.
-   The SGPA prediction logic is based on internal scores and applies different multipliers for various scenarios. The accuracy of these predictions may vary.
-   The `/sis` endpoint requires student USN and DOB for authentication against the parent portal. Ensure these are provided correctly.
-   The `fast` parameter in the `/sis` endpoint can be used to speed up data retrieval by skipping the fetching of course credits from the feedback portal, which might be slower or less reliable. If skipped, course credits might default to 0.

## Author 👤

[myselfshravan](https://github.com/myselfshravan)

Feel free to contribute to this project or report any issues.
