class Node:
    def __init__(self, node_id, cluster_id, info):
        # Initialize a Node instance.

        # Parameters:
        # - node_id (str): Unique identifier for the node.
        # - cluster_id (int): Identifier for the cluster to which the node belongs.
        # - info (str): Information or description associated with the node.
        # - 

        # Attributes:
        # - node_id (str): Unique identifier for the node.
        # - cluster_id (int): Identifier for the cluster to which the node belongs.
        # - info (str): Information or description associated with the node.
        # - communication_log (list): List to store communication history.
        # - monitor1 (str): Identifier of the first node that this node is monitoring.
        # - monitor2 (str): Identifier of the second node that this node is monitoring.
        # - charge1 (str): Identifier of the first node that is monitoring this node.
        # - charge2 (str): Identifier of the second node that is monitoring this node.
        # - charge_info (dict): Dictionary to store received charge information.
        
        self.node_id = node_id
        self.cluster_id = cluster_id
        self.info = info
        self.communication_log = []  
        self.monitor1 = -1
        self.monitor2 = -1
        self.charge1 = -1
        self.charge2 = -1
        self.is_cluster_head = False
        self.is_central_node = False
        self.is_non_cluster_head = False
        self.millivolts = 1500 # each node has a battery capacity of 1.5V or 1,500 millivolts

    def set_as_cluster_head(self):
        self.is_cluster_head = True

    def set_as_central_node(self):
        self.is_central_node = True

    def set_as_non_cluster_head(self):
        self.is_non_cluster_head = True

    def set_charge(self, charge):
        self.charge = charge

    #TBD: nothing can be carried out when the energy level of the node is dead.
    def consume_energy(self, amount):
        # Reduce the energy by the specified amount.
        self.millivolts -= amount
        if self.millivolts < 0:
            self.millivolts = 0  # Ensure energy doesn't go below zero

    def check_energy(self):
        print("This node has " + str(self.millivolts) + " millivolts remaining!")

    def send_charge_info(self, destination_cluster_head):
        # Simulate sending charge information to the cluster head.

        # Parameters:
        # - destination_cluster_head (Node): The cluster head to which the charge information is sent.

        destination_cluster_head.receive_charge_info(self.charge, self.node_id)

        # Consume charge for sending charge info
        self.consume_charge(1.5)

    def receive_charge_info(self, charge, source_node_id):
        # Simulate receiving charge information from another node.

        # Parameters:
        # - charge (int): The received charge information.
        # - source_node_id (str): The identifier of the node from which the charge information is received.

        self.charge_info = {"source_node": source_node_id, "charge": charge}

        # Consume charge for recieving charge info
        self.consume_charge(0.5)

    
        
        
