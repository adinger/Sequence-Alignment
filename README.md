Calculates the best global alignment of two gene sequences using a dynamic programming scoring matrix.
Built with Python 2.

### Usage 

`seq1.fa` and `seq2.fa` contain the two gene sequences. They are assumed to be the same length.

Run the following, replacing sequence-length with the length of the sequences, which are assumed to be the same.
```
python create_data_and_align.py [sequence-length]
```

Example:
```
python create_data_and_align.py 100
```

### Output
A .txt file containing the highest-scoring alignment of the two gene sequences.
