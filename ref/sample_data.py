import numpy as np

arr_ref = np.loadtxt("data\sample_data.csv", delimiter=";", dtype=str, skiprows=1)
# print(arr_ref)
arr_val_ref = arr_ref[:,0]
# print(arr_val_ref[0])
arr_data_ref = arr_ref[:,1:]
# print(arr_data_ref[0])

# data_byte = "78 0 0 0 80 78 80 78 80 78 80 78 0 0 78 78 0 0 0 0 0"
data_byte = "78 0 0 0 80 78 80 78 80 78 0 0 0 78 0 78 0 0 0 0 80"
# print(data_byte)
arr_data_byte = np.array(data_byte.split())
# print(arr_data_byte)

for i in range(arr_val_ref.size):
    if(np.array_equal(arr_data_byte, arr_data_ref[i])):
        print(float(arr_val_ref[i]))