class Node:
    def __init__(self, name, contact_number, address=None):
        self.prev = None
        self.next = None
        self.name = name
        self.contact_number = contact_number
        self.address = address

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.name_list, self.address_list, self.contact_number_list = [], [], []

    def return_head(self):
        return self.head

    def insert(self, name=None, contact_number=None, address=""):
        # Handling base cases
        if name is None and contact_number is None:
            return "Please provide your name and contact number"
        elif name is None:
            return "Please provide your name"
        elif contact_number is None:
            return "Please provide your contact number"

        # Checking if the list is empty
        if self.head == None:
            self.head = Node(name, contact_number, address)
            self.tail = self.head
        # If not, insert new contact details at the end of the doubly linked list
        else:
            new_node = Node(name, contact_number, address)
            self.tail.next = new_node
            self.tail = new_node
        return "Success"

    def delete_node(self, name, address, contact_number):
        prev, current = self.search(name, address, contact_number)
        if prev is None:
            self.head = current.next
        else:
            prev.next = current.next
        del current

    def update(self, prev_name, prev_address, prev_contact_number, name, address, contact_number):
        prev, current = self.search(prev_name, prev_address, prev_contact_number)
        current.name = name
        current.address = address
        current.contact_number = contact_number

    def search(self, name, address, contact_number):
        current = self.return_head()
        prev = None
        while current is not None:
            if name == current.name and address == current.address and contact_number == current.contact_number:
                break
            prev = current
            current = current.next
    
        return prev, current