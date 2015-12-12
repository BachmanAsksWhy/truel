import unittest
import random
import sys
from truel_game import *

class ShooterTest(unittest.TestCase):

	def setUp(self):
		global s
		s = Shooter()

	def test_is_shot(self):
		self.assertEqual(s.is_alive, True)
		s.is_shot()
		self.assertEqual(s.is_alive, False)

class TruelTest(unittest.TestCase):

	def setUp(self):
		global t1
		global ShooterA 
		global ShooterB
		global ShooterC
		ShooterA = Shooter() # least accurate shot
		ShooterB = Shooter() # middle accuracy
		ShooterC = Shooter() # most accurate shot

		ShooterA.hit_probability = 1.0/3
		ShooterB.hit_probability = 2.0/3
		ShooterC.hit_probability = 1

		t1 = Truel([ShooterA, ShooterB, ShooterC], 2, 0)

	def test_instance(self):
		self.assertTrue(isinstance(t1, Truel),
						str(t1) + ' is not an instance of Truel')


	def test_truel_complete(self):
		self.assertEqual(t1.truel_complete(), False)
		t1.hit_count = t1.hit_count + 2
		self.assertEqual(t1.truel_complete(), True)

	def test_find_next_best_shooter(self):
		self.assertEqual(t1.find_next_best_shooter(ShooterA, t1.shooters), ShooterC)
		self.assertEqual(t1.find_next_best_shooter(ShooterB, t1.shooters), ShooterC)
		self.assertEqual(t1.find_next_best_shooter(ShooterC, t1.shooters), ShooterB)
		t1.shooters = t1.shooters[1:]
		self.assertEqual(t1.find_next_best_shooter(ShooterB, t1.shooters), ShooterC)
		self.assertEqual(t1.find_next_best_shooter(ShooterC, t1.shooters), ShooterB)
			
	def test_hit_best_shooter(self):
		self.assertEqual(t1.hit_best_shooter(ShooterC), [ShooterA, ShooterB])
		self.assertEqual(ShooterC.is_alive, False)
		self.assertEqual(t1.hit_count, 1)
		self.assertEqual(t1.killed, [ShooterC])
		self.assertEqual(t1.hit_best_shooter(ShooterB), [ShooterA])
		self.assertEqual(ShooterB.is_alive, False)
		self.assertEqual(t1.hit_count, 2)
		self.assertEqual(t1.killed, [ShooterC, ShooterB])

	def test_miss_best_shooter(self):
		self.assertEqual(t1.miss_best_shooter(ShooterC), [ShooterA, ShooterB, ShooterC])
		self.assertEqual(ShooterC.is_alive, True)
		self.assertEqual(t1.hit_count, 0)
		self.assertEqual(t1.killed, [])
		t1.hit_best_shooter(ShooterB)
		self.assertEqual(t1.miss_best_shooter(ShooterA), [ShooterA, ShooterC])
		self.assertEqual(t1.hit_count, 1)
		self.assertEqual(t1.killed, [ShooterB])

	def test_strategy1(self):
		pass

	def test_strategy2(self):
		pass

	def test_strategy3(self):
		pass

class TruelExperimentTest(unittest.TestCase):

	def setUp(self):
		global t2
		t2 = Truel([ShooterA, ShooterB, ShooterC], 2, 0)

		global te
		te = TruelExperiment()

		global ShooterA 
		global ShooterB
		global ShooterC
		ShooterA = Shooter() # least accurate shot
		ShooterB = Shooter() # middle accuracy
		ShooterC = Shooter() # most accurate shot

	def test_know_strategy(self):
		self.assertEqual(te.know_strategy('2'), 2)
		self.assertEqual(te.know_strategy('1'), 1)
		self.assertEqual(te.know_strategy('3'), 3)

	def test_know_start(self):
		te.shooters = [ShooterA, ShooterB, ShooterC]
		self.assertEqual(te.know_starter(1), ShooterA)
		self.assertEqual(te.know_starter(2), ShooterB)
		self.assertEqual(te.know_starter(3), ShooterC)

	def test_conduct_experiment():
		pass


unittest.main()