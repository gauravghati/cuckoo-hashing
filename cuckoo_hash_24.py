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
		self.tables = [[None]*init_size for _ in range(2)]

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

	def insert(self, key: int) -> bool:
		table_id = 0
		hash_value = self.hash_func(key, 0)
		displacement = 0
		curr_key = key

		while self.tables[table_id][hash_value] and len(self.tables[table_id][hash_value]) == self.bucket_size:
			if displacement > self.CYCLE_THRESHOLD:
				return False
			displacement += 1
			rand_idx = self.get_rand_idx_from_bucket(hash_value, table_id)
			temp = self.tables[table_id][hash_value][rand_idx]
			self.tables[table_id][hash_value].remove(temp)
			self.tables[table_id][hash_value].append(curr_key)
			curr_key = temp
			table_id ^= 1
			hash_value = self.hash_func(curr_key, table_id)

		bucket = self.tables[table_id][hash_value]
		if not bucket:
			bucket = [curr_key]
		else:
			bucket.append(curr_key)
		self.tables[table_id][hash_value] = bucket
		return True

	def lookup(self, key: int) -> bool:
		table0 = self.tables[0]
		table1 = self.tables[1]

		hash_value0 = self.hash_func(key, 0)
		hash_value1 = self.hash_func(key, 1)

		bucket0 = table0[hash_value0]
		if bucket0 and key in bucket0:
			return True

		bucket1 = table1[hash_value1]
		if bucket1 and key in bucket1:
			return True

		return False

	def delete(self, key: int) -> None:
		table0 = self.tables[0]
		table1 = self.tables[1]

		hash_value0 = self.hash_func(key, 0)
		hash_value1 = self.hash_func(key, 1)

		bucket0 = table0[hash_value0]
		bucket1 = table1[hash_value1]

		if bucket0 and key in bucket0:
			bucket0.remove(key)
			if not bucket0:
				table0[hash_value0] = None

		if bucket1 and key in bucket1:
			bucket1.remove(key)
			if not bucket1:
				table1[hash_value1] = None

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1
		old_table_size = self.table_size
		old_tables = self.get_table_contents()
		self.table_size = new_table_size
		self.tables = [[None]*new_table_size for _ in range(2)]

		for i in range(old_table_size):
			if old_tables[0][i] is not None:
				for ele in old_tables[0][i]:
					self.insert(ele)

		for i in range(old_table_size):
			if old_tables[1][i] is not None:
				for ele in old_tables[1][i]:
					self.insert(ele)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
