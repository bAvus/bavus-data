import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# In our dataset 2 seconds roughly convert into 30 entries.
short_series = 30 * 5
normalize = True

def process_dataset(dataset):
    df = pd.read_csv("preprocessed/%s.csv" % dataset)

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
        if not np.amax(values) < 0.00001:
            values /= np.amax(values)

    return pd.DataFrame({
        "lat": df["lat"][:-short_series-1],
        "lng": df["lng"][:-short_series-1],
        "score": values,
    })

def process_data(datasets):
    fragments = []

    for i in range(len(datasets)):
        fragments.append(process_dataset(datasets[i]))

        # Filling some gaps. Sorry for that.
        if i == 0:
            fragments.append(pd.DataFrame({
                "lat": [60.17841897910478],
                "lng": [24.79882939720973],
                "score": fragments[-1].tail(1)["score"],
            }))
        elif i == 1 or i == 3 or i == 4:
            fragments.append(pd.DataFrame({
                "lat": [60.1737616],
                "lng": [24.8014866],
                "score": fragments[-1].tail(1)["score"],
            }))

        # This is for Frontend to trigger a change of tracks.
        if i != len(datasets) - 1:
            fragments.append(pd.DataFrame({
                "lat": [0],
                "lng": [0],
                "score": [-1],
            }))

    df = pd.concat(fragments)

    plt.plot(np.arange(len(df["score"])), df["score"])
    plt.savefig("output/all.png")
    plt.clf()

    df.to_csv("output/data.csv", index=False)

process_data(["ride1", "ride1_extension", "ride2", "ride2_extension", "ride3"])
