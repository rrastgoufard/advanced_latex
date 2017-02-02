
from __future__ import print_function

import numpy as np
import os
from grid import template

tex = r"""
\begin{align}
A_[=[i]=] & = 
\begin{pmatrix}
\input{../img/matrices/[=[i]=].tex}
\end{pmatrix} \\
|A_[=[i]=]| & = [=[d]=] \\
A_[=[i]=]^{-1} & = 
\begin{pmatrix}
\input{../img/matrices/[=[i]=]i.tex}
\end{pmatrix} \\
|A_[=[i]=]^{-1}| & = [=[di]=]
\end{align}
"""

def doit(outdir):
  for i in range(5):
    A = np.random.randn(4,4)
    np.savetxt(
      os.path.join(outdir, "{}.tex".format(i)),
      A,
      fmt="%5.3f",
      delimiter=" & ",
      newline=" \\\\\n",
      )
    Ai = np.linalg.inv(A)
    np.savetxt(
      os.path.join(outdir, "{}i.tex".format(i)),
      Ai,
      fmt="%5.3f",
      delimiter=" & ",
      newline=" \\\\\n",
      )
    d = np.linalg.det(A)
    di = np.linalg.det(Ai)
    
    fname = "summary{}.tex".format(i)
    with open(os.path.join(outdir,fname),"w") as fout:
      fout.write(template(tex).format(
        i=i,
        d="{:.3f}".format(d),
        di="{:.3f}".format(di),
        ))

#$ simple_problem
def simple_problem(outdir):
  A = np.matrix([
    [3, 5, 2],
    [1, 6, 2],
    [1, 1, 1],
    ])
  b = np.matrix([1,2,3]).T
  x = np.linalg.solve(A, b)
  
  pairs = [(A,"A"), (b,"b"), (x,"x")]
  for v, name in pairs:
    np.savetxt(
      os.path.join(outdir, "{}.tex".format(name)),
      v,
      fmt="%5.3f",
      delimiter=" & ",     # These two lines 
      newline=" \\\\\n",   # enable latex inputs.
      )
#$    

if __name__ == "__main__":
  doit("../img/matrices")
  simple_problem("../tex/pieces")