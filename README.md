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
	from polygnome import *
	x,y,z = generators('x y z')
	commutativeRelations =(relation(y * x, x * y), relation(z * x, x * z), relation(z * y, y * z))
	commutativeAlgebra = algebra(commutativeRelations)
	print commutativeAlgebra.reduce(z * y * x) # prints xyz


