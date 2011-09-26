#!/usr/bin/env python
# encoding: utf-8
"""
Parameta.py

Created by Masahiro MIYAJI on 2011-09-26.
Copyright (c) 2011 ISDL. All rights reserved.
"""

import random, time

class Parameta:
	"""docstring for Parameta"""
	def __init__(self, random_seed = time.time(), gene_length=100, dimention=2, population_size=10, max_generation=100,
					scaling_method="liner", selection_method="", crossover_method="", mutation_method="", mutation_rate=0.1):
		random.seed(random_seed)
		self.gene_length = gene_length
		self.dimention = dimention
		self.population_size = population_size
		self.max_generation = max_generation
		self.scaling_method = scaling_method
		self.selection_method = selection_method
		self.crossover_method = crossover_method
		self.mutation_method = mutation_method
		self.mutation_rate = mutation_rate
		
def main():
	pass


if __name__ == '__main__':
	main()

