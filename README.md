Polygnome is a Python package designed and built for my PhD thesis working with noncommutative algebras,
particularly in dealing with the Hochschild cohomology spaces of certain PBW-algebras.

# Contents

[Installation](#installation)

[Usage Examples](#usage-examples)

[Overview of Design](#overview-of-design)

[Polynomials](#polynomials)

[Tensors](#tensors)

[Algebras and Relations](#algebras-and-relations)

# Installation <a name="installation"></a>

Currently the best way to use this is to put the following in a script:

	import sys
	sys.path.append("path/to/polygnome")
	from polygnome import *

Where `path/to/polygnome` should be changed so to reflect the folders location on your drive.

# Usage Examples <a name="usage-examples"></a>
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

# Overview Of Design <a name="overview-of-design"></a>

Polygnome is an object-oriented Python package designed for ease of use with
particular computations in mind. No claims are made for efficiency and I
certainly did not write it using any of the theory of computer algebra that
exists. However, I have used the package extensively and found it perfectly
capable of handling several kinds of non-commutative calculations, in particular
those involving (tensor products of) algebras with "ordered" relations. 

As much as possible, I have tried to make as few algebraic assumptions as
possible. This is a package designed outright for the PBW class of algebras but
it can be used for other algebras if one desires but it may not be the best
place for it. For example, the free algebra is a fundamental building block of
the code.

An overriding design principle is that methods should change an object as little
as possible, choosing to return new objects rather than mutating internal state.
I believe this matches how mathematicians think about mathematical objects; it
certainly matches how I think about them.

## A Note on Fields and Sage 

I have not implemented any fields or code for handling different underlying
fields. This should be doable as using Python hooks in your field definition
will make all of the code I have written mesh with yours but I am not intending
to implement this feature.

A better approach would be to convert this package to a Sage package which I
would be interested in doing in the long term but do not currently have the time
to. If this is something you would like to do I would love to help so please
contact me!


## Class Hierarchy

Every object in Polygnome inherits from an abstract class `polygnomeObject`.
This ensures that every object must know how to print itself as a Python string
and as a Latex string. It is up to you how you use these but I tend to use the
Python string as helpful information for debugging and Latex as something that I
would be happy to place in my thesis.


The next major class in the hierarchy is `arithmeticInterface` which again is an
abstract class that defines the basic methods that any vectors, elements of
algebras, tensors etc. must define. This also defines a method `clean`. The
precise meaning of `clean` is context dependent but the basic idea is to
simplify as much as possible without knowing any of the details of the context.
For example, an element of the free algebra `x+x` would `clean` to `2*x`. 

## Polynomials  <a name="polynomials"></a> 

All polynomials inherit from the `arithmeticInterface`.  #### Composite Pattern
All polynomials and monomials are stored internally as elements of the free
algebra. In order to make seperate the behaviour of polynomials from the
algebras I made the decision that the information about the algebra in which a
polynomial resides should be contained in the brain of the programmer. If you
want to define an algebra in which `x * y` equals `y *x` then you can make an
algebra object containing that information, but it does not change the fact
that `x`, `y` and `x * y` are all instances of `monomial` and carry no
information about relations at all.

Polynomials are implemented using the "Composite" design pattern (see
[wikipedia](https://en.wikipedia.org/wiki/Composite_pattern)).  The class
`abstractPolynomial` is an abstract class that is inherited by both `polynomial`
and `monomial`. The user should not need to know which type of object they are
dealing with internally except in that there are methods that only make sense on
monomials. This is best explained with an example.

Consider the polynomial `x * y * z + z * x * x`. For some reason we want to know
what generators appear as the third factors in any monomials appearing in the
polynomial, to do this we iterate through the monomials and then print the third
factor in each one:
```
x,y,z = generators('x y z')
poly = x * y * z + z * x * x
for mono in poly:
	print mono[2]
```
This will output `z` and `x`. Iterating through a monomial simply returns the monomial itself.

#### Monomials 

Internally a monomial has a list of strings which are the generators of the
algebra. The generators much match the form "\<letter>+\<digits>".  Using
square brackets accesses the list elements as monomials in the usual pythonic
way, in particular you can use slices to get 'submonomials'. For example,
`(x*y*z)[0:2]` is the monomial `x*y`. 

## Tensors <a name="tensors"></a> 

Tensors are implemented using the "Composite" design pattern as polynomials.
Please see the section on Polynomials for a description of this. `pureTensor`
corresponds to `monomial` and `tensor` corresponds to `polynomial`.


#### Pure Tensors 

Instances of `pureTensor` have a list called `monomials` which are the
components of the pure tensor and a field called coefficient. Cleaning the pure
tensor makes all monomials have coefficient one and moves their coefficients
into the coefficient field. 

Accessing a pure tensor using square brackets returns pure tensors with
components corresponding to that sublist in the same way as using them on
monomials.

Currently, pure tensors cannot have components that are polynomials. If you want
to put a polynomial into a tensor you have to iterate through the monomials and
create pure tensors of each etc. This is laborious and is something I am trying
to fix. 

## Algebras and Relations <a name="algebras-and-relations"></a> 

An algebra is really just a list of relations. The algebra then can be used to
'reduce' an polynomial so that it applies relations until no more apply. Recall
that I have assumed the relations are ordered so that they have a leading 'out
of order' term which can be written more 'in order'.

#### Relations 

Relations have three fields: `leadingMonomial`, `lowerOrderTerms` and
`coefficient`. The latter field `coefficient` is really there because of an
unfortunate design problem with pure tensors which is to be fixed. The
important method is `doesAct` which tests whether this relation can reduce a
given monomial. To make this class as simple as possible this is an incredibly
simple-minded method; the method only checks whether the polynomial you pass it
is exactly the `leadingMonomial`.  The `algebra` defined by this relation has
to be a bit smarter to compensate for this.

#### Algebras 

An `algebra` has some relations which it can use to `reduce` a polynomial until
it no longer has any "out of order" monomials. If you choose your relations
badly this can take some time and won't terminate if you have not written your
relations in the correct form (out of order ---> in order). The reduction works
by testing if any relation can act on any of the monomials in a given
polynomial, and then reduces the input using this monomial.

For most users, `reduce` will suffice. However, if one wishes to know the exact
details of the reduction in terms of reduction functions, the methods
`makeReductionSequence` and `reductionSequenceGenerator` will allow one to do
this. If you are unsure of what a generator is in Python just use the first
method. A reduction function was defined by Bergman in his paper on the Diamond
Lemma.


	
