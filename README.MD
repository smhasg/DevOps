GPU Monitor Service

Production-ready NVIDIA GPU monitoring service for Linux servers.

This project continuously collects GPU metrics using NVIDIA's nvidia-smi utility and stores the data inside a SQL database for monitoring, analytics, infrastructure observability, and AI cluster management.

Designed for:

AI/ML servers
Multi-GPU workstations
Training clusters
Deep learning environments
CUDA infrastructure
GPU resource monitoring
Linux production environments

Unlike simple shell scripts, this project is designed to behave like a lightweight infrastructure monitoring service that can run continuously in the background using systemd.

Why This Project Exists

When working with machine learning infrastructure, GPU visibility becomes critical.

On AI servers, especially systems shared between multiple users or running long training jobs, it is important to continuously monitor:

GPU temperature
VRAM usage
GPU utilization
idle vs active GPUs
thermal pressure
hardware load patterns

While nvidia-smi provides this information interactively, it does not persist metrics historically.

This project solves that problem by:

collecting GPU statistics automatically
parsing and structuring the output
saving metrics into SQL
enabling historical analysis and dashboard integration

The collected data can later be integrated with:

Grafana
Prometheus
monitoring dashboards
alerting systems
scheduling systems
anomaly detection pipelines
Features
GPU Monitoring

Continuously monitors all NVIDIA GPUs installed on the system.

Temperature Tracking

Reads GPU thermal data in real time.

Memory Usage Tracking

Collects:

used VRAM
total VRAM
memory consumption patterns
GPU Utilization Monitoring

Tracks GPU compute usage percentage to identify:

active workloads
idle GPUs
overloaded devices
SQL Storage

Stores metrics inside a SQL database for:

historical analysis
reporting
visualization
infrastructure analytics
Linux Service Integration

Runs as a persistent Linux service using systemd.

Automatic Restart

If the process crashes, systemd automatically restarts it.

Lightweight Design

Minimal resource consumption suitable for production environments.

Architecture Overview

The service follows a simple monitoring pipeline:

NVIDIA GPU
     │
     ▼
nvidia-smi
     │
     ▼
Python Monitoring Service
     │
     ▼
Metric Parser
     │
     ▼
SQL Database
     │
     ▼
Dashboards / Analytics / Monitoring
How The Monitoring Works

The application periodically executes the following NVIDIA command:

nvidia-smi --query-gpu=index,name,temperature.gpu,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

This command returns structured information for each available GPU.

Example output:

0, NVIDIA RTX 4090, 52, 2048, 24564, 35
1, NVIDIA RTX 4090, 47, 0, 24564, 0

The Python service parses the output and extracts:

Metric	Description
GPU Index	GPU identifier
GPU Name	Hardware model
Temperature	GPU temperature in Celsius
Memory Used	Currently allocated VRAM
Memory Total	Total available VRAM
GPU Utilization	GPU usage percentage

Each monitoring cycle inserts a new record into the SQL database.

This creates a continuous historical timeline of GPU activity.

Project Structure
gpu-monitor/
├── app.py
├── config.txt
├── requirements.txt
├── gpu-monitor.service
└── README.md
File Descriptions
app.py

Main monitoring application.

Responsibilities:

execute nvidia-smi
parse GPU metrics
connect to SQL
insert monitoring records
run continuously
config.txt

Contains database connection configuration.

The application reads SQL credentials dynamically from this file.

Format:

host,database,username,password,port

Example:

127.0.0.1,gpu_monitor,root,mypassword,3306
requirements.txt

Python dependencies required by the project.

Install dependencies using:

pip install -r requirements.txt
gpu-monitor.service

Linux systemd service definition.

Used to:

start the monitoring process automatically
keep the process alive
restart on failure
integrate with Linux boot process
Requirements
Operating System

Linux distribution with systemd

Examples:

Ubuntu
Debian
CentOS
Rocky Linux
Arch Linux
GPU Requirements
NVIDIA GPU
NVIDIA Drivers Installed
nvidia-smi available in PATH

Verify installation:

nvidia-smi
Python Requirements
Python 3.8+
pip
Database Requirements

Currently supported:

MySQL

Future support planned:

PostgreSQL
SQLite
TimescaleDB
Database Setup

Create the database table:

CREATE TABLE gpu_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gpu_index INT,
    gpu_name VARCHAR(255),
    temperature INT,
    memory_used INT,
    memory_total INT,
    gpu_utilization INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
Running The Application Manually

Before enabling the Linux service, test the application manually:

python3 app.py

Example runtime logs:

[2026-05-18 12:10:01] GPU 0 | Temp: 51C | Memory: 1200MB/24564MB | Utilization: 32%
[2026-05-18 12:10:01] GPU 1 | Temp: 48C | Memory: 0MB/24564MB | Utilization: 0%
Linux Service Installation

This project uses systemd to run continuously in the background.

Step 1 — Copy Project Files

Example deployment location:

/opt/gpu-monitor

Copy the project directory:

sudo mkdir -p /opt/gpu-monitor
Step 2 — Copy Service File

Copy the service file into the systemd directory:

sudo cp gpu-monitor.service /etc/systemd/system/
Step 3 — Edit Service Configuration

Open the service file:

sudo nano /etc/systemd/system/gpu-monitor.service

Verify paths:

WorkingDirectory=/opt/gpu-monitor
ExecStart=/usr/bin/python3 /opt/gpu-monitor/app.py

Modify them if your project location differs.

Step 4 — Reload systemd
sudo systemctl daemon-reload
Step 5 — Enable Service

Enable automatic startup on boot:

sudo systemctl enable gpu-monitor
Step 6 — Start Service
sudo systemctl start gpu-monitor
Step 7 — Verify Service Status
sudo systemctl status gpu-monitor
Viewing Logs

Real-time logs:

journalctl -u gpu-monitor -f

Logs from today:

journalctl -u gpu-monitor --since today
Example Monitoring Scenarios

This service can be used for:

AI Training Infrastructure

Track GPU usage during training jobs.

Shared GPU Servers

Detect idle or overloaded GPUs.

Thermal Monitoring

Identify overheating GPUs.

Infrastructure Analytics

Analyze long-term utilization patterns.

GPU Scheduling Systems

Provide data for automated resource allocation.

Research Clusters

Monitor compute activity across experiments.

Production Considerations
Security

Avoid storing production credentials in plaintext.

Recommended improvements:

environment variables
encrypted secrets
vault systems
Scalability

Future improvements may include:

multi-node support
distributed monitoring
Prometheus integration
metrics streaming
Reliability

systemd restart policies help ensure continuous operation even after crashes or reboots.
