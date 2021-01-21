#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sks_quiz_v1.py
Kleines Quiz um die SKS-Theoriefragen zu üben. Alle Fragen kommen von ELWIS (https://www.elwis.de/DE/Sportschifffahrt/Sportbootfuehrerscheine/Fragenkatalog-SKS/Fragenkatalog-SKS-node.html)
Date: 21/01/2021
License: MIT
"""

import csv
import pickle
import random


pkl_path = 'sks_questions.pkl'

class Question:
	def __init__(self, category, number, question, answer, right_count, wrong_count, ask_count):
		self.category = category
		self.number = number
		self.question = question
		self.answer = answer
		self.right_count = right_count
		self.wrong_count = wrong_count
		self.ask_count = ask_count

	def ask(self):
		self.ask_count += 1
		print(self.category)
		print(str(self.number) + '. ' + self.question)
		i = input('Antwort: ')
		if i == 'q':
			print('Quitting')
			save_object(quiz.questions, pkl_path)
			quit()
			
		for a in self.answer:
			print(a)
		return input('Richtige Antwort? y/n ')


class Quiz:
	def __init__(self, questions):
		self.questions = questions

	def analyse_input(self, input, question, q_index):
		if input == 'y':
			question.right_count += 1
		elif input == 'n':
			question.wrong_count += 1
		elif input == 'q':
			# save q list to pickle
			save_object(self.questions, pkl_path)
			quit()
		self.questions[q_index] = question
		print('Richtig: ' + str(question.right_count)+ ' Falsch: ' + str(question.wrong_count))
	
	def all(self):
		for n, q in enumerate(self.questions):
			i = q.ask()
			self.analyse_input(i, q, n)
			# save q list to pickle
			save_object(self.questions, pkl_path)
	
	def category(self, cat):		
		questions = self.questions_categorised()
		if cat == 'n':
			idx = 0
		elif cat == 'r':
			idx = 1
		elif cat == 'w':
			idx = 2
		elif cat == 's':
			idx = 3
		for n, q in enumerate(questions[idx]):
			i = q.ask()
			self.analyse_input(i, q, n)
		# save q list to pickle
		save_object(self.questions, pkl_path)

	def random(self):
		ask = True
		while ask:
			idx = random.randint(0, len(question_list))
			q = self.questions[idx]
			i = q.ask()
			self.analyse_input(i, q, idx)
			# save q list to pickle
			save_object(self.questions, pkl_path)
			
	def wrongest(self):
		sorted_q = sorted(self.questions, key=lambda x: x.wrong_count, reverse=True)
		for n, q in enumerate(sorted_q):
			i = q.ask()
			self.analyse_input(i, q, n)
			# save q list to pickle
			save_object(self.questions, pkl_path)

	def rarest(self):
		sorted_q = sorted(self.questions, key=lambda x: x.ask_count)
		for n, q in enumerate(sorted_q):
			i = q.ask()
			self.analyse_input(i, q, n)
			# save q list to pickle
			save_object(self.questions, pkl_path)
	
	def questions_categorised(self):
		nav_qs = [q for q in self.questions if q.category == 'navigation']
		law_qs = [q for q in self.questions if q.category == 'schifffahrtsrecht']
		weather_qs = [q for q in self.questions if q.category == 'wetterkunde']
		sm_qs = [q for q in self.questions if q.category == 'seemannschaft1' or q.category == 'seemannschaft2']
		
		return nav_qs, law_qs, weather_qs, sm_qs
	
	
			
		
# Open / save pickle
def save_object(obj, filename):
	with open(filename, 'wb') as output:  # Overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def open_object(filename):
	with open(filename, 'rb') as input:
		return pickle.load(input)

# main		
if __name__ == "__main__":
	question_list = open_object(pkl_path)

	print("""SKS Quiz
	a - Alle Fragen
	k - Kategorie
	z - zufällige Fragen
	f - schlechteste Fragen zuerst
	s - seltendste Fragen
	q - Beenden
	""")
	i = input('Auswahl... ')

	quiz = Quiz(question_list)

	if i == 'a':
		quiz.all()

	elif i == 'k':
		print("""Kategorien
		n - Navigation
		r - Seefahrtsrecht
		s - Seemannschaft 1 & 2
		w - Wetterkunde
		""")
		c = input('Kategorie... ')
		quiz.category(c)

	elif i == 'z':
		quiz.random()

	elif i == 'f':
		quiz.wrongest()

	elif i == 's':
		quiz.rarest()
