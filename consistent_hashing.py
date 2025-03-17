import hashlib
import bisect
from collections import defaultdict

class ConsistentHashing:
    def __init__(self, num_replicas=3):
        """
        Initialize the consistent hashing ring.
        :param num_replicas: Number of virtual nodes per real node.
        """
        self.num_replicas = num_replicas
        self.ring = {}  # Hash ring {hash_value: node}
        self.sorted_keys = []  # Sorted list of hash values
        self.node_keys = defaultdict(set)  # Mapping: {node -> set(keys)}

    def _hash(self, key):
        """Generate a hash value using MD5."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node):
        """
        Add a node with multiple virtual nodes.
        Redistributes keys that were assigned to the next node.
        """
        for i in range(self.num_replicas):
            hash_val = self._hash(f"{node}#{i}")
            self.ring[hash_val] = node
            bisect.insort(self.sorted_keys, hash_val)

        self._redistribute_keys()

    def remove_node(self, node):
        """
        Remove a node and its virtual nodes from the ring.
        Redistributes the node's keys to the next available node.
        """
        keys_to_redistribute = set()
        
        # Remove virtual nodes from the ring
        for i in range(self.num_replicas):
            hash_val = self._hash(f"{node}#{i}")
            if hash_val in self.ring:
                del self.ring[hash_val]
                self.sorted_keys.remove(hash_val)

        # Collect keys that need redistribution
        if node in self.node_keys:
            keys_to_redistribute = self.node_keys[node]
            del self.node_keys[node]

        self._redistribute_keys(keys_to_redistribute)

    def _redistribute_keys(self, keys_to_redistribute=None):
        """
        Redistributes keys when a node is added or removed.
        Moves affected keys to the correct node.
        """
        if keys_to_redistribute is None:
            # Reassign all keys in case of new node addition
            keys_to_redistribute = {key for keys in self.node_keys.values() for key in keys}
            self.node_keys.clear()

        for key in keys_to_redistribute:
            assigned_node = self.get_node(key)
            if assigned_node:
                self.node_keys[assigned_node].add(key)

    def get_node(self, key):
        """
        Get the node responsible for storing the given key.
        Assigns key if not already mapped.
        """
        if not self.ring:
            return None  # No nodes available

        hash_val = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_val) % len(self.sorted_keys)
        assigned_node = self.ring[self.sorted_keys[idx]]

        # Assign the key to the node if not already assigned
        self.node_keys[assigned_node].add(key)

        return assigned_node

    def display_ring(self):
        """Prints the hash ring and key distribution for debugging."""
        print("\n--- Hash Ring ---")
        for hash_val in sorted(self.ring):
            print(f"{hash_val} -> {self.ring[hash_val]}")
        
        print("\n--- Node Key Mapping ---")
        for node, keys in self.node_keys.items():
            print(f"{node}: {sorted(keys)}")


# Example Usage
# if __name__ == "__main__":
#     ch = ConsistentHashing(num_replicas=3)

#     # Adding nodes
#     ch.add_node("NodeA")
#     ch.add_node("NodeB")
#     ch.add_node("NodeC")

#     print("\n--- Initial Hash Ring and Key Distribution ---")
#     ch.display_ring()

#     # Assign keys
#     keys = ["key1", "key2", "key3", "key4", "key5", "key6"]
#     for key in keys:
#         print(f"Key {key} is assigned to {ch.get_node(key)}")

#     print("\n--- Updated Key Distribution After Assignments ---")
#     ch.display_ring()

#     # Remove a node
#     print("\n--- Removing NodeB ---")
#     ch.remove_node("NodeB")
#     ch.display_ring()

#     # Add a new node
#     print("\n--- Adding NodeD ---")
#     ch.add_node("NodeD")
#     ch.display_ring()
