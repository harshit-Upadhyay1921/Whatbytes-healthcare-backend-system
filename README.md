# Healthcare Backend System

A RESTful healthcare backend built with **Django, Django REST Framework (DRF), and PostgreSQL**. The application provides JWT-based authentication, patient and doctor management, and patient-doctor assignments.

## Features

- **JWT Authentication:** User registration and login using SimpleJWT.
- **Patient Management:** Create, retrieve, update, and delete patient records.
- **Doctor Management:** Create, retrieve, update, and delete doctor records.
- **Patient-Doctor Mapping:** Assign doctors to patients, retrieve assignments, and remove mappings.
- **Ownership Validation:** Restrict patient access to the user who created the record.
- **Duplicate Prevention:** Enforce uniqueness of patient-doctor assignments.
- **Input Validation:** Validate incoming requests and return appropriate API errors.
- **PostgreSQL:** Store application data in a relational database.
- **Environment Configuration:** Keep sensitive settings in environment variables.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- SimpleJWT
- psycopg2
- python-dotenv (if configured in the project)

## API Endpoints

All endpoints are prefixed with `/api/`.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Log in and obtain JWT tokens |

### Patients

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List the authenticated user's patients |
| GET | `/api/patients/<id>/` | Retrieve a patient |
| PUT | `/api/patients/<id>/` | Update a patient |
| DELETE | `/api/patients/<id>/` | Delete a patient |

### Doctors

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List doctors |
| GET | `/api/doctors/<id>/` | Retrieve a doctor |
| PUT | `/api/doctors/<id>/` | Update a doctor |
| DELETE | `/api/doctors/<id>/` | Delete a doctor |

### Patient-Doctor Mappings

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List mappings |
| GET | `/api/mappings/<patient_id>/` | Retrieve doctors assigned to a patient |
| DELETE | `/api/mappings/<id>/` | Remove a mapping by its ID |

**Note:** Confirm the mapping deletion URL against the implementation before submission. If the implemented route uses `/api/mappings/<id>/delete/`, document that exact route instead.

## Authentication

Protected endpoints require a valid JWT access token.

Include the token in the request header:

```http
Authorization: Bearer <access_token>
```

Obtain the token by logging in through `/api/auth/login/`.

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version supported by the project dependencies
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/harshit-Upadhyay1921/Whatbytes-healthcare-backend-system.git
cd Whatbytes-healthcare-backend-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Configure the variables required by `healthcare/settings.py`, including your Django secret key and PostgreSQL connection details.

Example:

```env
SECRET_KEY=your-secret-key
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your-postgresql-password
DB_HOST=localhost
DB_PORT=5432
```

Use the exact variable names expected by the project settings. Never commit your actual `.env` file or database credentials.

### 4. Create the database

Create a PostgreSQL database named `healthcare_db`:

```sql
CREATE DATABASE healthcare_db;
```

Ensure PostgreSQL is running and the configured database user has the required permissions.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API server will be available at:

`http://127.0.0.1:8000/`

## API Verification

The endpoints can be verified using Postman or another REST API client.

Verify the following workflows:

- Register a user and log in to obtain JWT tokens.
- Create, retrieve, update, and delete patient records.
- Confirm that users cannot access or modify another user's patients.
- Create and manage doctor records.
- Assign doctors to patients and retrieve their mappings.
- Confirm that duplicate patient-doctor assignments are rejected.
- Remove mappings and verify that the deletion endpoint behaves correctly.

## Security Considerations

- Passwords are handled using Django's password hashing.
- JWT authentication protects restricted endpoints.
- Environment variables are used for sensitive configuration.
- Patient ownership is enforced to prevent unauthorized access.
- Database constraints prevent duplicate patient-doctor assignments.

## Author

**Harshit Upadhyay**

GitHub: [harshit-Upadhyay1921](https://github.com/harshit-Upadhyay1921)

---

Developed as part of the Healthcare Backend Assignment.
