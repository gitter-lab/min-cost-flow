import subprocess

# uncomment line 73 and 74 to check over dictionaries

command = "python"
script = "minCostFlow.py"

print("testing code functionality")
for i in range (1,8):

    print("test: ",i)
    args = [
    "--edges_file", f"tests/test{i}/edges.txt",
    "--sources_file", f"tests/test{i}/sources.txt",
    "--targets_file", f"tests/test{i}/targets.txt",
    "--output", f"test{i}"
    ] 
    cmd = [command, script] + args

    # Run the command
    subprocess.run(cmd)


print("\ntesting code correctness")
for i in range (1,14):
    print("graph: ",i)
    args = [
    "--edges_file", f"graphs/graph{i}/edges.txt",
    "--sources_file", f"graphs/graph{i}/sources.txt",
    "--targets_file", f"graphs/graph{i}/targets.txt",
    "--output", f"graph{i}"
    ] 
    cmd = [command, script] + args

    # Run the command
    subprocess.run(cmd)