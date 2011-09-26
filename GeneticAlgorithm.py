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
			self.show_evaluations()

	def show_evaluations(self):
		for i in self.genes:
			print self.calc_decimal(i.gene),
			
	def isfinish(self, count = 1):
		if self.parameta.max_generation <= count:
			return True
		else:
			return False

	def evaluation(self, gene):
		return self.rastrigin(gene)

	@staticmethod
	def rastrigin(ary):
		value = 0.0
		for i in range(len(ary)):
			value += ary[i] * ary[i] - 10 * math.cos(2 * math.pi * ary[i])
		return 10 * len(ary) + value

	def selection(self):
		result = []
		if self.parameta.selection_method is "roulette":
			rate_sum = 0
			# for i in self.gene:
			# 	rate_sum += self.
		return result

	def crossover(self):
		if self.parameta.crossover_method is "single":
			selected = self.selection
			
	
	def mutation(self):
		if self.parameta.mutation_method is "normal":
			pass
	
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
	
	def calc_decimal(self, gray):
		arr = []
		for i in self.split_gene(gray):
			arr.append(self.scaling(self.binary_to_decimal(self.gray_to_binary(i)), -5.12, 5.12))
		return self.evaluation(arr)
	
	@staticmethod
	def gray_to_binary(gray):
		binary = []
		binary.append(gray[0])
		for i in xrange(1,len(gray)):
			binary.append(binary[i-1]^gray[i])
		return binary
	
	@staticmethod
	def binary_to_decimal(binary):
		decimal = 0
		length = len(binary)
		for i in range(length):
			decimal += binary[i]*(2**(length-i-1))
		return decimal
	
	
def main():
	para = Parameta(random_seed=1)
	ga = GeneticAlgorithm(para)
	print ga.gray_to_binary([1,1,1,1])
	generation = 0
	while not ga.isfinish(generation):
		generation +=1
		print "Generation:",generation
		if deb:
			ga.show_evaluations()
		ga.crossover()
		ga.mutation()
	print "finish:",ga.show_evaluations()

if __name__ == '__main__':
	main()
