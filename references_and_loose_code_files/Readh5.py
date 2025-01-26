import h5py


file_path = "data_12345.h5"
with h5py.File(file_path, 'r') as hdf:
    print("Keys:", list(hdf.keys()))

    dataset_name = "Keypress_data"
    data = hdf[dataset_name][:]
    print(data)