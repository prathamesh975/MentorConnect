# MentorConnect – Student Mentorship Management Portal

MentorConnect is a web-based platform that allows students to discover mentors, request mentorship, and track the status of their mentorship requests.

## Features

- Server-side mentor listing using Flask and Jinja2
- Mentorship request form with input validation
- Mentorship request status tracking
- JSON API for mentors and mentorship requests
- Health check endpoint
- Automated testing using pytest
- Code linting using flake8
- Docker containerization
- GitHub Actions CI/CD pipeline
- Deployment through Render

## Technology Stack

- Python 3.12
- Flask
- Jinja2
- pytest
- flake8
- Docker
- GitHub Actions
- Render
- Git/GitHub

## Application Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Home page |
| `/mentors` | GET | Display mentors |
| `/request` | GET/POST | Submit mentorship request |
| `/requests` | GET | View mentorship requests |
| `/api/mentors` | GET | Mentor JSON API |
| `/api/requests` | GET | Request JSON API |
| `/health` | GET | Application health check |

## Running Locally

Create and activate a virtual environment:

```bash
python -m venv .venv