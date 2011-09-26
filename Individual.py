#!/usr/bin/env python
# encoding: utf-8
"""
Individual.py

Created by Masahiro MIYAJI on 2011-09-26.
Copyright (c) 2011 ISDL. All rights reserved.
"""

import random
from Parameta import *

class Individual:
	"""docstring for Individual"""
	def __init__(self, id = 0, parameta = Parameta(), gene = None):
		self.id = id
		self.parameta = parameta
		if gene:
			self.gene = gene
		else:
			self.gene = [random.choice([0,1]) for i in xrange(parameta.gene_length*parameta.dimention)]
		
def main():
	individual = Individual()
	print individual.gene

if __name__ == '__main__':
	main()

