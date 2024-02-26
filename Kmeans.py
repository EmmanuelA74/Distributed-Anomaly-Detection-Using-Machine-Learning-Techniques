import warnings
import random
import numpy as np
from node import Node
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from scipy.spatial.distance import euclidean

# Suppress future warnings to maintain clean output
warnings.simplefilter(action='ignore', category=FutureWarning)

# Generate dataset with random points in 3D space
dataset = [[random.randint(1, 50) for _ in range(3)] for _ in range(201)]

# Dictionary to store information about each node
node_info = {}

# Assign unique information to each point in the dataset
for i in range(len(dataset)):
    node_info[str(dataset[i])] = {"info": "This is point " + str(i)}

# Randomly select a node as the central node
central_node_id = random.choice(list(node_info.keys()))
node_objects = {}

# Create Node objects
for i, (point, info) in enumerate(node_info.items()):
    # Assuming point is the node_id, i is used as cluster_id, and info is used as info
    node_objects[str(point)] = Node(node_id=str(point), cluster_id=i, info=info)
    if point == central_node_id:
        node_objects[str(point)].set_as_central_node()

# Load list of points for cluster analysis
sample = dataset

# Prepare initial center by directly using numpy to initialize cluster center.
initial_centers = np.array(sample)[np.random.choice(len(sample), size=20, replace=False)]

# Create instance of K-Means algorithm with prepared centers
kmeans_instance = kmeans(sample, initial_centers)

# Run cluster analysis and obtain results
kmeans_instance.process()
clusters = kmeans_instance.get_clusters()
final_centers = kmeans_instance.get_centers()

# Assign cluster head to point closest to other points in the cluster
for i, cluster in enumerate(clusters):
    cluster_points = [sample[idx] for idx in cluster]
    cluster_center = final_centers[i]
    min_distance = float('inf')
    cluster_head = None
    for point in cluster_points:
        distance = euclidean(cluster_center, point)
        if distance < min_distance:
            min_distance = distance
            cluster_head = point
    # Update Node object to mark the cluster head
    cluster_head_node = node_objects[str(cluster_head)]
    cluster_head_node.set_as_cluster_head()

    # Update node_info dictionary to indicate the cluster head
    node_info[str(cluster_head)]["node_type"] = "Cluster Head"

    # For each point in the cluster that is not a cluster head, store its two closest points
    distances = [(euclidean(point, p), p) for p in cluster_points if p != cluster_head]
    distances.sort(key=lambda x: x[0])
    non_cluster_head_nodes = [p[1] for p in distances if not node_objects[str(p[1])].is_cluster_head]

    # Ensure there are enough non-cluster head nodes to sample
    if len(non_cluster_head_nodes) >= 2:
        # Assign monitors and charges for non-cluster head nodes
        for non_cluster_head_node_id in non_cluster_head_nodes:
            non_cluster_head_node = node_objects[str(non_cluster_head_node_id)]

            # Update the Node object to mark non-cluster head
            non_cluster_head_node.set_as_non_cluster_head()

            # Update node_info dictionary to indicate non-cluster head
            node_info[str(non_cluster_head_node_id)]["node_type"] = "Non-Cluster Head"

            # Choose two other non-cluster head nodes for monitoring
            monitors_and_charges = random.sample(
                [n for n in non_cluster_head_nodes if n != non_cluster_head_node_id], 2
            )

            # Update the monitored nodes to record the current node
            for monitored_node_id in monitors_and_charges:
                monitored_node = node_objects[str(monitored_node_id)]
                non_cluster_head_node.monitor1 = monitored_node_id
                non_cluster_head_node.charge1 = monitored_node_id

                # Send charge information to the cluster head
                cluster_head_node.send_charge_info(cluster_head_node)

                # Print node information
                print(f"\nNode {non_cluster_head_node.node_id} Info:")
                print("-------------------")
                print(f"info: {non_cluster_head_node.info['info']}")
                print(f"coordinates: {non_cluster_head_node.node_id}")
                print(f"monitored_by: {monitors_and_charges}")
                print(f"charge: {non_cluster_head_node.charge}")
                print(f"cluster_head: {cluster_head_node.node_id}")
                print()

# Visualize obtained results
kmeans_visualizer.show_clusters(sample, clusters, final_centers)

# Print information directly to the terminal
for node, obj in node_objects.items():
    print(f"{node}: {obj.info['info']}", end="")
    if obj.is_cluster_head:
        print(" (Cluster Head)", end="")
    if obj.is_central_node:
        print(" (Central Node) Coordinates: {node}", end="")
    print()

# Print Cluster Heads
print("\nCluster head nodes:")
for node, obj in node_objects.items():
    if obj.is_cluster_head:
        print(f"{node}: {obj.info['info']}")
        print(f"Attack result: {obj.check_for_attack()}")
        print(f"coordinates: {node}")
        print(f"nodes in the cluster: {cluster_points}")
        print()

# Print Central Node
central_node = [node for node, obj in node_objects.items() if obj.is_central_node][0]
print(f"\nCentral Node:")
central_node_info = node_objects[central_node].info
print(f"info: {central_node_info['info']}")
print(f"coordinates: {central_node}")
print("Cluster Heads:")
for node, obj in node_objects.items():
    if obj.is_cluster_head:
        print(node)


# Define a time interval (in minutes)
time_interval = 30 # 10 minutes, to be adjusted

# Simulate activities over time
for minute in range(time_interval):
    print(f"\nMinute {minute + 1}:")

    # Each node in the cluster shares a temperature reading with its cluster head
    for node_id, node_obj in node_objects.items():
        if node_obj.is_non_cluster_head or node_obj.is_cluster_head:
            temperature_reading = random.randint(20, 30)  # Simulate temperature readings
            node_obj.communication_log.append({"timestamp": minute, "node_id": node_id, "temperature": temperature_reading})

            # Penalize energy for transmission
            node_obj.set_charge(node_obj.charge - 1)

            # If the node is a cluster head, penalize less for reception
            if node_obj.is_cluster_head:
                node_obj.set_charge(node_obj.charge - 0.5)

    # Every 5 minutes, the cluster head sends the list to the central node
    if (minute + 1) % 5 == 0:
        print("\nSending data to Central Node:")
        central_node_obj = node_objects[central_node]
        data_to_send = []

        # Collect data from cluster heads
        for node_id, node_obj in node_objects.items():
            if node_obj.is_cluster_head:
                data_to_send.extend(node_obj.communication_log)

        # Calculate energy spent (proportional to the amount of data sent)
        energy_spent = len(data_to_send)
        central_node_obj.set_charge(central_node_obj.charge - energy_spent)

        # Clear communication logs after sending data
        for node_id, node_obj in node_objects.items():
            if node_obj.is_cluster_head:
                node_obj.communication_log = []

    # Print node information after each minute
    for node_id, obj in node_objects.items():
        print(f"\nNode {node_id} Info:")
        print("-------------------")
        print(f"info: {obj.info['info']}")
        print(f"coordinates: {node_id}")
        print(f"charge: {obj.charge}")
        print("Energy spent: " + energy_spent)
