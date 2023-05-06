import os
import time
import datetime
import json
import argparse
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Define argument parser to accept optional arguments for concurrency and batch size
parser = argparse.ArgumentParser(description='Delete and restart pods in a given namespace.')
parser.add_argument('-c', '--concurrency', type=int, default=1, help='Number of threads to use for concurrent execution.')
parser.add_argument('-b', '--batch-size', type=int, default=5, help='Batch size for deleting pods.')
args = parser.parse_args()

# Print script information for the user
print("This script will delete all the healthy pods in a given namespace in batches and then wait for them to restart.")
print("You can set the batch size and sleep interval between batches to customize the script behavior.")
print("You can also set the number of threads to use for concurrent execution.")

# Get the namespace where you want to restart pods
NAMESPACE = input("Enter the namespace where you want to restart pods (default): ").strip() or "default"

# Get the batch size for deleting pods
BATCH_SIZE = args.batch_size

# Get the sleep interval between batches
sleep_interval = input("Enter the sleep interval between batches in seconds (5): ").strip() or "5"
SLEEP_INTERVAL = int(sleep_interval)

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

# Define function to delete pods in a batch
def delete_pods(pod_list_to_delete):
    # Log the pods being deleted
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: Deleting pods: {pod_list_to_delete}\n")

    # Delete the pods
    cmd = f"kubectl delete pods -n {NAMESPACE} {' '.join(pod_list_to_delete)}"
    os.system(cmd)

# Use a thread pool executor to perform concurrent execution
with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
    # Delete all the pods in batches
    num_restarted_pods = 0
    for i in tqdm(range(num_batches), desc="Deleting pods", total=num_batches):
        # Get the list of pods to delete in this batch
        start_index = i * BATCH_SIZE
        end_index = (i + 1) * BATCH_SIZE
        pod_list_to_delete = pod_list[start_index:end_index]

        # Execute the delete_pods function in a separate thread
        executor.submit(delete_pods, pod_list_to_delete)

        # Wait for the pods to be terminated
        time.sleep(SLEEP_INTERVAL)

        # Calculate the number of pods that have been restarted so far
