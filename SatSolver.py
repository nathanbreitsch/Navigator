__author__ = 'NathanBreitsch'
import glpk

class SatSolver:
    @staticmethod
    def solve(matrix, vector):
        lp = glpk.LPX()        # Create empty problem instance
        lp.name = 'feasibility'     # Assign symbolic name to problem
        lp.obj.maximize = True # Set this as a maximization problem
        lp.rows.add(len(vector))         # Append rows to this instance
        for r in lp.rows:      # Iterate over all rows
            r.name = str(r.index) # Name them their index
            r.bounds = 0.0,None #each row is bigger than 0
        lp.cols.add(len(matrix[0]))         # Append columns to this instance
        for c in lp.cols:      # Iterate over all columns
            c.name = 'x%d' % c.index # Name them x0, x1, and x2
            c.bounds = 0.0, 1.0     # bound in circle
        lp.obj[:] = [ 10.0, 6.0, 4.0 ]   # Set objective coefficients
        lp.matrix = [ 1.0, 1.0, 1.0,     # Set nonzero entries of the
                     10.0, 4.0, 5.0,     #   constraint matrix.  (In this
                      2.0, 2.0, 6.0 ]    #   case, all are non-zero.)
        lp.simplex()           # Solve this LP with the simplex method
        print 'Z = %g;' % lp.obj.value,  # Retrieve and print obj func value
        print '; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols)
                               # Print struct variable names and primal values

    @staticmethod
    def makeZeros(n):
        temp = []
        for i in range(0,n):
            temp.append(0)
        return temp