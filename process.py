import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# In our dataset 2 seconds roughly convert into 30 entries.
short_series = 30 * 5
normalize = True

def process_data(datasets):
    fragments = []
    for dataset in datasets:
        fragments.append(pd.read_csv("preprocessed/%s.csv" % dataset))
    df = pd.concat(fragments)

    x_data = df["acc_x"]
    x_delta_data = np.subtract(x_data[1:], x_data[:-1])

    z_data = df["acc_z"]
    z_delta_data = np.subtract(z_data[1:], z_data[:-1])

    speed_data = df["speed"]

    values = []

    for i in range(len(x_delta_data)-short_series):
        mx_x = np.amax(np.absolute(x_delta_data[i:i+short_series]))
        mx_z = np.amax(np.absolute(z_delta_data[i:i+short_series]))
        avg_speed = np.average(speed_data[i:i+short_series])
        val = (mx_x + mx_z) / avg_speed
        values.append(val)

    if normalize:
        values /= np.amax(values)

    plt.plot(np.arange(len(x_delta_data)-short_series), values)
    plt.savefig("output/all.png")
    plt.clf()

    pd.DataFrame({
        "lat": df["lat"][:-short_series-1],
        "lng": df["lng"][:-short_series-1],
        "score": values,
    }).to_csv("output/data.csv", index=False)

process_data(["ride1", "ride1_extension", "ride2", "ride2_extension", "ride3"])
