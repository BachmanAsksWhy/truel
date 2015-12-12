#Britt Binler
#CIT 592, Truel Simulation
#Fall 2015


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import random
import sys
import copy
import operator
import pprint as pprint
import expectedBullets

################## This method credited to:
## http://stackoverflow.com/questions/4866587/pythonic-way-to-reset-an-objects-variables
def resettable(f):
	def __init_and_copy__(self, *args):
		f(self, *args)
		self.__original_dict__ = copy.deepcopy(self.__dict__)

		def reset(o = self):
			o.__dict__ = o.__original_dict__

		self.reset = reset

	return __init_and_copy__
##################


###############################
###############################
class Shooter:
	@resettable
	def __init__(self, hit_probability = 1.0, name = ""):
		self.hit_probability = hit_probability
		self.is_alive = True
		self.name = ""
		self.bullets_shot = 0
		self.number = 0

	def get_is_alive(self):
		return self.is_alive

	def get_hit_probability(self):
		return self.hit_probability

	def get_name(self):
		return self.name

	def get_bullets_shot(self):
		return self.bullets_shot

	def get_wins(self):
		return self.wins

	def is_shot(self):
		self.is_alive = False


###############################
###############################


class Truel:
	@resettable
	def __init__(self, shooters, strategy, starter):
		self.hit_count = 0
		self.bullets_shot = 0
		self.shooters = shooters
		self.num_shooters = len(shooters)
		self.strategy = strategy
		self.first_shooter = starter #shooter object
		self.alive = self.shooters[:] #list of shooter objects
		self.killed = [] #list of shooter objects
		self.bullet_results = [] #list of shooter objects
		self.results = [] #list of ints

	def reset(self):
		self.hit_count = 0
		self.bullets_shot = 0
		self.alive = self.shooters[:] #list of shooter objects
		self.num_shooters = len(self.shooters)
		self.killed = [] #list of shooter objects


################################### get functions

	def get_hit_count(self):
		return self.hit_count

	def get_strategy(self):
		return self.strategy

	def get_shots_fired(self):
		return self.shots_fired

	def get_shooters(self):
		return self.shooters

	def get_num_shooters(self):
		return self.num_shooters

	def get_alive(self):
		return self.alive

	def get_killed(self):
		return self.killed

	def get_bullet_results(self):
		return self.bullet_results

	def get_bullets_shot(self):
		return self.bullets_shot

	def get_results(self):
		return self.results



##################################

	def truel_complete(self):
		return self.hit_count == 2

	def find_next_best_shooter(self, person, shooters):
		#person is an object, shooters is a list of objects
		shooters_by_accuracy = {}
		try:
			for shooter in shooters:
				#adds shooters to dictionary with hit probability as keys
				shooters_by_accuracy[shooter.get_hit_probability()] = shooter
				best_shooter = shooters_by_accuracy[max(shooters_by_accuracy.keys())]
			if person == best_shooter:
				#if the person shooting is the best shooter, assigns next best shooter
				del shooters_by_accuracy[max(shooters_by_accuracy.keys())]
				best_shooter = shooters_by_accuracy[max(shooters_by_accuracy.keys())]
			return best_shooter
		except ValueError:
			pass
		
	def hit_best_shooter(self, best_shooter):
		best_shooter.is_shot()
		self.hit_count = self.hit_count + 1 #increment total hit count
		self.killed.append(best_shooter)
		del self.alive[self.alive.index(best_shooter)]
		return self.killed

	def check_if_hits_target(self, shooter):
		r = random.uniform(0,1)
		print(r)
		if shooter.get_hit_probability() > r:
			return True
		else:
			return False

##################################

	#Strategy 1: first_shooter shoots in air, everyone then shoots at next most accurate person
	def strategy1(self):
		self.alive = copy.deepcopy(self.shooters)
		start = shooters.index(first_shooter) + 1
		# print(shooters)
		for person in self.shooters[start:]: 
			best_shooter = self.find_next_best_shooter(person, self.shooters)
			r = random.uniform(0,1)
			print(r, 'is r in strategy1')
			if person.get_hit_probability() > r:
				winner = self.hit_best_shooter(person, best_shooter)
				best_shooter = self.find_next_best_shooter(person, self.alive)
			# print(self.hit_count)
		if self.truel_complete():
			winner = self.shooters[0]
			print(winner.get_name(), "wins!")
		else:
			winner = self.strategy2(self.shooters)

		winner = self.shooters[0]
		return winner

	#Strategy 2: first_shooter shoots at best_shooter
	def strategy2(self):
		'''User-selected shooter will shoot at next most accurate shooter.
		Each shooter will shoot at the most accurate shooter that remains alive. Returns a list of survivors.'''
		#TODO: shooters ordered by hit_probability low to high
		print(self.shooters)
		print(self.killed)
		while not self.truel_complete():
			for shooter in self.shooters:

				if shooter not in self.killed:
					print(shooter.get_name(), 'is alive')
					self.bullets_shot = self.bullets_shot + 1
					shooter.bullets_shot = shooter.bullets_shot + 1
					best_shooter = self.find_next_best_shooter(shooter, self.alive)
					if self.check_if_hits_target(shooter):
						print(shooter.get_name(), 'hits', best_shooter.get_name())
						self.alive = self.hit_best_shooter(best_shooter)
		winner = self.alive[0]
		print(winner.get_name(), "wins!")
		return winner #shooter

	#Strategy 3: first_shooter shoots at second_best_shooter
	def strategy3(self, shooters, first_shooter):
		self.alive = copy.deepcopy(self.shooters)
		result = self.shoot_at_best_shooter(self.shooters[0], self.shooters[1])

		for person in self.shooters[1:]: #skip first element, PersonA 'shoots in air'
			best_shooter = self.find_next_best_shooter(person, self.shooters)
			winner = self.shoot_at_best_shooter(person, best_shooter)
		if not self.truel_complete():
			winner = self.strategy2(self.shooters)
		return winner


	# def resettable(f):
	# 	def __init_and_copy__(self, *args):
	# 		f(self, *args)
	# 		self.__original_dict__ = copy.deepcopy(self.__dict__)

	# 		def reset(o = self):
	# 			o.__dict__ = o.__original_dict__

	# 		self.reset = reset

	# 	return __init_and_copy__
	
