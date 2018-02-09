#rewrite in c
#It will be used very frequantly. 
from MonteCarloTreeSearch import Node

'''
def PUCT(node,constant):
	"""Variant of PUCT algorithm
	   where cpuct is a constant determining the level of exploration; this search control
	   strategy initially prefers actions with high prior probability and low visit count, but
	   asympotically prefers actions with high action value"""

	return constant*node.prior_probability*((sum(???))**(1/2))/(1+node.visit_count)
'''



def UCB1(node,constant):
	pass	


def UCT(node,constant):
	""" 

	"""
	return node.value / node._count + constant * sqrt(log(node.parent.visit_count) / node.visit_count)

	
