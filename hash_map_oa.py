# Description: This is a HashMap implementation with Open Addressing and Quadratic Probing using HashEntries.


from helper_classes import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def q_probe(self, index: int, init_index: int, probe: int, capa: int, key: str) -> int:
        """Helper method to perform quadratic probing.

        @param: index - the current array position
                init_index - the initial array index
                probe - the probe factor
                capacity - the capacity of the current array
                key - the key of the object we're looking to place
        @return: the index either modified or staying the same
        """
        # Keep looking until we don't have a collision, then apply the quadratic probing formula
        # If statement to break if the same key is found for the replacement scenario
        while self._buckets[index]:
            if self._buckets[index].key == key:
                return index
            index = (init_index + probe ** 2) % capa
            probe += 1
        return index

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in the hash map. If the key already exists, its value is replaced
        with the new value, otherwise it is added on as usual. The table must also be resized when the
        load factor is >= 0.5.

        @param: key - the key used to search, value - the value for the corresponding key
        @return: None
        """
        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        hash = self._hash_function(key)
        index = hash % self._capacity
        probe = 1
        init_index = index

        # Recalculates the index
        index = self.q_probe(index, init_index, probe, self._capacity, key)

        # No collision, simply set it to a new HashEntry, increment size
        # Otherwise, check when the current index is a tombstone, if so, set it to new HashEntry, toggle off
        # tombstone status and increment size. If not, simply replace the value but don't increment size.
        if not self._buckets[index]:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        else:
            if self._buckets[index].is_tombstone is True:
                self._buckets[index] = HashEntry(key, value)
                self._buckets[index].is_tombstone = False
                self._size += 1
            elif self._buckets[index].key == key:
                self._buckets[index].value = value

    def table_load(self) -> float:
        """
        Computes the load factor using the formula size/capacity

        @param: None
        @return: a floating point number indicating the load factor
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        @param: None
        @return: an integer indicating the amount of empty buckets
        """
        # Iterate count when the current index is None, or it has the tombstone status toggled on.
        count = 0
        for pos in range(self._buckets.length()):
            if self._buckets[pos] is None or self._buckets[pos].is_tombstone is True:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of the hash table, keeps all existing key/value pairs while rehashing all links.
        Only works when the new_capacity >= 1 or the new_capacity is >= the current size.

        @param: the new capacity of the hash table
        @return: None
        """
        if new_capacity >= 1 and new_capacity >= self._size:
            # stores the old bucket and its capacity into temp variables, then set to new capacity
            # and populate the new bucket with None values.
            former_table = self._buckets
            former_capa = self._capacity
            self._capacity = new_capacity
            new_buckets = DynamicArray()

            for val in range(new_capacity):
                new_buckets.append(None)

            # References buckets to the new buckets, reset size
            # Loop through and put the old table's elements that are not none or has False for tombstone
            # status into the new bucket, rehashing and updating size is done within put().
            self._buckets = new_buckets
            self._size = 0
            for pos in range(former_capa):
                if former_table[pos] and former_table[pos].is_tombstone is False:
                    self.put(former_table[pos].key, former_table[pos].value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key

        @param: key used to search
        @return: the value corresponding to key, None if key is not found
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        probe = 1
        init_index = index

        # Recalculates index if there was a collision when placing the value
        index = self.q_probe(index, init_index, probe, self._capacity, key)

        if self.contains_key(key):
            return self._buckets[index].value

    def contains_key(self, key: str) -> bool:
        """
        Checks if a given key is in the hash map.

        @param: key - the key used to search
        @return: boolean indicating if the chain has the key
        """
        # Extra condition to ensure that the tombstone value has to be toggled off before returning true.
        for pos in range(self._capacity):
            if self._buckets[pos] and self._buckets[pos].key == key and self._buckets[pos].is_tombstone is False:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key(if found) and its associated value from the hash map.

        @param: key used to search
        @return: None
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        probe = 1
        init_index = index

        index = self.q_probe(index, init_index, probe, self._capacity, key)

        # toggles tombstone status and decrements the size
        if self._buckets[index] and self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            self._buckets[index].is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map, does not change table capacity.

        @param: None
        @return: None
        """
        # Loops through to set every value to None in buckets, then resets the current size to 0
        for pos in range(self._capacity):
            self._buckets[pos] = None
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Returns a DA that has all the keys stored in the hash map.

        @param: None
        @return: the DA storing all the keys of hash map
        """
        # Make sure the value at the current index is not None and that its tombstone status is False before appending.
        keys_arr = DynamicArray()
        for pos in range(self._capacity):
            if self._buckets[pos] and self._buckets[pos].is_tombstone is False:
                keys_arr.append(self._buckets[pos].key)

        return keys_arr


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
