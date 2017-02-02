import os
import errno
from subprocess import call

#colorscheme = "tango"
colorscheme = "native"

def main(indir=".", full=True, delete=True):  
#$ define_matches
  exts = {
    ".m" : "%$", 
    ".py" : "#$",
    ".tex" : "%$",
    }
#$  
  ignores = [
    #"make_pygments.py",
    #"code.tex",
    ]

  # a dictionary of all of the directories
  # we'll need to create.
  dirs = {
    "listing": "../tex/pieces/",
    "colorinfo": "../tex/",
    "color": "colorized/",
    "snippets": "snippets/"
    }
  for d in dirs:
    
    # Delete the folder of colored code
    # and the folder of snippets to start
    # fresh each time.
    if delete:
      if d in ["color", "snippets"]:
        call( ["rm", "-fr", dirs[d]] )
      
    # Make sure all of the needed folders exist.
    mkdir_p(dirs[d])

  # always write the color information
  make_color_info(dirs["colorinfo"], colorscheme)

  # keep track of which files we colored
  matched_files = []
    
  # list all of the files in this directory
  for f in os.listdir(indir):
    fullf = os.path.join(indir,f)
    if f in ignores:
      continue
    name, ext = os.path.splitext( f )
    
    # if the file has one of the given 
    # extensions, proceed to color it
    if ext in exts:
      fnew = "{}.tex".format(name, ext[1:])
      fnewdir = os.path.join(
        dirs["color"], ext[1:])
      fnew = os.path.join(fnewdir, fnew)
      print f
      make_snippets(fullf, dirs["snippets"],
                    pat = exts[ext])
      if full:
        matched_files.append((name, ext[1:]))
        mkdir_p(fnewdir)
        call( [
          "pygmentize",
          "-f", "latex",
          "-P", "verboptions={}".format(
            "numbers=left,numbersep=0.5em"),
          "-o",  fnew, fullf
        ] )
        
  # write all of the colored code pieces
  # to a code_listing table of contents
  # in latex.
  code_file = os.path.join(
    dirs["listing"], "code.tex")
  color_dir = os.path.join( 
    "../code/", dirs["color"] )
  mode = "w" if delete else "a"
  with open(code_file, mode) as fout:
    for m,e in sorted(matched_files):
      #joined = "_".join([m, e])
      joined = os.path.join(e,m)
      sout = "\\code{{{}.{}}}\n".format(
        "\\_".join( m.split("_")), e)
      sout += "\\label{{code/{}}}\n".format(joined)
      sout += "\\begin{footnotesize}"
      sout += "\\input{{{}.tex}}".format(
        os.path.join(color_dir, joined))
      sout += "\\end{footnotesize}\n\n"
      fout.write(sout)

#$ snipdef
def snipdef(pat, line):
  """Look for snippet definitions on a line."""
  if pat not in line:
    return None
  idx = line.index(pat)
  # If the line starts with pat, then
  # consider it to be a snippet.
  if idx == 0:
    # The snippet's name is everything
    # to the right of pat on this line.
    return line[idx+len(pat):].strip()
  return None # pattern is in line but not snippet
#$
      
def make_snippets(fname, outdir, pat="%!"):
  """
  Goes through the specified file and looks for
  matching pairs of pat.  It puts the code
  segment in between the tags into a 
  small file and then colorizes just that
  code segment.
  """
#$ collect_lines
  name, ext = os.path.splitext(fname)
  snippets = {} # dict of this file's snippets
  with open(fname, "r") as fin:
    sname = "" # sname will be the name of snippet
    for i, line in enumerate(fin.readlines()):
      if snipdef(pat, line) is not None:
        sname = snipdef(pat, line)     
        if sname: # beginning of a snippet
          if not sname in snippets:
            # +1 because the code starts
            # on the line after the label.
            # Another +1 because enumerate
            # starts with i at 0.
            snippets[sname] = (i+2, [])
      if sname and snipdef(pat, line) is None:
        snippets[sname][1].append(line)
#$ write_snippets
  for sname in snippets:
    i, lines = snippets[sname]
    print " ", sname, i, "-", i+len(lines)-1
    
    fname = sname + ext
    inname = os.path.join(outdir, fname)
    
    # put snippet in outdir subfolder 
    # labeled by extension    
    snipdir = os.path.join(outdir,ext[1:])
    mkdir_p(snipdir)
    with open(inname, "w") as fout:
      fout.writelines(lines)
#$ pygmentize      
    call([
      "pygmentize", 
      "-f", "tex", 
      "-P", "verboptions={},{},{}".format(
        "numbers=left", 
        "numbersep=0.5em",
        "firstnumber={}".format(i)),
      "-o", os.path.join(snipdir, sname + ".tex"),
      inname
      ])
#$      
    call(["rm", inname])
    
    #for l in lines:
      #print "   ", i, l.strip()
      #i += 1
      
def make_color_info( outdir, style ):
  outfile = os.path.join(outdir,"color_info.tex")
  o = open( outfile, "w" )
  call( [
    "pygmentize",
    "-S", style,
    "-f", "latex"
    ], stdout = o )
  
# borrowing from stackoverflow.
# http://stackoverflow.com/questions/
#   600268/mkdir-p-functionality-in-python
def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if ( exc.errno == errno.EEXIST and 
        os.path.isdir(path) ):
      pass
    else: raise
    
if __name__ == "__main__":
  main()
  main("../tex/", full=False, delete=False)
  main("../tex/pieces/", full=False, delete=False)