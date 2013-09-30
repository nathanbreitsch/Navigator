__author__ = 'NathanBreitsch'

class SatSolver:
    @staticmethod
    def solve(matrix):


        numRows = len(matrix)
        numCols = len(matrix[0])
        lp = glpk.LPX()        # Create empty problem instance
        lp.name = 'feasibility'     # Assign symbolic name to problem
        lp.obj.maximize = True # Set this as a maximization problem
        lp.rows.add(numRows)   # Append rows to this instance
        for r in lp.rows:      # Iterate over all rows
            r.name = str(r.index) # Name them their index
            r.bounds = 0.0,None #each row is bigger than 0
        lp.cols.add(numCols)         # Append columns to this instance
        for c in lp.cols:      # Iterate over all columns
            c.name = 'x%d' % c.index # Name them x0, x1, and x2
            c.bounds = 0.0, 1.0     # bound in circle
        lp.obj[:] = SatSolver.makeZeros(len(matrix[0]))   # Set objective coefficients
        matrixEntries = []
        for i in range(0, numRows):
            for j in range(0, numCols):
                if matrix[i][j] != 0:
                    matrixEntries.append((i, j, matrix[i, j])) #append all non-zero entries
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