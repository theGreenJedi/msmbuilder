from Emsmbuilder import old_ArgLib
from Emsmbuilder import plot_graph
import numpy as np
from scipy import io, sparse
import sys
import glob

def run(Matrix, EqPops, ImageDir, Directed=False, EdgeScale=1, PopCutoff=0.01, EdgeCutoff=0.0, OutputFile='Graph.dot'):

    if ImageDir: pngs = glob.glob(ImageDir+'/*.png')
    else: pngs = None
    G = plot_graph.CreateNetwork(Matrix,EqPops,Directed=Directed,EdgeScale=EdgeScale,PopCutoff=PopCutoff,EdgeCutoff=EdgeCutoff,ImageList=pngs)

    plot_graph.PlotNetwork(G,OutputFile=OutputFile)

if __name__ == "__main__":
    print """Draws a representation of your MSM and draws a graph corresponding to it. This graph
is written as a .dot file, which can be read by many common graph utilities. Read in MSM info
as a counts, transition, or net flux matrix.

Note: You need networkx and either Graphviz & PyGraphviz or pydot to get this utility working.
To get the graph the way you want it to look, you might want to open up this script and play
with some default parameters (EdgeScale=1, PopCutoff=0.01, EdgeCutoff=0.1) in the run() function.\n\n"""

    arglist=["tmat", "populations", "directed", "input", "output", "epsilon"]
    options=old_ArgLib.parse(arglist, Custom=[("tmat", "Name of the matrix to represent as a graph. Can be a counts, transition, or net flux matrix. In .mtx format.", None), ("input", "Directory containing node images generated by 'RenderStateImages.py' that will be associated with the graph (optional).", 'None'), ("output", "Name of the dot file to write. Defaut: Graph.dot", 'NoOutputSet')])
    print sys.argv
    
    if options.output == 'NoOutputSet': output='Graph.dot'
    else: output=options.output

    if options.directed == 'directed':
        directed=True
    else:
        directed=False
    print 'Directed', directed

    Matrix=io.mmread( options.tmat )
    Pops=np.loadtxt( options.populations )

    PopCutoff=float(options.epsilon)
    
    run(Matrix, Pops, options.input, Directed=directed, OutputFile=output,PopCutoff=PopCutoff)
