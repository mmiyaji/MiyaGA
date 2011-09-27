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
		self.eval = 0
		self.parameta = parameta
		if gene:
			self.gene = gene
			# self.gene = []
			# for i in gene:
			# 	self.gene.append(i)
		else:
			self.gene = [random.choice([0,1]) for i in xrange(parameta.gene_length*parameta.dimention)]

	def split_gene(self):
		genes = []
		for j in xrange(0,self.parameta.dimention):
			genes.append(self.gene[self.parameta.gene_length*(j):self.parameta.gene_length*(j+1)])
		return genes

	@staticmethod
	def joint_gene(genes):
		gene = []
		for i in genes:
			gene.extends(i)
		return gene
	
	def gray_to_binary(self):
		binary = []
		binary.append(self.gene[0])
		for i in xrange(1,len(self.gene)):
			binary.append(binary[i-1]^self.gene[i])
		return binary
	
	def gray_to_decimal(self):
		binary = self.gray_to_binary
		return self.binary_to_decimal(binary)
	
	@staticmethod
	def binary_to_decimal(binary):
		decimal = 0
		length = len(binary)
		for i in range(length):
			decimal += binary[i]*(2**(length-i-1))
		return decimal
	
	
	
def main():
	individual = Individual()
	print individual.gene

if __name__ == '__main__':
	main()

