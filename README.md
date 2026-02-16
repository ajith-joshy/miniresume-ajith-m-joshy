Mini Resume Management API:

This is a Mini Resume Collector REST API built using Django and Django REST Framework.

The application allows:

-Uploading resumes (PDF/DOC/DOCX)

-Storing candidate metadata in memory

-Filtering candidates by skill, experience, and graduation year

-Retrieving and deleting candidates

-Health check endpoint for service monitoring

-No database is used. Data is stored in memory during runtime.

#Python Version - Python 3.11.9

#Installation steps

1️) Clone the Repository

git clone https://github.com/your-username/miniresume-ajith-m-joshy.git

cd miniresume-ajith-m-joshy

2️) Create Virtual Environment

python -m venv venv 

3)Activate Virtual Environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

4️) Install Dependencies


pip install -r requirements.txt

#Running the Application 

1) python manage.py runserver

The application will start at:
http://127.0.0.1:8000/ 

2) Health Check Endpoint

This endpoint verifies that the application is running properly.

Endpoint:
GET /health

Example Response:

{

    "status": "ok"

}

Status Code:
200 OK

3) Upload Candidate (Create)

Endpoint:
POST /candidates/

Content Type:
multipart/form-data

Required Fields:

full_name

dob (Format: YYYY-MM-DD)

contact_number

contact_address

education_qualification

graduation_year

years_of_experience

skill_set (comma separated values)

resume (PDF/DOC/DOCX file)

Example Request (Form Data):

full_name = Ajith Joshy
dob = 2003-02-25
contact_number = 8281882309
contact_address = ABC, Kerala
education_qualification = B Tech in Computer Science
graduation_year = 2025
years_of_experience = 1
skill_set = python,django,react
resume = <file upload>

Example Response:
{
    "id": 1,
    "full_name": "Ajith Joshy",
    "dob": "2003-02-25",
    "contact_number": "8281882309",
    "contact_address": "ABC House, Kerala",
    "education_qualification": "B Tech in Computer Science",
    "graduation_year": 2025,
    "years_of_experience": 1,
    "skill_set": [
            "python",
            "django",
            "react"
    ],
    "resume": "uploads/Resume.pdf"
}

Status Code:
201 Created

4) List Candidates

Endpoint:
GET /candidates/

Example Response:

[
    {
        "id": 1,
        "full_name": "Ajith Joshy",
        "graduation_year": 2025,
        "years_of_experience": 1,
        "skill_set": [
            "python",
            "django",
            "react"
        ],
        .....
    }
]

5) Filter Candidates

You can filter using query parameters.

Filter by Skill:
GET /candidates/?skill=python

Filter by Minimum Experience:
GET /candidates/?experience=2

Filter by Graduation Year:
GET /candidates/?graduation_year=2025

Multiple Filters Together:
GET /candidates/?skill=python&experience=1

If no candidates match:

{
    "message": "No candidates found"
}

6) Retrieve Candidate by ID

Endpoint:
GET /candidates/{id}/

Example:
GET /candidates/1/

If ID not found:
{
    "error": "No candidate found"
}
Status Code:
404 Not Found

7) Delete Candidate

Endpoint:
DELETE /candidates/{id}/

Example:
DELETE /candidates/1/

Response:
{
    "message": "Deleted successfully"
}
