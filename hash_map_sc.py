# Description: This is a HashMap implementation using chaining with the help of the LinkedList class.


from helper_classes import (DynamicArray, LinkedList,
                            hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hashmap. If a given key already exists,
        within, its associated value is replaced with a new value. Otherwise, a new key/value
        pair is added.

        @param: key - used to search if the entry contains the key
                value - if the key is found, inserted into the entry along with key
        @return: None
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        entry = self._buckets[index]

        # Checks if the key is already in the entry, updates size(or not) accordingly
        if entry.contains(key):
            entry.remove(key)
            entry.insert(key, value)
        else:
            entry.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        @param: None
        @return: an integer indicating the amount of empty buckets
        """
        # Initialize a counter and go through each bucket, increment when the bucket's LL has a length of 0.
        count = 0
        for pos in range(self.get_capacity()):
            if self._buckets[pos].length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Computes the load factor using the formula size/capacity

        @param: None
        @return: a floating point number indicating the load factor
        """
        return self.get_size() / self.get_capacity()

    def clear(self) -> None:
        """
        Clears the contents of the hash map, does not change table capacity.

        @param: None
        @return: None
        """
        # Loop through and set each bucket to an empty LL and resetting the size
        for pos in range(self.get_capacity()):
            self._buckets[pos] = LinkedList()
            self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of the hash table, keeps all existing key/value pairs while rehashing all links.
        Only works when the new_capacity >= 1.

        @param: the new capacity of the hash table
        @return: None
        """
        # if the new capacity is <= 0, do nothing
        # store old table/capacity into temp variables, assigning new capacity, populating new buckets, then resetting
        # size. Iterate through old table and call put() to rehash key/value pairs into the new bucket, which also
        # updates the current size.
        if new_capacity > 0:
            former_table = self._buckets
            former_capa = self._capacity
            self._capacity = new_capacity
            new_buckets = DynamicArray()
            for val in range(new_capacity):
                new_buckets.append(LinkedList())

            self._buckets = new_buckets
            self._size = 0
            for pos in range(former_capa):
                if former_table[pos] is not None:
                    for node in former_table[pos]:
                        self.put(node.key, node.value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.

        @param: the key used to search
        @return: the value of the object, None if the key is not found
        """
        if self.contains_key(key):
            hash = self._hash_function(key)
            index = hash % self._capacity
            return self._buckets[index].contains(key).value

    def contains_key(self, key: str) -> bool:
        """
        Checks if a given key is in the hash map.

        @param: key - the key used to search
        @return: boolean indicating if the chain has the key
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        chain = self._buckets[index]

        return True if chain.contains(key) else False

    def remove(self, key: str) -> None:
        """
        Removes the given key(if found) and its associated value from the hash map.

        @param: key used to search
        @return: None
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].contains(key):
            self._buckets[index].remove(key)
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Returns a DA containing all the keys stored in the hash map.

        @param: None
        @return: a DA storing all the keys from hash map
        """
        result_keys = DynamicArray()
        for pos in range(self._buckets.length()):
            for node in self._buckets[pos]:
                result_keys.append(node.key)
        return result_keys


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the mode(s) of an array of values not guaranteed to be sorted.

    @param: da - a DynamicArray of LL
    @return: a tuple containing a DA of the mode value(s), and its occurrences.
    """

    # initialize an additional mode_map to help out with values that share the mode count.
    map = HashMap(da.length() // 3, hash_function_1)
    mode_map = HashMap(da.length() // 3, hash_function_1)
    mode_count = 1

    # Iterate through and utilize value as an occurrences counter, set to 1 or increment value,
    # update mode_count alongside it to store the largest mode so far.
    for pos in range(da.length()):
        if map.contains_key(da[pos]):
            count = map.get(da[pos]) + 1
            map.put(da[pos], count)
            if count >= mode_count:
                mode_count = count
        else:
            map.put(da[pos], 1)

    # Iterate through DA again, now compare each node's occurrence value to the mode count, if it matches,
    # put the key and its mode count onto mode_map, then get its keys to store into the return tuple.
    for pos in range(da.length()):
        if map.get(da[pos]) == mode_count:
            mode_map.put(da[pos], mode_count)

    return [mode_map.get_keys(), mode_count]


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

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ['-147', '-147', '-147', '196', '921', '557', '639', '-480', '-480'],
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")
