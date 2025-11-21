# 🔐 Host Activity Monitoring & Incident Response Dashboard

A real-time host monitoring and incident response dashboard that collects and visualizes system metrics, detects anomalies, and generates incident reports using **FastAPI**, **React**, and **MongoDB/Elasticsearch**.

---

## 📖 Project Overview
The **Host Activity Monitoring & Incident Response Dashboard** provides real-time visibility into host activity, detects suspicious behavior, and supports effective response actions.  

Key metrics include **CPU usage, memory utilization, network activity, running processes, and system logs**.  
A lightweight **Python agent** collects these metrics and sends them to a **FastAPI backend**, which stores the data in **MongoDB/Elasticsearch**.  

A **React-based dashboard** visualizes the collected data with charts and tables, highlights anomalies, and provides structured incident reports (PDF/HTML).  
Response actions such as notifying admins, terminating suspicious processes, or isolating hosts will be integrated.  

By the end, the system will deliver a **secure, scalable, and interactive monitoring solution** for cybersecurity operations.  

---

## ✨ Features
- Monitor CPU, memory, network activity, processes, and logs  
- Real-time dashboard with filters (host, timeframe, activity type)  
- Rule-based incident detection and alerts  
- Automated PDF/HTML incident reports  
- Response actions: notify admin, kill process, isolate host  
- Authentication & role-based access control  

---

## 🛠 Tech Stack
- **Backend** → FastAPI  
- **Frontend** → React  
- **Database** → MongoDB / Elasticsearch  
- **Agent** → Python  

---

## 🗓 Roadmap
- **Week 1–2**: Planning & Setup  
- **Week 3–4**: Data Collection  
- **Week 5–6**: Monitoring Dashboard  
- **Week 7–8**: Incident Detection  
- **Week 9–10**: Reporting & Response  
- **Week 11–12**: Finalization & Security  

---

## ⚙️ Setup Instructions
# 🚀 Project Setup & Run Guide (Windows)

This guide explains how to start MongoDB, launch the FastAPI backend, run supporting scripts, and open the frontend dashboard on **Windows**.

---

## 📦 1. Start MongoDB Server

If MongoDB is installed as a **Windows service** (default):

```sh
net start MongoDB

📥 2. Install Dependencies
pip install -r requirements.txt

3. Start the FastAPI Server
uvicorn fastapi_app:app --reload --port 8000

🤖 4. Run the Agent Script
Open a new terminal and activate the venv again:
python agent.py

🖥️ 5. Run the Host Simulation Script
In another terminal:
python simulate_hosts.py

🌐 6. Open the Frontend Dashboard
start dashboard.html
