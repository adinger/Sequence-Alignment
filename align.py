import numpy as np
import sys
'''
read in program arguments
'''
fasta_file1 = sys.argv[1]
fasta_file2 = sys.argv[2]
sub_matrix_file = sys.argv[3]
gap_penalty = int(sys.argv[4])
print(type(fasta_file1))

'''
extract sequences and their lengths to use as dimensions for matrix
'''
file1 = open(sys.argv[1], "r")
lines1 = file1.readlines()
len1 = len(lines1[1])
seq1 = "0"+lines1[1]

file2 = open(sys.argv[2], "r")
lines2 = file2.readlines()
len2 = len(lines2[1])
seq2 = "0"+lines2[1]

'''
parse sub.txt into a matrix
'''
sub_matrix_file = sys.argv[3]

'''
create matrix of scores and previous directions (for backtracing)
'''
scores = np.ndarray((len2+1, len1+1), dtype=int)
prevdirs = np.ndarray((len2+1, len1+1), dtype=object)

'''
create matrix of substitution rules
'''
def parse_subs_file(subsfile):
	ret = []
	lines = subsfile.readlines()
	for i in range(1,5):
		ret.append(lines[i].split()[1:])
	return ret

subs = parse_subs_file(open(sys.argv[3]))

print(len1, len2)
def find_score(r,c):
	result = 0
	l1 = seq1[c]
	l2 = seq2[r]

	if (l1 == l2):
		if (l1 == 'A'):
			result = subs[0][0]
		elif (l1 == 'C'):
			result = subs[1][1]
		elif (l1 == 'G'):
			result = subs[2][2]
		elif (l1 == 'T'):
			result = subs[3][3]
	elif ((l1=='A' and l2=='C') or (l2=='A' and l1=='C')):
		result = subs[0][1]
	elif ((l1=='A' and l2=='G') or (l2=='A' and l1=='G')):
		result = subs[0][2]
	elif ((l1=='A' and l2=='T') or (l2=='A' and l1=='T')):
		result = subs[0][3]
	elif ((l1=='C' and l2=='G') or (l2=='C' and l1=='G')):
		result = subs[1][2]
	elif ((l1=='C' and l2=='T') or (l2=='C' and l1=='T')):
		result = subs[1][3]
	elif ((l1=='G' and l2=='T') or (l2=='G' and l1=='T')):
		result = subs[2][3]

	return (scores[r-1][c-1] + int(result))


'''
@param (int)left, (int)upper, (int)diagonal
@return (int)max, (char)dir
'''
def find_score_and_prevdir(r,c):
	left = scores[r,c-1] + gap_penalty
	upper = scores[r-1,c] + gap_penalty
	diagonal = find_score(r,c)

	max = left
	dir = 'l'
	if upper > max:
		max = upper
		dir = 'u'
	if diagonal > max:
		max = diagonal
		dir = 'd'

	scores[r,c] = max
	prevdirs[r,c] = dir

'''
populate matrix 
(seq1 is horizontal 'axis', seq2 is vertical 'axis')
'''
# fill out col1 and row1 w/negative even numbers
val = 0
for c in range(len1+1):
	scores[0][c] = val
	val += gap_penalty

val = 0
for c in range(len2+1):
	scores[c][0] = val
	val += gap_penalty

#print(scores)
for r in range(1,len2+1):
	for c in range(1,len1+1):
		find_score_and_prevdir(r,c)
		#print(scores[r,c], prevdirs[r,c])

#print("The score is ", scores[-1][-1])
#print(scores)
'''
backtracing

initialize a list to store directions

start from bottom-right-most cell:
'''
output1 = []
output1.append(seq1[-1])
output2 = []
output2.append(seq2[-1])
path = []
r = len2
c = len1

while r > 1 and c > 1:
	path.append(prevdirs[r,c])
	if prevdirs[r,c] == 'l':
		output1.append(seq1[c-1])
		output2.append('-')
		c -= 1
	elif prevdirs[r,c] == 'u':
		output1.append('-')
		output2.append(seq2[r-1])
		r -= 1
	elif prevdirs[r,c] == 'd':
		output1.append(seq1[c-1])
		output2.append(seq2[r-1])
		r -= 1
		c -= 1

output1.reverse()
output2.reverse()
print(" ".join(output1))
print(" ".join(output2))
print("Score = %d" % scores[-1][-1])
