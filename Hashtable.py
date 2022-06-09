class HashTable:
    def __init__(self):
        # initialize the size of the hashmap. Set all positions to None
        self.size = 64
        self.map = [None] * self.size

    def _get_hash(self, key):
        # turn the key into a usable index
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    def insert(self, key, value):
        # index value
        key_hash = self._get_hash(key)
        # constructed list of what will be inserted into the cell
        key_value = [key, value]

        # if cell is empty -> insert list
        # else -> compare the keys -> IF the same update the value: ELSE append the new key_value

        # if cell is empty
        if self.map[key_hash] is None:
            # insert list
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                # compare keys
                if pair[0] == key:
                    # update the value
                    pair[1] = value
                    return True
            # if keys are different add a new key value pair
            self.map[key_hash].append(key_value)
            return True


    def get(self, key):
        # get index
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            # iterate though the keys in the cell
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None


    def delete(self, key):
        # key index
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False

        # use range since to find the index in order to remove an element
        for i in range (0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                # when found remove item from the list
                self.map[key_hash].pop(i)
                return True


    def print(self):
        # prints out every non-none cell of the array
        for item in self.map:
            if item is not None:
                print(str(item))




