import numpy as np
import sys
from random import randint
import subprocess

L = int(sys.argv[1])

def random_letter(l):
	letter = randint(0,3)
	if letter==0 and l!='A':
		return 'A'
	elif letter==1 and l!='T':
		return 'T'
	elif letter==2 and l!='G':
		return 'G'
	else:
		return 'C'

def generate_sequence(s1):
	s2 = list(s1)
	for i in range(L/10):
		position = randint(0,L-1)
		change = randint(0,1)
		#print("position is %d" % position)
		#print("change is %d" % change)
		if change==0:
			s2[position] = random_letter(s2[position])
		else:
			#print(s2[position])
			del s2[position]

	return s2

'''
create s1 randomly
'''
s1 = []
for i in range(L):
	s1.append(random_letter('z'))

s2 = generate_sequence(s1)
s3 = generate_sequence(s1)

'''
write newly generated sequences to to seq1.fa and seq2.fa
'''
file1 = open("seq1.fa", "w")
file1.write(">GAL1\n" + ''.join(s2))
file2 = open("seq2.fa", "w")
file2.write(">GAL1\n" + ''.join(s3))

file1.close()
file2.close()
# call the align program:
subprocess.call(['python', 'align.py','seq1.fa','seq2.fa','subs.txt','-500'])
#subprocess.call(['python', 'align.py','mel.fa','psd.fa','subs.txt','-500'])
