import os
import time
import datetime
from tqdm import tqdm
import json

# Set the namespace where you want to restart pods
NAMESPACE = "default"

# Set the batch size
BATCH_SIZE = 5

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
for i in tqdm(range(num_batches), desc="Deleting pods", total=num_batches):
    # Get the list of pods to delete in this batch
    start_index = i * BATCH_SIZE
    end_index = (i + 1) * BATCH_SIZE
    pod_list_to_delete = pod_list[start_index:end_index]

    # Log the pods being deleted
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: Deleting pods: {pod_list_to_delete}\n")

    # Delete the pods
    cmd = f"kubectl delete pods -n {NAMESPACE} {' '.join(pod_list_to_delete)}"
    print(f"Running command : {cmd}")
    os.system(cmd)

    # Wait for the pods to be terminated
    time.sleep(5)

    # Calculate the number of pods that have been restarted so far
    num_restarted_pods += len(pod_list_to_delete)

    # Print the status message with the progress bar, pod names, and pod counts
    tqdm.write(f"Restarted {num_restarted_pods}/{num_pods} pods: {pod_list_to_delete}.")

# Print the log file contents to the terminal
with open(LOG_FILE, "r") as log_file:
    print(log_file.read())
