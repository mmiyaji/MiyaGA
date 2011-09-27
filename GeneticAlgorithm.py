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
		self.genes = [Individual(id=i, parameta=self.parameta) for i in xrange(self.parameta.population_size)]
		if deb:
			print "Initial individuals:"
			self.show_evaluations()

	def show_evaluations(self):
		sum = 0
		for i in self.genes:
			res = self.evaluation(i.gene)
			# print "#",res,i.gene
			sum += res
		# print 
		# print sum/len(self.genes)
		
	def isfinish(self, count = 1):
		if self.parameta.max_generation <= count:
			return True
		else:
			return False

	def evaluation(self, gene):
		# return self.onemax(gene)
		arr = []
		for i in self.split_gene(gene):
			# print "I:",i,
			j = self.gray_to_binary(i)
			# print "J:",j,
			k = self.binary_to_decimal(j)
			# print "K:",k,
			s = self.scaling(k, -5.12, 5.12)
			# print "S:",s
			arr.append(s)
		# print arr
		return self.rastrigin(arr)
	
	@staticmethod
	def onemax(gene):
		value = 0
		for i in gene:
			if i == 1:
				value += 1
		return -value
	
	@staticmethod
	def rastrigin(ary):
		value = 0.0
		for i in ary:
			value += i * i - 10 * math.cos(2 * math.pi * i)
		return 10 * len(ary) + value

	def selection(self):
		result = []
		if self.parameta.selection_method is "roulette":
			rate_sum = 0
			# for i in self.gene:
			# 	rate_sum += self.
		elif self.parameta.selection_method is "tournament":
			choices = random.sample(self.genes, self.parameta.tournament_size)
			sorted_choices = sorted(choices,key=lambda x: self.evaluation(x.gene),reverse=False)
			# for i in sorted_choices:
			# 	print self.calc_decimal(i.gene),
			result = sorted_choices[:2]
			# print "####"
			# for i in result:
			# 	print self.calc_decimal(i.gene),
			# print "$$$$"
			# print self.evaluation(result[1].gene)
		return result

	def crossover(self):
		if self.parameta.crossover_method is "single":
			genes = []
			eliets = sorted(self.genes,key=lambda x: self.evaluation(x.gene),reverse=False)[:2]
			# for i in eliets:
			# 	print "E:",self.evaluation(i.gene)
			print self.evaluation(eliets[0].gene), ",", 
			for i in self.split_gene(eliets[0].gene):
				# print "I:",i,
				j = self.gray_to_binary(i)
				# print "J:",j,
				k = self.binary_to_decimal(j)
				# print "K:",k,
				s = self.scaling(k, -5.12, 5.12)
				print s,
			# for i in eliets[0].gene:
			# 	print i,
			print 
			genes.append(Individual(id=eliets[0].id, parameta=self.parameta, gene = eliets[0].gene))
			genes.append(Individual(id=eliets[1].id, parameta=self.parameta, gene = eliets[1].gene))
			for i in xrange(self.parameta.population_size - int(math.ceil(self.parameta.eliet_rate/2.0))):
				point = random.randint(1,(self.parameta.gene_length*self.parameta.dimention)-1)
				selected = self.selection()

				if self.parameta.crossover_rate > random.random():
					gene1 = selected[0].gene[point:] + selected[1].gene[:point]
					gene2 = selected[1].gene[point:] + selected[0].gene[:point]
				else:
					gene1 = selected[0].gene
					gene2 = selected[1].gene
				genes.append(Individual(id=selected[0].id, parameta=self.parameta, gene = gene1))
				genes.append(Individual(id=selected[1].id, parameta=self.parameta, gene = gene2))
			self.genes = genes

	def mutation(self):
		if self.parameta.mutation_method is "normal":
			# for i in xrange(self.parameta.population_size):
			for i in self.genes:
				if self.parameta.mutation_rate > random.random():
					point = random.randint(0,(self.parameta.gene_length*self.parameta.dimention)-1)
					if i.gene[point]:
						i.gene[point] = 0
					else:
						i.gene[point] = 1
	
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
	para = Parameta(random_seed=None, gene_length=100, dimention=2, population_size=4, 
					tournament_size=2, max_generation=100, mutation_rate=0.2)
	ga = GeneticAlgorithm(para)
	# print ga.gray_to_binary([1,1,1,1])
	generation = 0
	while not ga.isfinish(generation):
		generation +=1
		# print "Generation:",generation,
		print generation,",",
		if deb:
			ga.show_evaluations()
		ga.crossover()
		ga.mutation()
	print "finish:",
	ga.show_evaluations()
	# print "LAST"
	# print ga.rastrigin([0,0])
	# para = Parameta(random_seed=3, gene_length=3, dimention=2, population_size=5, 
	# 				tournament_size=5, max_generation=1)
	# ga = GeneticAlgorithm(para)
	# # print ga.gray_to_binary([1,1,1,1])
	# point = random.randint(1,(para.gene_length*para.dimention)-1)
	# selected = [Individual(id=1, parameta=para, gene=[1,1,1,1,1,1]),Individual(id=2, parameta=para, gene=[0,0,0,0,0,0])]
	# 
	# gene1 = selected[0].gene[point:] + selected[1].gene[:point]
	# gene2 = selected[1].gene[point:] + selected[0].gene[:point]
	# 
	# selected[0].gene = gene1
	# selected[1].gene = gene2
	# print gene1, selected[0].gene
	# print gene2, selected[1].gene

if __name__ == '__main__':
	main()
