using DelimitedFiles

# Read the data from the CSV file
input = DelimitedFiles.readdlm("$(@__DIR__)/ACTIVSg10k_loadP.csv", ',', Any, '\n')

# Extract the data from the input array
# The first column is the time in hours
# The second column is the demand in MW
buses = input[1,2:end]