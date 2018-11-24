columns_of_interest = [
    "loggingTime(txt)",
    "loggingSample(N)",
    "locationTimestamp_since1970(s)",
    "locationLatitude(WGS84)",
    "locationLongitude(WGS84)",
    "locationAltitude(m)",
    "locationSpeed(m/s)",
    "locationVerticalAccuracy(m)",
    "locationHorizontalAccuracy(m)",
    "accelerometerTimestamp_sinceReboot(s)",
    "accelerometerAccelerationX(G)",
    "accelerometerAccelerationY(G)",
    "accelerometerAccelerationZ(G)"
]

speed_lower_bound = 0.1

import pandas as pd

def get_data_subset(dataset):
    df = pd.read_csv("raw_data/" + dataset + ".csv")

    df = df[df["locationSpeed(m/s)"] > speed_lower_bound]

    df[columns_of_interest].to_csv("subset_data/" + dataset + ".csv", index=False)

get_data_subset("ride1")
get_data_subset("ride2")
