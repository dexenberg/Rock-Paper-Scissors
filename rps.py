from numpy import random
from collections import deque
import math
import agent 
import ast
import os.path
from os import path

rps = {'r':'Rock', 's':'Scissors', 'p':'Paper'}
userscore = 0
compscore = 0	


# def wtl(agent, user_guess):
	# if (user_guess == 'r'):
		# return (agent.p_p, agent.p_r, agent.p_s)
	# if (user_guess == 's'):
		# return (agent.p_r, agent.p_s, agent.p_p)
	# else:
		# return (agent.p_s, agent.p_p, agent.p_r)

def battle(ch, ch1):     # 1 if ch beats ch1; 0 for tie; -1 if ch gets beaten by ch1
	if (ch == ch1):
		return 0
	if ((ch == 'r' and ch1 == 's')  or (ch == 'p' and ch1 == 'r') or (ch == 's' and ch1 == 'p')):
		return 1
	return -1

def show_battle(battle):
	global userscore
	global compscore
	global w
	global t
	global l
	if (battle == 0):
		userscore += 1/2
		compscore += 1/2
		t += 1
		return "Tie                    " + "     User " + str(userscore) + "  :  Computer " + str(compscore)
	if (battle == -1):
		userscore += 1
		w += 1
		return "User Won               " + "     User " + str(userscore) + "  :  Computer " + str(compscore)
	else:
		compscore += 1
		l += 1
		return "Computer Won           " + "     User " + str(userscore) + "  :  Computer " + str(compscore)

def print_stats():
	print("Let's see how you've done")
	print("So far, User won " + str(w) + " battles, Computer won " + str(l) + " and you tied " + str(t) +" times.")
	if (w > l + 5):
		print("Wow.... Unexpected, unreal gameplay!")
	elif (l>w+5):
		print("Imagine being beaten by a computer....PFFFF Cringe and F in the chat boys")
	else:
		print("Hm... Balanced")
	print("If we are looking at finished sessions then User won " + str(sw) + ", Computer won " + str(sl) + ", while you tied " + str(st) + " times.") 

# def agents_guess(agents):   # makes the guess for each agent
	# guesses = []
	# for agent in agents:
		# guesses.append(random.choice(['r', 'p', 's'], p = [agent.p_r, agent.p_p, agent.p_s]))
	# return guesses
	

	


# def user_guess(n):       # when we want to control our user
	# if (n == 1):
		# return list(random.choice(['r', 'p', 's'], p = [1/3, 1/3, 1/3], size = 50))
	# if (n == 2):
		# return ['r']*25 + ['s']*25
	# if (n == 3):
		# return ['r']*50

# def restart_agents_weight():        # reset the weights to 1 for each new session
	# for i in range(len(agents)):
		# agents[i].weight = 1


agents = []
changing_agents = []
staticagentsexpected = 66 * 2
agentspertype = 66 * 3
type_changing_agents = 4;       # only switch clockwise/counter-clockwise/stay based on if last output was loss/win/tie
								#             r/p/s based on last battle output
								# 			  r/p/s based on last symbol played by user
								# 			  r/p/s based on last symbol played by computer


totalagentsexpected = agentspertype * type_changing_agents + staticagentsexpected

symbol_int = {'r' : -1, 'p' : 0, 's' : 1}

def copy_agents(last_battle, way, last_input):
	x =  66 						  						 			  # no of agents of a certain type
	y =  agent.noagents - agent.nochanging_agents					      # all agents that are fixed (agents - nochanging_agents)
	lint = symbol_int[last_input]
	lc = (lint + last_battle)%3
	if (lc == 2):
		lc = -1                                               # deduce last symbol played by computer from last_battle and last_input
	
	if (way == 1):
		agents[ y : (y+x)] = changing_agents[(last_battle + 1) *x : (last_battle + 2) * x] 
		for i in range(y, y+x):
			agents[i].change_probabilities(last_input)
		agents[ (y+x) : (y+2*x)] = changing_agents[(last_battle + 4) *x : (last_battle + 5) * x]
		agents[ (y+2*x) : (y+3*x)] = changing_agents[(lint + 7) *x : (lint + 8) * x] 			
		agents[ (y+3*x) : (y+4*x)] = changing_agents[(lc + 10) *x : (lc + 11) * x] 			
	else:
		changing_agents[(last_battle + 1) * x : (last_battle + 2) * x] = agents[ y : (y+x)]
		changing_agents[(last_battle + 4) * x : (last_battle + 5) * x] = agents[ (y+x) : (y+2*x)]
		changing_agents[(lint + 7) *x : (lint + 8) * x] = agents[ (y+2*x) : (y+3*x)]
		changing_agents[(lc + 10) *x : (lc + 11) * x] = agents[ (y+3*x) : (y+4*x)] 

