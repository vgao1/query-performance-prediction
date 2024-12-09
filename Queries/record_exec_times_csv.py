import csv
# X is trial # (i.e., 1, 2, 3) that should be replaced
no_index_folder_name = "results_no_index_trial3/"
index_folder_name = "results_index_trial3/"

no_index_number_file_names = []
for i in range(1, 23):
  if i!=17 and i!=20:
    no_index_number_file_names.append(str(i))

index_number_file_names = []
for i in range(1, 23):
  index_number_file_names.append(str(i))

no_index_alphanumeric_file_names = []
for i in range(1,23):
  file_name = [str(i) + 'a', str(i) + 'b', str(i) + 'c', str(i) + 'd', str(i) + 'e']
  if i==17 or i==20:
    continue
  elif i==18:
    file_name = [str(i) + 'a', str(i) + 'b', str(i) + 'c', str(i) + 'd']
  for name in file_name:
    no_index_alphanumeric_file_names.append(name)

index_alphanumeric_file_names = []
for i in range(1,23):
  file_name = [str(i) + 'a', str(i) + 'b', str(i) + 'c', str(i) + 'd', str(i) + 'e']
  if i==18:
    file_name = [str(i) + 'a', str(i) + 'b', str(i) + 'c', str(i) + 'd']
  for name in file_name:
    index_alphanumeric_file_names.append(name)

def generate_row_data(query_name, folder_name, indexed):
  file_path = folder_name + query_name + "_output.txt"
  lines = []
  try:
    with open(file_path, 'r') as file:
      lines = [line.strip() for line in file]
  except FileNotFoundError:
    print(f"Error: The file {file_path} does not exist.")
  except Exception as e:
    print(f"An error occurred: {e}")
  execution_time = lines[-3].split(":")[1].split(" ")[1]
  new_data = [query_name, "", execution_time, indexed]
  data.append(new_data)

header = ["query_id", "SQL_query", "execution time (ms)",	"if_indexed"]
data = [header]

"""
We wrote data in this order because this was the order we recorded
SQL statements in the SQL_query column of the CSV for trial 1.
For future trials, we can copy and paste Trial 1 CSV's SQL_query column into
the later trial's SQL_query column.
"""
for name in index_number_file_names:
  generate_row_data(name, index_folder_name, 1)

for name in no_index_number_file_names:
  generate_row_data(name, no_index_folder_name, 0)

for name in index_alphanumeric_file_names:
  generate_row_data(name, index_folder_name, 1)

for name in no_index_alphanumeric_file_names:
  generate_row_data(name, no_index_folder_name, 0)

# X is trial # (i.e., 1, 2, 3) that should be replaced
output_file_path = "trial3_exec_times.csv"
try:
  with open(output_file_path, mode="w", newline="") as file: 
    writer = csv.writer(file)
    writer.writerows(data)
    print(f"Data successfully written to {output_file_path}")
except Exception as e:
  print(f"An error occurred: {e}")
