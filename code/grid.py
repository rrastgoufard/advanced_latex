 
from __future__ import print_function

import os

#$ string_formatting
string1 = "hello {firstname} {lastname}".format(
  firstname="Ebrahim",
  lastname="Amiri",
  )
string2 = "hello {{{firstname}}} {{{lastname}}}".format(
  firstname="Ittiphong",
  lastname="Leevongwat",
  )
names = [(string1,"amiri"), (string2,"leev")]
for s,n in names:
  outname = "../tex/pieces/{}.tex".format(n)
  with open(outname,"w") as fout:
    fout.write(s)
#$

#$ template
header = r"""\begin{multicols}{[=[cols]=]}"""
footer = r"""\end{multicols}"""
texstring = r"""
\includegraphics[width=\linewidth]{[=[name]=]}
"""

def template(x):
  y = x.replace("{","{{")
  y = y.replace("}","}}")
  y = y.replace("[=[","{")
  y = y.replace("]=]","}")
  return y
#$

#$ grid
def grid(indir, outfile, C=5, N=None):
  with open(outfile, "w") as fout:
    
    # print the header
    fout.write(template(header).format(cols=C))
    
    # print something for each file
    for f in sorted(os.listdir(indir))[:N]:
      fout.write(template(texstring).format(
        name=os.path.join(indir,f),
        ))
      
    # print the footer
    fout.write(template(footer).format())
#$

#$ using_grid
if __name__ == "__main__":
  grid(
    indir="../img/fouriers", 
    outfile="../tex/pieces/grid.tex",
    C=5, # five columns, all images
    )
  grid(
    indir="../img/fouriers",
    outfile="../tex/pieces/closeup.tex",
    N=4, # four images total
    C=2, # across two columns
    )
#$