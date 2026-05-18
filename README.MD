# GPU Monitor Service

A lightweight Linux GPU monitoring service designed for NVIDIA GPU servers.

This project continuously collects GPU statistics using `nvidia-smi`, parses the output, and stores the metrics in a SQL database for monitoring, analytics, and infrastructure management purposes.

The service is intended for:
- AI/ML infrastructure monitoring
- GPU server management
- DevOps environments
- CUDA server observability
- Multi-GPU systems
- Research and training clusters

---

# Features

- Continuous GPU monitoring
- NVIDIA GPU temperature tracking
- GPU memory usage monitoring
- GPU utilization monitoring
- SQL database integration
- Config-based database connection
- Linux systemd service support
- Lightweight and production-friendly
- Multi-GPU support
- Automatic restart using systemd

---

# Project Structure

```text
gpu-monitor/
├── GpuMonitoring.py
├── config.txt
├── requirements.txt
├── gpu-monitor.service
└── README.md