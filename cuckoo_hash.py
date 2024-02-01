# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[int]]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		if self.lookup(key):
			return True

		table_id = 0
		hash_value = self.hash_func(key, 0)
		displacements = 0
		curr_key = key

		while self.tables[table_id][hash_value] is not None:
			if displacements > self.CYCLE_THRESHOLD:
				return False
			displacements += 1
			temp, self.tables[table_id][hash_value] = self.tables[table_id][hash_value], curr_key
			table_id ^= 1
			curr_key = temp
			print(table_id, hash_value)
			hash_value = self.hash_func(curr_key, table_id)

		self.tables[table_id][hash_value] = curr_key

		return True

	def lookup(self, key: int) -> bool:
		table0 = self.tables[0]
		table1 = self.tables[1]

		hash_value0 = self.hash_func(key, 0)
		hash_value1 = self.hash_func(key, 1)

		if table0[hash_value0] == key or table1[hash_value1] == key:
			return True

		return False

	def delete(self, key: int) -> None:
		hash_value0 = self.hash_func(key, 0)
		hash_value1 = self.hash_func(key, 1)

		if self.tables[0][hash_value0] == key:
			self.tables[0][hash_value0] = None
		elif self.tables[1][hash_value1] == key:
			self.tables[1][hash_value1] = None

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1
		old_table_size = self.table_size
		self.table_size = new_table_size
		old_tables = self.tables
		self.tables = [[None]*new_table_size for _ in range(2)]

		for i in range(old_table_size):
			if old_tables[0][i] is not None:
				self.insert(int(old_tables[0][i]))

		for i in range(old_table_size):
			if old_tables[1][i] is not None:
				self.insert(int(old_tables[1][i]))

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define

# chash = CuckooHash(10)
# chash.insert(12)
# print("12(0): ", chash.hash_func(12, 0,))
# print("12(0): ", chash.hash_func(12, 1,))
# print(chash.get_table_contents())
# chash.insert(11)
# print("11: ", chash.hash_func(11, 0,))
# print(chash.get_table_contents())
# chash.insert(24)
# print("24: ", chash.hash_func(24, 0,))
# print(chash.get_table_contents())
# chash.insert(100)
# print("100: ", chash.hash_func(100, 0,))
# print(chash.get_table_contents())
# chash.insert(101)
# print("101(0): ", chash.hash_func(101, 0,))
# print("101(1): ", chash.hash_func(101, 1,))
# print(chash.get_table_contents())
# chash.insert(13)
# print("13: ", chash.hash_func(13, 0,))
# print(chash.get_table_contents())
# print("insertion of 15: ", chash.insert(15))
# print("15(0): ", chash.hash_func(15, 0,))
# print("15(1): ", chash.hash_func(15, 1,))
# print(chash.get_table_contents())
# chash.insert(22)
# print("22: ", chash.hash_func(22, 0,))
# print(chash.get_table_contents())
# chash.insert(25)
# print("25: ", chash.hash_func(25, 0,))
# print(chash.get_table_contents())
# chash.insert(27)
# print("27: ", chash.hash_func(27, 0,))
# print(chash.get_table_contents())
# chash.rehash(15)
# print(chash.get_table_contents())
