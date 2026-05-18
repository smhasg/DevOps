import subprocess
import mysql.connector
import time
from datetime import datetime

CONFIG_FILE = "config.txt"

POLL_INTERVAL = 10


def load_config():
    with open(CONFIG_FILE, "r") as f:
        data = f.read().strip().split(",")

    return {
        "host": data[0],
        "database": data[1],
        "user": data[2],
        "password": data[3],
        "port": int(data[4])
    }


def get_gpu_stats():
    command = [
        "nvidia-smi",
        "--query-gpu=index,name,temperature.gpu,memory.used,memory.total,utilization.gpu",
        "--format=csv,noheader,nounits"
    ]

    result = subprocess.check_output(command).decode("utf-8").strip()

    gpus = []

    for line in result.split("\n"):
        parts = [x.strip() for x in line.split(",")]

        gpu = {
            "gpu_index": int(parts[0]),
            "gpu_name": parts[1],
            "temperature": int(parts[2]),
            "memory_used": int(parts[3]),
            "memory_total": int(parts[4]),
            "gpu_utilization": int(parts[5])
        }

        gpus.append(gpu)

    return gpus


def insert_stats(connection, gpu):
    cursor = connection.cursor()

    query = """
    INSERT INTO gpu_stats (
        gpu_index,
        gpu_name,
        temperature,
        memory_used,
        memory_total,
        gpu_utilization
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        gpu["gpu_index"],
        gpu["gpu_name"],
        gpu["temperature"],
        gpu["memory_used"],
        gpu["memory_total"],
        gpu["gpu_utilization"]
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()


def main():
    config = load_config()

    connection = mysql.connector.connect(
        host=config["host"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
        port=config["port"]
    )

    print("GPU Monitor Started")

    while True:
        try:
            gpus = get_gpu_stats()

            for gpu in gpus:
                insert_stats(connection, gpu)

                print(
                    f"[{datetime.now()}] "
                    f"GPU {gpu['gpu_index']} | "
                    f"Temp: {gpu['temperature']}C | "
                    f"Memory: {gpu['memory_used']}MB/{gpu['memory_total']}MB | "
                    f"Utilization: {gpu['gpu_utilization']}%"
                )

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()