#!/usr/bin/env python
# encoding: utf-8
"""
GeneticAlgorithm.py

Created by Masahiro MIYAJI on 2011-09-23.
Copyright (c) 2011 ISDL. All rights reserved.
"""

import random, math
from Parameta import *
from Individual import *

deb = True

class GeneticAlgorithm:
	"""docstring for GeneticAlgorithm"""
	def __init__(self, parameta = Parameta()):
		self.parameta = parameta
		# self.genes = [Individual(id=i, parameta=self.parameta) for i in xrange(self.parameta.population_size)]
		self.genes = [Individual(id=i, parameta=self.parameta) for i in xrange(self.parameta.population_size)]
		if deb:
			print "Initial individuals:"
			for i in self.genes:
				for i in self.split_gene(i.gene):
					print self.binary_to_gray(i), self.scaling(self.binary_to_gray(i), -5.12, 5.12)

	def scaling(self, val, min, max):
		length = self.parameta.gene_length
		if self.parameta.scaling_method is "liner":	
			value = -max + (val / (math.pow(2,length)-1)) * (max-min)
		else:
			value = 0
			print "error"
		return value
	
	def split_gene(self, gene):
		genes = []
		for j in xrange(0,self.parameta.dimention):
			genes.append(gene[self.parameta.gene_length*(j):self.parameta.gene_length*(j+1)])
		return genes

	@staticmethod
	def joint_gene(genes):
		gene = []
		for i in genes:
			gene.extends(i)
		return gene
	
	@staticmethod
	def binary_to_gray(binary):
		print binary
		decimal = 0
		length = len(binary)
		for k in range(length):
			decimal += binary[k]*(2**(length-k-1))
		return decimal
	
	@staticmethod
	def gray_to_binary(gray):
		binary = [0] * len(gray)
		binary[0] = gray[0]
		for i in range(len(gray)):
			binary[i] = binary[i-1]^gray[i]
		return binary
	
def main():
	para = Parameta(random_seed=1)
	ga = GeneticAlgorithm(para)
	
	
	
	
	
	


if __name__ == '__main__':
	main()
