Here is the setup for the problem:

We want to determine if there is enough space within a lake to land a float plane.
More abstractly, the problem is to determine if there is a straight line distance greater than some target value
contained within an arbitrary polygon.

The naive solution, contained within naive.py, is to check the distance between each vertice of the polygon.
The problem with this solution is that it may not be accurate for concave polygons.
It doesn't account for obsticals that may be contained between two vertices.

To run naive.py, make sure you have python3, numpy, and pandas installed. I personally used virtual environment for this.
Next type py naive.py into the command line.