###############################
###############################


class TruelExperiment():
	@resettable
	def __init__(self):
		self.num_experiments = 0
		self.results = []
		self.bullet_results = []
		self.shooters = []
		self.num_shooters = 0
		self.strategy = 0

################ input functions

	def ask_strategy(self):
		question = """There are three possible strategies:
		Strategy 1: First shooter shoots in air, everyone then shoots at next most accurate person
		Strategy 2: First shooter shoots at most accurate shooter (excluding themself)
		Strategy 3: First shooter shoots at second most accurate shooter (excluding themself)

		Strategy choice: """

		try:
			answer = int(input(question))
			return answer
		except:
			print("Enter the corresponding number - 1, 2, or 3 - to your strategy selection.\n")
			return self.ask_strategy()					
		
		
	def ask_name(self, shooter):
		try:
			shooter.name = input("What is the name of Shooter %d? " %(shooter.number))
			return shooter.name
		except:
			return self.ask_name(shooter)

	def ask_hit_probability(self, shooter):
		try:
			shooter.hit_probability = eval(input("What is %s's hit probability? " %(shooter.name)))
			return shooter.hit_probability
		except:
			print("Enter a number.")
			return self.ask_hit_probability(shooter)

	def ask_num_experiments(self):
		try:
			self.num_experiments = int(input('How many rounds of shooting would you like in this truel experiment? '))	
			return self.num_experiments
		except:
			print("Enter an integer.")
			return self.ask_num_experiments()

	def ask_first_shooter(self):
		try:
			for shooter in self.shooters:
				print("%d:" %(shooter.number), shooter.get_name(), " - Hit Probability: %f" %(shooter.get_hit_probability()))
			first_shooter = int(input("Which shooter fires first? "))
			return first_shooter
		except:
			print("Enter an integer.")
			return self.ask_first_shooter()

	def ask_num_shooters(self):
		try:
			print("Traditionally, 3 shooters participate in a truel.")
			self.num_shooters = int(input('How many shooters will participate in this truel? '))
			return self.num_shooters
		except:
			print("Enter an integer.")
			return self.ask_num_shooters()

	def ask_about_shooters(self):
		try:
			for number in range(0, self.num_shooters):
				self.shooters.append(Shooter())
			i = 1
			for shooter in self.shooters:
				shooter.number = i
				try:
					shooter.name = self.ask_name(shooter)
				except:
					shooter.name = self.ask_name(shooter)
				try:
					shooter.hit_probability = self.ask_hit_probability(shooter)
				except:
					print("Enter a number.")
					shooter.hit_probability = self.ask_hit_probability(shooter)
				i = i + 1
			return self.shooters
		except:
			return self.ask_about_shooters()

#####################

	def know_strategy(self, answer):
		if answer == '':
			return self.ask_strategy()
		elif answer == 1:
			self.strategy = 1
			return self.strategy
		elif answer == 2:
			self.strategy = 2
			return self.strategy
		elif answer == 3:
			self.strategy = 3
			return self.strategy
		else:
			return self.ask_strategy()

	def know_starter(self, first_shooter): #first_shooter is an int
		starter = self.shooters[first_shooter - 1]
		return starter #starter is a shooter

	def conduct_experiment(self, t):
		self.num_experiments = self.ask_num_experiments()
		print('strategy', self.strategy)
		for experiment in range(0, self.num_experiments):
			t.reset() 	#resets some truel values for each round 

			if self.strategy == 1:
				winner = None
				# print(first_shooter.get_name(), "shoots in the air!")
				winner = t.strategy1()

			if self.strategy == 2:
				winner = None
				# print(first_shooter.get_name(), "shoots at the next most accurate shooter!")
				winner = t.strategy2()

			if self.strategy == 3:
				winner = None
				# print(first_shooter.get_name(), "shoots at the second most accurate shooter!")
				winner = t.strategy3()

			self.results.append(winner.number)
			self.bullet_results.append(winner)



	def main(self):

		#TODO handle infinite loop by limiting max number of rounds
		te = TruelExperiment()

		te.num_shooters = te.ask_num_shooters() #int
		te.shooters = te.ask_about_shooters() #list of shooter objects
		strategy_choice = te.ask_strategy() #int
		te.strategy = te.know_strategy(strategy_choice)
		first_shooter = te.ask_first_shooter() #int
		starter = te.know_starter(first_shooter)

		t = Truel(te.shooters, te.strategy, starter)

		te.results = te.conduct_experiment(t) 

		

		replay = input("\nWould you like to play again? Enter yes or no: ")

		if replay[0].lower().strip() == 'y':
			return self.main()
		elif replay[0].lower().strip() == 'n':
			return sys.exit(0)
		else:
			self.main()


if __name__ == "__main__":
	TruelExperiment().main()
