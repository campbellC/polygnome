Polygnome
---------------

Polygnome is a package designed and built for my PhD thesis working with noncommutative algebras, particularly in dealing with the Hochschild cohomology spaces of certain PBW-algebras.


Installing
-------------
Currently the best way to use this is to put the following in a script:

	import sys
	sys.path.append("path/to/polygnome")
	from polygnome import *

Where `path/to/polygnome` should be changed so to reflect the folders location on your drive.

Examples
---------------
A simple reduction:

	from polygnome import *
	x,y,z = generators('x y z')
	commutativeRelations =(relation(y * x, x * y), relation(z * x, x * z), relation(z * y, y * z))
	commutativeAlgebra = algebra(commutativeRelations)
	print commutativeAlgebra.reduce(z * y * x) # prints xyz


A noncommutative reduction in the quantum plane:
	
	from polygnome import *
	x, y = generators('x y')
	qCommutationRelation = relation(y * x, 'q' * x * y) # alternatively coefficient('q')
	quantumPlane = algebra(qCommutationRelation)
	print quantumPlane.reduce( (y ** 2) * x + 2).toLatex() 
	# prints "qqxy^{2} + 2"

An example of a function on the tensor product of an algebra with itself:

	from polygnome import *

	x, y = generators('x y')
	qCommutationRelation = relation(y * x, 'q' * x * y)
	quantumPlane = algebra(qCommutationRelation)
	
	SecondBarSpace = tensorAlgebra([quantumPlane,quantumPlane])

	@bimoduleMapDecorator(SecondBarSpace, quantumPlane)
	def multiplicationMap(ab):
		a = ab[0]
		b = ab[1]
		return a * b
	
	poly = pureTensor(y * x).tensorProduct(x) + pureTensor(x * y).tensorProduct(y) 
	print multiplicationMap(poly)
outputs qqxxy+xyy. Note the decorator extends the definition of the map bilinearly, and takes in
the domain and the codomain so that it can reduce the output.




	
