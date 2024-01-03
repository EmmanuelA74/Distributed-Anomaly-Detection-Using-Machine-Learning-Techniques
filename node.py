class Node:
    def __init__(self, node_id, cluster_id, info):
        # monitors and charges 
        self.node_id = node_id
        self.cluster_id = cluster_id
        self.info = info
        self.communication_log = []  # to store communication history

    def send_message(self, message, destination_node):
        # Simulate sending a message to another node
        communication_entry = f"Sent '{message}' to Node {destination_node.node_id}"
        self.communication_log.append(communication_entry)

    def receive_message(self, message, source_node):
        # Simulate receiving a message from another node
        communication_entry = f"Received '{message}' from Node {source_node.node_id}"
        self.communication_log.append(communication_entry)

    def broadcast_message(self, message, cluster_nodes):
        # Simulate broadcasting a message to all nodes in the cluster
        for node in cluster_nodes:
            if node != self:
                self.send_message(message, node)