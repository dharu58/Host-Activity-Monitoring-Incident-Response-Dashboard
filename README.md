# 🔐 Host Activity Monitoring & Incident Response Dashboard

A real-time host monitoring and incident analytics system powered by:

- **Python Monitoring Agent (psutil)**
- **FastAPI Backend (MongoDB storage)**
- **HTML + JavaScript Dashboard (Chart.js)**

The system continuously collects CPU, memory, disk, network, I/O, and process-level data from hosts, stores them in MongoDB, and visualizes them in a real-time dashboard.

---

## 🚀 Features

- Real-time system metrics (CPU, RAM, Disk, Network)
- Live Chart.js graphs (auto-refreshing)
- Multi-host monitoring using hostname identifiers
- Lightweight Python agent
- FastAPI backend with MongoDB storage
- Historical + Latest metrics APIs
- Pure JS dashboard (no frameworks needed)
- Host simulation using `simulate_hosts.py`

---


---

## 📁 Project Files

bash
Copy code
Host-Activity-Monitoring-Incident-Response-Dashboard/
│
├── agent.py               # Host monitoring agent
├── simulate_hosts.py      # Multi-host simulator
├── fastapi_app.py         # FastAPI backend + MongoDB logic
├── dashboard.html         # Real-time dashboard UI
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container for backend
├── .env.example           # MongoDB connection template
└── README.md              # Documentation
---

# ⚙️ Tech Stack

### Backend  
- FastAPI  
- Uvicorn  
- Motor (Async MongoDB Driver)

### Monitoring Agent  
- Python  
- psutil  
- requests  

### Frontend  
- HTML  
- JavaScript  
- Chart.js  
- date-fns  

### Database  
- MongoDB  

---

# ▶️ Setup Instructions

## **1. Install Dependencies**
pip install -r requirements.txt


## **2. Start MongoDB**


mongod


## **3. Start FastAPI Backend**


uvicorn fastapi_app:app --reload --port 8000


## **4. Run Monitoring Agent**


python agent.py


Simulate multiple hosts:


python simulate_hosts.py


## **5. Start Dashboard**
Open:


dashboard.html

in your browser.

---

# 🐳 Docker Deployment

Your repository includes a **Dockerfile** for running the FastAPI backend inside a container.

## **1. Build the Docker Image**


docker build -t host-monitor-backend .


## **2. Run the Container**


docker run -d -p 8000:8000 --name host-monitor host-monitor-backend


Backend will now run at:


http://localhost:8000


## **3. Connect Dashboard and Agent to Docker**
- The **agent** will POST metrics to the container’s exposed port.
- The **dashboard** will fetch data from the same API URL.
