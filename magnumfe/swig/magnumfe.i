%module(package="magnumfe") cpp

%{
#include "Mesher.h"
#include "SubMeshInterpolator.h"
#include "DofForm.h"
#include "CGDofForm.h"
#include "DofAssembler.h"
#include "ScalarProductMatrix.h"
#include "ScalarProductMatrix2.h"
#include "TransScalarProductMatrix.h"
#include "NormalizedVector.h"
%}

// Handle NumPy and Dolfin Arrays
%{
#include <numpy/arrayobject.h> 
#define SWIG_SHARED_PTR_QNAMESPACE boost
%}

%include <exception.i>

%init%{
import_array();
%}

%import "typemaps/numpy.i"
%import "typemaps/array.i"
%import "typemaps/std_map.i"
%import "typemaps/primitives.i"

// Handle Strings
%include <std_string.i>

// Handle Shared Pointers
%include <std_shared_ptr.i>
%shared_ptr(dolfin::FunctionSpace)
%shared_ptr(dolfin::GenericTensor)
%shared_ptr(dolfin::GenericVector)
%shared_ptr(dolfin::GenericMatrix)
%shared_ptr(dolfin::GenericFunction)
%shared_ptr(dolfin::Mesh)

// don't create interface for eval methods
%ignore magnumfe::DofForm::nodeEval;
%ignore magnumfe::DofForm::eval;
%ignore magnumfe::CGDofForm::nodeEval;
%ignore magnumfe::CGDofForm::eval;

// Include headers
%include "Mesher.h"
%include "SubMeshInterpolator.h"
%include "DofForm.h"
%include "CGDofForm.h"
%include "DofAssembler.h"
%include "ScalarProductMatrix.h"
%include "ScalarProductMatrix2.h"
%include "TransScalarProductMatrix.h"
%include "NormalizedVector.h"

// vim:ft=cpp:
