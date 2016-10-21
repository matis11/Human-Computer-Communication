from sympy.interactive import printing
import sympy as sym

printing.init_printing(use_latex=True)

# Definicje zmiennych
x, y = sym.symbols("x y")

eq = sym.Eq(x ** 3 - 3 * x ** 2 - 13 * x - 15)