weights = []
print("Please enter your username:")
username = input().lower()

if (path.exists(username + ".txt")):
	f = open(username+".txt", "r")
	weights = ast.literal_eval(f.readline())
	[w, l, t, sw, sl, st] = ast.literal_eval(f.readline())
	print("Welcome back, " + username[0].upper() + username[1:] + "!")
else:
	f = open(username+".txt", "x")

if (weights == []):
	weights =  [(i,1.0) for i in range(totalagentsexpected)]
	[w,l,t, sw, sl, st] = [0, 0 ,0 ,0, 0, 0]
	print("Good to see new faces around! Good luck!")

agent.create_agents(agents, weights) 
agent.create_changing_agents(changing_agents, weights)

f.close()

# print(weights)


# for agent in agents:
	# print(agent.index, agent.p_r, agent.p_p, agent.p_s, agent.weight, agent.change_after, agent.p_stay, agent.p_ccwise, agent.p_cwise)
	
computerwon = 0
userwon = 0
tie = 0 	
turn = 0
j = 0 

print( "Total number of agents active is " + str(agent.noagents))
print( "To see some of your stats, type 'stats' at any point in the game.")

flag =  True
while(flag):
	print("How big would you like your session to be? (For a better experience we recommend a bigger number)")
	rounds = int(input())
	while ( rounds < 1):
		print("I'm not playing games with you... Well not yet until you choose a proper session size")
		rounds = int(input())
	if (rounds == 69):
		print("Nice ;)")
	print("Here we go!")
	j+=1 
	
	userscore = 0
	compscore = 0	
	# uguess = user_guess(2)
	# restart_agents_weight()
	turn = 0
	
	
	while turn < rounds:
		turn += 1
		print("Turn ", turn)
		# ch = uguess[turn - 1]
		ch = input().lower()
		if (ch == "stats"):
			print_stats()
			turn -= 1
			continue
		elif (len(ch) != 1 or ch not in 'rps'):
			print("Character doesn't represent either Rock, Paper or Scrissors")
			turn -= 1
			continue
			
		# if we passed first turn, then we add the agents that switch sides 	
		if (turn > 1):
			copy_agents(last_battle, 1, prevch)
			for i in range(66, 66*2):                            #change the static ones that update rotations only
				agents[i].change_probabilities(prevch)
		
		
		
		
		# predictions = agents_guess(agents)         	   # make predictions for each agent
		# print(predictions)
		mychoice = agent.decide(agents, 20) 	           # look at the prediction of the agent chosen
		print(username[0].upper() + username[1:] + " played " + rps[ch] + " and Computer played " + rps[mychoice])
		
		agent.update(agents, ch, turn)
		if (turn > 1):
			copy_agents(last_battle, -1, prevch)

		# for agnt in agents:
			# print(agnt.index, agnt.p_r, agnt.p_p, agnt.p_s, agnt.weight, agnt.change_after, agnt.p_stay, agnt.p_ccwise, agnt.p_cwise)
	
		last_battle =  battle(mychoice, ch)
		prevch = ch
		print(show_battle(last_battle) + "   " + str(j))
		
	if (userscore > compscore):
		sw += 1
		userwon += 1
	elif (compscore > userscore):
		sl += 1
		computerwon += 1
	else:
		tie += 1
		st += 1
	
	print("Want a rematch? I won't hurt this time! \n")
	flagtwo = True
	while (flagtwo):
		ch = input().lower()
		if (ch == "no" or ch == "n" or ch == "nah" or ch == "na"):
			flag = False
			flagtwo = False
			print("Ok Boomer \n")
		elif (ch == "yes" or ch == "ye" or ch =="y"):
			flagtwo = False
			print("Rematch it is!\n")
			
		else:
			print("Let's try answering that again \n")
	
	

print("Computer won " + str(computerwon) + " and " + username[0].upper() + username[1:] +" won " + str(userwon) + ". We had " + str(tie) + " ties.")
print_stats()
f = open(username+".txt", "w")
weights = []
for i in range(agent.noagents - agent.nochanging_agents):
	weights.append((agents[i].index, agents[i].weight))
for agent in changing_agents:
	weights.append((agent.index, agent.weight))
f.write(str(weights) + '\n')
f.write(str([w,l,t,sw,sl,st]))
f.close()
