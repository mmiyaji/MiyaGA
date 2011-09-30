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
		# if deb:
		# 	#print "Initial individuals:"
		# 	self.show_evaluations()
	
	def get_eliet(self, num = 1):
		eliets = sorted(self.genes,key=lambda x: self.evaluation(x.gene),reverse=False)[:num]
		return eliets
	
	def show_eliet(self, num = 1):
		eliets = self.get_eliet(num)
		for i in eliets:
			print self.evaluation(i.gene),",\t",
			for m in i.split_gene():
				# print "I:",i,
				j = self.gray_to_binary(m)
				# print "J:",j,
				k = self.binary_to_decimal(j)
				# print "K:",k,
				s = self.scaling(k, -5.12, 5.12)
				print s,",\t",
			# print self.evaluation(i.gene),
			# for j in i.gene:
			# 	print j,",",
		print 
		
	def fileout_plots(self):
		sum = 0
		string = ""
		for i in self.genes:
			res = self.evaluation(i.gene)
			string += str(res) + ", "
			# print res,",",
			for m in i.split_gene():
				j = self.gray_to_binary(m)
				# print "J:",j,
				k = self.binary_to_decimal(j)
				# print "K:",k,
				s = self.scaling(k, -5.12, 5.12)
				# print s,",",
				string += str(s) + ", "
			# print "#",i.id,res,i.gene
			string += "\n"
			# sum += res
		# print string
		return string
		# print sum/len(self.genes)
	
	def show_evaluations(self):
		sum = 0
		for i in self.genes:
			res = self.evaluation(i.gene)
			print res,",",
			# print "#",i.id,res,i.gene
			# sum += res
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
			# print "#",s,",",
			
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
		genes = []
		eliets = self.get_eliet(2)
		genes.append(Individual(id=eliets[0].id, parameta=self.parameta, gene = eliets[0].gene))
		genes.append(Individual(id=eliets[1].id, parameta=self.parameta, gene = eliets[1].gene))

		if self.parameta.crossover_method is "single":
			# for i in xrange(int(math.ceil((self.parameta.population_size - self.parameta.eliet_rate)/2.0))):
			while True:
				if len(genes) >= self.parameta.population_size:
					break
				point = random.randint(1,(self.parameta.gene_length*self.parameta.dimention)-1)
				selected = self.selection()
				if self.parameta.crossover_rate > random.random():
					gene1 = selected[0].gene[:point] + selected[1].gene[point:]
					gene2 = selected[1].gene[:point] + selected[0].gene[point:]
				else:
					gene1 = selected[0].gene
					gene2 = selected[1].gene
				genes.append(Individual(id=selected[0].id, parameta=self.parameta, gene = gene1))
				genes.append(Individual(id=selected[1].id, parameta=self.parameta, gene = gene2))
			self.genes = genes
		elif self.parameta.crossover_method is "multi":
			cross_times = self.parameta.crossover_point
			while True:
				if len(genes) >= self.parameta.population_size:
					break
				# point = random.randint(1,(self.parameta.gene_length*self.parameta.dimention)-1)
				points = random.sample(xrange(self.parameta.gene_length*self.parameta.dimention-2),cross_times)
				selected = self.selection()
				if self.parameta.crossover_rate > random.random():
					for i in points:
						point = i + 1
						# print point,
						gene1 = selected[0].gene[:point] + selected[1].gene[point:]
						gene2 = selected[1].gene[:point] + selected[0].gene[point:]
				else:
					gene1 = selected[0].gene
					gene2 = selected[1].gene
				genes.append(Individual(id=selected[0].id, parameta=self.parameta, gene = gene1))
				genes.append(Individual(id=selected[1].id, parameta=self.parameta, gene = gene2))
			self.genes = genes
				
				
			# print "!"
			# self.show_evaluations()
			# print "%"
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
			value = -max + (val / (math.pow(2,length))) * (max-min)
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
	para = Parameta(random_seed=None, gene_length=100, dimention=10, population_size=400, 
					crossover_method="multi",
					tournament_size=4, max_generation=500, mutation_rate=0.1,crossover_rate=1.0, eliet_rate=4)
	ga = GeneticAlgorithm(para)
	# print ga.gray_to_binary([1,1,1,1])
	generation = 0
	while not ga.isfinish(generation):
		generation +=1
		# print "Generation:",generation,
		print generation,",",
		if deb:
			# ga.show_evaluations()
			ga.show_eliet()
			# f = open("log/Ruhenheim/animation02/animate_"+str(generation)+".csv","w")
			# f.write(ga.fileout_plots())
			# f.close()
		ga.crossover()
		ga.mutation()
	# print "finish:",
	# ga.show_evaluations()
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
