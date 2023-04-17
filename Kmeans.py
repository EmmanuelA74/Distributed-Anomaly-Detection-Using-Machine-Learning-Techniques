import random
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.samples.definitions import FCPS_SAMPLES
from pyclustering.utils import read_sample
from scipy.spatial.distance import euclidean

dataset = []
list = []
node_info = {}

for i in range(100):
    for j in range(3):
        num = random.randint(1, 50)
        list.append(num)
    dataset.append(list)
    list = []

for i in range(len(dataset)):
    node_info[str(dataset[i])] = "This is point " + str(i)

# Load list of points for cluster analysis.
sample = dataset

# Prepare initial centers using K-Means++ method. This is the number of clusters
initial_centers = kmeans_plusplus_initializer(sample, 5).initialize()

# Create instance of K-Means algorithm with prepared centers.
kmeans_instance = kmeans(sample, initial_centers)

# Run cluster analysis and obtain results.
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
    node_info[str(cluster_head)] += " (Cluster Head)"
    
# Visualize obtained results
kmeans_visualizer.show_clusters(sample, clusters, final_centers)
print(clusters)
print(dataset)
print(node_info)

with open('values3.txt', 'w') as data:
    for node, info in node_info.items():
        data.write(node + ": " + info + "\n")
