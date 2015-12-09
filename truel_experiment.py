#Britt Binler
#CIT 592, HW 6: Simulation
#October 2015

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import random
import copy
import operator

results = {'Shooter 1' : 0, 'Shooter 2' : 0, 'Shooter 3' : 0} #value = number of times shooter wins
shooters = {'Shooter 1' : 1.0/3, 'Shooter 2' : 2.0/3, 'Shooter 3' : 1} #value = shooter accuracy
alive = copy.deepcopy(shooters)

def get_best_shooter(shooters, shooter):
	'''Finds the most accurate living shooter who is not the person shooting. Returns the best shooter.'''
	global alive
	shooters_copy = copy.deepcopy(alive)
	best_shooter = max(shooters_copy, key=shooters_copy.get) #find the best alive shooter
	while best_shooter == shooter: #make sure the best shooter is 
		del shooters_copy[best_shooter]
		best_shooter = max(shooters_copy, key=shooters_copy.get)
	return best_shooter

def get_second_best_shooter(shooters, shooter):
	'''Finds the most accurate living shooter who is not the person shooting. Returns the best shooter.'''
	global alive
	shooters_copy = copy.deepcopy(alive)
	best_shooter = max(shooters_copy, key=shooters_copy.get) #find the best alive shooter
	while best_shooter == shooter: #make sure the best shooter is not the person shooting
		del shooters_copy[best_shooter]
		best_shooter = max(shooters_copy, key=shooters_copy.get)
	del shooters_copy[best_shooter]
	best_shooter = max(shooters_copy, key=shooters_copy.get) #find the second best alive shooter
	return best_shooter

def strategy1(shooters, shooter):
	'''User-selected shooter will shoot in the air. The next shooter will shoot at the next most 
	accurate shooter that remains alive and so one. Returns a list of survivors.'''
	global alive
	killed = []
	#first two shots
	#Right now, person 1 shoots first. to adjust, change slice
	for person in list(shooters)[1:]: 
		if person in alive: #if person is alive
			r = random.uniform(0,1) #random number to compare to shooter's hit probability
			best_shooter = get_best_shooter(shooters, person)

			if alive[person] > r: #if shooter wins

				killed.append(best_shooter) #removes best shooter from alive and appends to killed
				del alive[best_shooter]

	if len(killed) == 2:
		return list(alive.keys())
	else:
		while len(killed) < 2 : #two people die, the game is over
			for person in list(shooters): 
				if person in alive: #if person is alive
					r = random.uniform(0,1) #random number to compare to shooter's hit probability
					best_shooter = get_best_shooter(shooters, person)

					if alive[person] > r: #if shooter wins
						killed.append(best_shooter) #removes best shooter from alive and appends to killed
						del alive[best_shooter]

		return list(alive.keys())
	

def strategy2(shooters, shooter):
	'''User-selected shooter will shoot at next most accurate shooter.
	Each shooter will shoot at the most accurate shooter that remains alive. Returns a list of survivors.'''
	global alive
	killed = []
	
	while len(killed) < 2 : #two people die, the game is over
		for person in shooters: 
			if person in alive: #if person is alive
				r = random.uniform(0,1) #random number to compare to shooter's hit probability
				best_shooter = get_best_shooter(shooters, person)

				if alive[person] > r: #if shooter wins
					print('person', person, 'shot', best_shooter)
					killed.append(best_shooter) #removes best shooter from alive and appends to killed
					del alive[best_shooter]
					# print(len(killed))

	return list(alive.keys())

def strategy3(shooters, shooter, victim):
	global alive
	killed = []
	#first two shots
	#Right now, person 1 shoots first. to adjust, change slice
	r = random.uniform(0,1) #random number to compare to shooter's hit probability
	second_best_shooter = get_second_best_shooter(shooters, person)

	if alive[person] > r: #if shooter wins
		killed.append(second_best_shooter) #removes best shooter from alive and appends to killed
		del alive[second_best_shooter]

	while len(killed) < 2 : #two people die, the game is over
		for person in list(shooters): 
			if person in alive: #if person is alive
				r = random.uniform(0,1) #random number to compare to shooter's hit probability
				best_shooter = get_best_shooter(shooters, person)

				if alive[person] > r: #if shooter wins
					killed.append(best_shooter) #removes best shooter from alive and appends to killed
					del alive[best_shooter]

		return list(alive.keys())	


def num_wins(winner_list):
	'''Increments results dictionary value of winner key. Handles draws. Updates results.'''
	global results
	draw = 0
	if len(winner_list) == 1:
		results[winner_list[0]] = results[winner_list[0]] + 1
	else:
		draw = draw + 1
	# print(results)
	return results 


def conduct_experiment(n_experiments, strategy_choice, shooter):
	'''Conducts experiment with strategy, first shooter, and number of rounds chosen by user.
	Calls num_wins to update results for each round of shooting. Returns a list of who won each
	round for use in plot.'''
	global shooters
	global alive
	plot_results = []
	i = 0

	for i in range(0, n_experiments):
		shooters = {'Shooter 1' : 1.0/3, 'Shooter 2' : 2.0/3, 'Shooter 3' : 1} #value = shooter accuracy
		alive = copy.deepcopy(shooters)

		if int(strategy_choice) == 1:
			winner = strategy1(shooters, shooter)

		if int(strategy_choice) == 2:
			winner = strategy2(shooters, shooter)

		if int(strategy_choice) == 3:
			winner = strategy2(shooters, shooter)

		num_wins(winner)

		plot_results = plot_results + winner

		i += 1

	return plot_results

def main():		
	global results
	num_people = 3
	num_experiments = int(input('How many rounds of shooting would you like in this Truel? '))	
	shooter = input('''Which shooter would you like to shoot first?
	1: shot accuracy is 1/3
	2: shot accuracy is 2/3
	3: shot accuracy is 1
	Enter the corresponding number of your choice: ''')
	shooter_name = 'Shooter ' + shooter
	result = '{0} hello world {0} hello world {0}'.format(shooter_name)
	strategy_choice = input('''Which strategy would you like to use?
	1: {0} shoots in the air.
	2: {0} shoots at the next most accurate shooter.
	3: {0} shoots at the next least accurate shooter.
	Enter the corresponding number of your choice:  '''.format(shooter_name))




	plot_results = conduct_experiment(num_experiments, strategy_choice, shooter)
	experiment_results = list(results.values())
	plot_results = [1 for x in plot_results if x == 'Shooter 1'] + [2 for x in plot_results if x == 'Shooter 2'] + [3 for x in plot_results if x == 'Shooter 3']
	print(plot_results)
	
	for person in results:
		print(person, results[person])
	return results

	bins = list(range(0, num_people + 1))

	# #Probability
	# a = plt.hist(results, bins, normed=1) #to calculate probability; also need to comment out plt.plot(bins) when using this line
##	plt.xlabel('Number of People Who Matched')
##	plt.ylabel('Probability')
##	plt.title('Histogram of Coat Check Experiment Probability, %d People' %num_people)	
	average = sum(results)/float(len(results))
	print('average', average)

	#Experiment
	plt.xlabel('Number of People Who Matched')
	plt.ylabel('Matches per Experiment')
	plt.title('Histogram of Coat Check Experiment, %d People' %num_people)
	plt.plot(bins) #set x axis

	plt.hist(plot_results, bins)
	plt.show()


if __name__ == '__main__':
	main()
