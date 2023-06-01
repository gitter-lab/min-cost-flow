# Min-Cost Flow Code

The script `minCostFlow.py` attempts to connect sources to targets in a graph
using a minimum-cost flow algorithm.

More details of the algorithm can be found in:  
[Automating parameter selection to avoid implausible biological pathway models](https://doi.org/10.1038/s41540-020-00167-1).
Chris S Magnano, Anthony Gitter.
*npj Systems Biology and Applications*, 7:12, 2021.

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
