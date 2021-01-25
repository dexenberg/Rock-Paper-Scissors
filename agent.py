from collections import deque
from numpy import random
import math

miu = 0.25
k = 2
e = math.e
history_len = 20

class Agent:
	p_r = 1/3;
	p_s = 1/3;
	p_p = 1/3;
	change_after = ''
	p_stay = 1/3;
	p_cwise = 1/3;
	p_ccwise = 1/3;
	weight = 1.0;
	# history = deque([], maxlen = history_len)
	def __init__(self, ind, r = 1/3, p = 1/3, s = 1/3, w = 1, last_battle = -2, p_stay = 1/3, p_ccwise = 1/3, p_cwise = 1/3):
		self.index = ind;
		self.p_r = r;
		self.p_p = p;
		self.p_s = s;
		self.change_after = last_battle
		self.weight = w;
		self.p_stay = p_stay
		self.p_ccwise = p_ccwise
		self.p_cwise = p_cwise
		# self.history = deque([], maxlen = history_len)
	def change_probabilities(self, lastinput):
		if (lastinput == 'r'):
			self.p_r = self.p_stay
			self.p_p = self.p_cwise
			self.p_s = self.p_ccwise
		elif (lastinput == 'p'):
			self.p_r = self.p_ccwise
			self.p_p = self.p_stay
			self.p_s = self.p_cwise
		elif (lastinput == 's'):
			self.p_r = self.p_cwise
			self.p_p = self.p_ccwise
			self.p_s = self.p_stay
	# def update_loss(self):
		# self.weight = self.weight * (1 - miu)
	# def update_tie(self):
		# self.weight = self.weight
	# def update_win(self):
		# self.weight = self.weight / (1 - miu)
	def predict_against(self):
		e_p = self.p_r - self.p_s
		e_s = self.p_p - self.p_r
		e_r = self.p_s - self.p_p
		dict = {e_p : 'p', e_s : 's', e_r : 'r'}
		maxim = max(e_p, e_s, e_r)
		return dict[maxim]
	def update(self, user_guess):
		dict = {'r' : self.p_r, 'p' : self.p_p, 's' : self.p_s} 
		coefficient =  (dict[user_guess] - 1 ) * (- e**(-k) + 1) + 1     # between e^-k and 1
		# print(self.p_r, self.p_p, self.p_s, coefficient)
		weight_update = 1 + miu * math.log(coefficient)
		# if (len(self.history) == history_len):
			# self.weight = self.weight/self.history[0]
		# self.history.append(weight_update)
		self.weight = self.weight * weight_update
	def classic_update(self, user_guess):
		dict = {'r' : self.p_r, 'p' : self.p_p, 's' : self.p_s} 
		agent = self.predict_against()
		# if (len(self.history) == history_len):
			# self.weight = self.weight/self.history[0]
		weight_update =  1 + miu * k * (battle(agent, user_guess) - 1) / 2
		# self.history.append(weight_update)
		self.weight = self.weight * weight_update
			
	# def update2(self, user_guess):
		# pw, pt, pl = wtl(self, user_guess)
		# coefficient = pw + pt/2 - pl;        # we scale coefficient from -1, 1 to the interval e^-k , 0 and then extract the log
		# a = (e**k + 1)/(e**k - 1)
		# b = a + 1
		# coefficient = (coefficient + a)/b
		# self.weight = self.weight * (1 + miu * math.log(coefficient))
		# print(1 + miu*math.log(coefficient))

def guess(agents):         # returns index of agent chosen
	prob = [agents[i].weight for i in range(len(agents))] 
	prob = [prob[i]/sum(prob) for i in range(len(agents))]
	#print(prob)
	return random.choice([i for i in range(len(agents))], p = prob)


def decide(agents, trials):
	rps = {'r': 0, 's' : 0, 'p' : 0}
	for i in range(trials):
		agent_index = guess(agents)                    # select my agent according to the weights
		myagent = agents[agent_index]
		w = [agent.weight for agent in agents]
		# print(myagent.p_r, myagent.p_p, myagent.p_s, myagent.change_after, myagent.weight/sum(w))
		mychoice = myagent.predict_against()
		rps[mychoice] += 1
	print(rps)
	if (rps['r'] > rps['s'] and rps['r'] > rps['p']):
		return 'r'
	elif (rps['s'] > rps['p']):
		return 's'
	return 'p'
	
def update(agents, user, turn):  # updates the weight of the agent according to the previous performance
	for i in range(len(agents)):
		if (turn == 1 and 66<=i and i<66*2):         # we dont update those static agents on this turn
			continue
		agents[i].update(user)
	pass
	# for i in range(noagents):
		# if (battle(predictions[i], user) == 1):
			# agents[i].update_win()
		# elif (battle(predictions[i], user) == 0):
			# agents[i].update_tie()
		# else:
			# agents[i].update_loss()
	# pass
	
noagents = 0;
nochanging_agents = 0;
	
	
def create_agents(agents, weights):              # create agents with all probabilities
	global noagents
	for i in range(11):
		for j in range(11 - i):
			# print(i/10 , j/10 , (10 - i - j)/10)
			new_agent = Agent(noagents, r = i/10, p = j/10, s = (10 - i - j)/10, w = weights[noagents][1])
			noagents += 1;
			agents.append(new_agent)
	for i in range(11):
		for j in range(11 - i):
			new_agent = Agent(noagents, r = i/10, p = j/10, s = (10 - i - j)/10, w=weights[noagents][1], last_battle = -2 , p_stay = i/10, p_ccwise = j/10, p_cwise = (10 - i - j)/10)
			noagents += 1
			agents.append(new_agent)
			
def create_changing_agents(changing_agents, weights):    # create agents that change according to the output of the last battle
	global noagents
	global nochanging_agents
	for lb in range(-1,2):
		for i in range(11):
			for j in range(11 - i):
				new_agent = Agent(noagents, w=weights[noagents][1], last_battle = lb, p_stay = i/10, p_ccwise = j/10, p_cwise = (10 - i - j)/10)
				noagents += 1
				nochanging_agents += 1
				changing_agents.append(new_agent)
	for lb in range(-1,2):
		for i in range(11):
			for j in range(11 - i):
				new_agent = Agent(noagents, r = i/10, p = j/10, s = (10 - i -j)/10, w=weights[noagents][1], last_battle = lb)  # last battle
				noagents += 1
				nochanging_agents += 1
				changing_agents.append(new_agent)
	for lb in range(-1,2):
		for i in range(11):
			for j in range(11 - i):
				new_agent = Agent(noagents, r = i/10, p = j/10, s = (10 - i -j)/10, w=weights[noagents][1], last_battle = lb + 3) # last symbol played by user
				noagents += 1
				nochanging_agents += 1
				changing_agents.append(new_agent)
	for lb in range(-1,2):
		for i in range(11):
			for j in range(11 - i):
				new_agent = Agent(noagents, r = i/10, p = j/10, s = (10 - i -j)/10, w=weights[noagents][1], last_battle = lb + 6) # last symbol played by computer
				noagents += 1
				nochanging_agents += 1
				changing_agents.append(new_agent)
