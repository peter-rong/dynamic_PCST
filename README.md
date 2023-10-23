# dynamic PCST
This is the repo for a mutant problem to the traditional price collecting steiner tree problem where nodes hold both the cost and the reward. And we are changing the threshold to see change in performance. Implementation is complete. 

# Input text tile format:
The output file has the format:
- number of MA vertices (integer)
- list of vertex coordinates (2 floats per line, one line for each vertex)
- number of MA edges (integer)
- list of vertex indices and angles (2 integers + 1 float per line : angle measure of that edge), one line for each edge, indexing from 0)

# Usage: 

python3 main.py filename.txt

("filename.txt" is the input text file that contains information about the Medial Axis.)

# Output file format: 

Stored in output.txt
The output file has the format:
- list of lowest threshold needed to drop the edge, one line for each edge
