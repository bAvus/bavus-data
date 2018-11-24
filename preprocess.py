columns_of_interest = {
    "loggingTime(txt)": "time",
    "loggingSample(N)": "N",
    "locationTimestamp_since1970(s)": "ts",
    "locationLatitude(WGS84)": "lat",
    "locationLongitude(WGS84)": "lng",
    "locationAltitude(m)": "alt",
    "locationSpeed(m/s)": "speed",
    "locationVerticalAccuracy(m)": "gps_v_accuracy",
    "locationHorizontalAccuracy(m)": "gps_h_accuracy",
    "accelerometerTimestamp_sinceReboot(s)": "acc_ts",
    "accelerometerAccelerationX(G)": "acc_x",
    "accelerometerAccelerationY(G)": "acc_y",
    "accelerometerAccelerationZ(G)": "acc_z"
}

# The value used in the paper is 10km/h = 2.78 m/s
speed_lower_bound = 2.78

import pandas as pd

def get_data_subset(dataset):
    df = pd.read_csv("raw_data/" + dataset + ".csv")
    # Filtering out 'slow' segments.
    df = df[df["locationSpeed(m/s)"] > speed_lower_bound]
    # Getting rid of unrelevant data.
    df = df[[*columns_of_interest]]
    # Renaming the columns.
    df = df.rename(index=str, columns=columns_of_interest)

    df.to_csv("subset_data/" + dataset + ".csv", index=False)

get_data_subset("ride1")
get_data_subset("ride2")
