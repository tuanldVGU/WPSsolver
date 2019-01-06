from gekko import GEKKO

m = GEKKO()
m.options.SOLVER=1  # APOPT is an MINLP solver

# optional solver settings with APOPT
m.solver_options = ['minlp_maximum_iterations 500', \
                    # minlp iterations with integer solution
                    'minlp_max_iter_with_int_sol 10', \
                    # treat minlp as nlp
                    'minlp_as_nlp 0', \
                    # nlp sub-problem max iterations
                    'nlp_maximum_iterations 50', \
                    # 1 = depth first, 2 = breadth first
                    'minlp_branch_method 1', \
                    # maximum deviation from whole number
                    'minlp_integer_tol 0.05', \
                    # covergence tolerance
                    'minlp_gap_tol 0.01']

#initial variables
x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21,x22,x23,x24 = [m.Var(value = 0, integer=True) for i in range(1,25)]

#initial value
print x5.value

#Equations
m.Equation(x15+x16+x17+x18+x21+x22+x23+x24>=20)
m.Equation(x16+x17+x18+x19+x22+x23+x24+x1>=20)
m.Equation(x17+x18+x19+x20+x23+x24+x1+x2>=20)
m.Equation(x18+x19+x20+x21+x24+x1+x2+x3>=16)
m.Equation(x19+x20+x21+x22+x1+x2+x3+x4>=16)
m.Equation(x20+x21+x22+x23+x2+x3+x4+x5>=16)
m.Equation(x21+x22+x23+x24+x3+x4+x5+x6>=25)
m.Equation(x22+x23+x24+x1+x4+x5+x6+x7>=25)
m.Equation(x23+x24+x1+x2+x5+x6+x7+x8>=25)
m.Equation(x24+x1+x2+x3+x6+x7+x8+x9>=40)
m.Equation(x1+x2+x3+x4+x7+x8+x9+x10>=40)
m.Equation(x2+x3+x4+x5+x8+x9+x10+x11>=40)
m.Equation(x3+x4+x5+x6+x9+x10+x11+x12>=60)
m.Equation(x4+x5+x6+x7+x10+x11+x12+x13>=60)
m.Equation(x5+x6+x7+x8+x11+x12+x13+x14>=60)
m.Equation(x6+x7+x8+x9+x12+x13+x14+x15>=60)
m.Equation(x7+x8+x9+x10+x13+x14+x15+x16>=30)
m.Equation(x8+x9+x10+x11+x14+x15+x16+x17>=30)
m.Equation(x9+x10+x11+x12+x15+x16+x17+x18>=30)
m.Equation(x10+x11+x12+x13+x16+x17+x18+x19>=30)
m.Equation(x11+x12+x13+x14+x17+x18+x19+x20>=25)
m.Equation(x12+x13+x14+x15+x18+x19+x20+x21>=25)
m.Equation(x13+x14+x15+x16+x19+x20+x21+x22>=25)
m.Equation(x14+x15+x16+x17+x20+x21+x22+x23>=25)

#Objectives
m.Obj(x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24)

#set global options
m.options.IMODE = 3

#solve simulation
m.solve(GEKKO(remote = True))

#results
print('')
print('Results: ')
for i in range (1,25):
    print('x'+str(i), str(vars() ["x"+str(i)].value))
