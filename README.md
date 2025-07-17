# Alnafi Web Project 🚀

This is a Flask-based web application developed as part of the Al Nafi Diploma program. It is containerized using Docker for easy deployment and portability.

---

## 🔧 Technologies Used
- Python 3
- Flask
- HTML/CSS
- Jinja2 templates
- MySQL (Dockerized)
- Docker & Docker Compose

---

## 🚀 How to Run Locally (with Docker)

```bash
# Clone the repository
git clone https://github.com/NaveedIqbal87/alnafi_web.git
cd alnafi_web

# Run the app with Docker Compose
docker compose -f docker-compose_mysql_flask.yml up --build

