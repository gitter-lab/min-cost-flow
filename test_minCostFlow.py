import subprocess

# uncomment line 73 and 74 to check over dictionaries

command = "python"
script = "minCostFlow.py"

for i in range (1,8):
    print("test: ",i)
    args = [
    "--edges_file", f"tests/graph{i}/edges.txt",
    "--sources_file", f"tests/graph{i}/sources.txt",
    "--targets_file", f"tests/graph{i}/targets.txt",
    "--output", f"test_graph{i}"
    ] 
    cmd = [command, script] + args

    # Run the command
    subprocess.run(cmd)