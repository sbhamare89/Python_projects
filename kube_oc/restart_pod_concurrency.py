import os
import time
import datetime
from tqdm import tqdm
import json
import threading

# Print script information for the user
print("This script will delete all the healthy pods in a given namespace in batches and then wait for them to restart.")
print("You can set the batch size and sleep interval between batches to customize the script behavior.")

# Get the namespace where you want to restart pods
NAMESPACE = input("Enter the namespace where you want to restart pods (default): ").strip() or "default"

# Get the batch size for deleting pods
batch_size = input("Enter the batch size for deleting pods (5): ").strip() or "5"
BATCH_SIZE = int(batch_size)

# Get the sleep interval between batches
sleep_interval = input("Enter the sleep interval between batches in seconds (5): ").strip() or "5"
SLEEP_INTERVAL = int(sleep_interval)

# Get the number of concurrent threads
num_threads = input("Enter the number of concurrent threads (1): ").strip() or "1"
NUM_THREADS = int(num_threads)

# Generate a unique log file name based on the current date and time
now = datetime.datetime.now()
DATE = now.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f"./logs/restart_pods_{NAMESPACE}_{DATE}.log"

# Create logs directory if it does not exist
if not os.path.exists('./logs'):
    os.mkdir('./logs')

# Get a list of all healthy pods in the namespace
pods_output = os.popen(f'kubectl get pods -n {NAMESPACE} -o json').read()
pods_json = json.loads(pods_output)
pod_list = [pod["metadata"]["name"] for pod in pods_json["items"]]
num_pods = len(pod_list)

# Calculate the number of batches
num_batches = (num_pods + BATCH_SIZE - 1) // BATCH_SIZE

# Delete all the pods in batches
num_restarted_pods = 0
lock = threading.Lock()

def delete_pods(pod_list_to_delete):
    global num_restarted_pods
    # Delete the pods
    cmd = f"kubectl delete pods -n {NAMESPACE} {' '.join(pod_list_to_delete)}"
    print(f"Running command : {cmd}")
    os.system(cmd)

    # Wait for the pods to be terminated
    time.sleep(SLEEP_INTERVAL)

    # Calculate the number of pods that have been restarted so far
    with lock:
        num_restarted_pods += len(pod_list_to_delete)

    # Log the pods being deleted
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: Deleting pods: {pod_list_to_delete}\n")

    # Print the status message with the progress bar, pod names, and pod counts
    tqdm.write(f"Restarted {num_restarted_pods}/{num_pods} pods: {pod_list_to_delete}.")

def delete_pods_threaded(pod_list_to_delete):
    threads = []
    for i in range(NUM_THREADS):
        start_index = i * (len(pod_list_to_delete) // NUM_THREADS)
        end_index = (i + 1) * (len(pod_list_to_delete) // NUM_THREADS)
        if i == NUM_THREADS - 1:
            end_index = len(pod_list_to_delete)
        pod_list_to_delete_thread = pod_list_to_delete[start_index:end_index]
        t = threading.Thread(target=delete
