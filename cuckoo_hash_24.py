# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[[None]*self.bucket_size]*init_size for _ in range(2)]

	def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
		# you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py). 
		# this function randomly chooses an index from a given bucket for a given table. this ensures that the random 
		# index chosen by your code and our test script match.
		# 
		# for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
		# you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
		# will displace the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx) + str(table_id)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[List[int]]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def bucket_full(self, table_id: int, hash_value: int) -> bool:
		bucket = self.tables[table_id][hash_value]
		for i in range(self.bucket_size):
			if bucket[i] is None:
				return False
		return True

	def insert(self, key: int) -> bool:
		if self.lookup(key):
			return True

		table_id = 0
		hash_value = self.hash_func(key, 0)
		cnt = 0
		temp_key = key

		while bucket_full(self, table_id, hash_value):
			if cnt > self.CYCLE_THRESHOLD:
				return False
			cnt += 1
			temp_val = self.tables[table_id][hash_value]
			self.tables[table_id][hash_value] = temp_key
			table_id ^= 1
			temp_key = temp_val
			hash_value = self.hash_func(temp_key, table_id)

		self.tables[table_id][hash_value] = temp_key

		return True
		pass

	def lookup(self, key: int) -> bool:
		table0 = self.tables[0]
		table1 = self.tables[1]

		hash_value0 = self.hash_func(key, 0)
		hash_value1 = self.hash_func(key, 1)

		for i in table0[hash_value0]:
			if key == i:
				return True

		for i in table1[hash_value1]:
			if key == i:
				return True

		return False

	def delete(self, key: int) -> None:
		table0 = self.tables[0]
		table1 = self.tables[1]

		hash_value0 = self.hash_func(key, 0)
		hash_value1 = self.hash_func(key, 1)

		for i in range(self.bucket_size):
			if key == table0[hash_value0][i]:
				table0[hash_value0][i] = None

		for i in range(self.bucket_size):
			if key == table1[hash_value1][i]:
				table1[hash_value1][i] = None

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO
		pass

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


