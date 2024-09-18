# Min-Cost Flow Code

The script `minCostFlow.py` attempts to connect sources to targets in a graph
using a minimum-cost flow algorithm.

More details of the algorithm can be found in:  
[Automating parameter selection to avoid implausible biological pathway models](https://doi.org/10.1038/s41540-020-00167-1).
Chris S Magnano, Anthony Gitter.
*npj Systems Biology and Applications*, 7:12, 2021.

## Edge Handling
The code is designed to process both undirected and directed edges, prioritizing directed edges in scenarios where an equivalent undirected edge exists and selecting higher edge weights in the case of duplicate edges.

## Input Format Example
The input should be formatted as follows, with columns for node1, node2, rank, and direction:
```
A       B       0.9     U
B       A       0.1     D
...
```
In this format, "U" represents an undirected edge, and "D" represents a directed edge.

## Dependencies

Google's [OR-Tools library](https://developers.google.com/optimization/flow/mincostflow) is required to run this script. 
> OR-Tools version: 9.4.1874

Python 3 is required to run this script
> verison 3.10.4 or 3.10.7 work best

## Usage
`minCostFlow.py [-h] --edges_file EDGES_FILE --sources_file SOURCES_FILE --targets_file TARGETS_FILE [--flow FLOW] --output OUTPUT [--capacity CAPACITY]`

>  -h, --help:      Show this help message and exit.
>
>  --edges_file:   Network file. File should be in SIF file format. 
>
>  --sources_file: File which denotes source nodes, with one node per line. 
>
>  --targets_file: File whiuch denotes target nodes, with one node per line. 
>
>  --flow           The amount of flow pushed through the network. 
>
>  --output         Prefix for all output files. 
>
>  --capacity       The amount of flow which can pass through a single edge. 

## Testing
`python test_minCostFlow.py`

The code executes two sets of graph series, namely the 'graph series' and the 'test series' The graphs series of graphs are used to check the code's correctness. Except for internal tiebreaking by the solver, each result is deterministic. The tests series of graphs are used to verify whether the code is executing appropriately depending on distinct edge cases. The expected results for both series can be found in graphs/correct_outputs.txt for the graph series and tests/correct_outputs.txt for the test series.