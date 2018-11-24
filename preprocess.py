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

def preprocess(path, dataset):
    df = pd.read_csv("%s/%s.csv" % (path, dataset))

    # This is for mock data.
    for attr in [*columns_of_interest]:
        if not attr in df.columns:
            df[attr] = '0'

    # Filtering out 'slow' segments.
    df = df[df["locationSpeed(m/s)"] > speed_lower_bound]
    # Getting rid of unrelevant data.
    df = df[[*columns_of_interest]]
    # Renaming the columns.
    df = df.rename(index=str, columns=columns_of_interest)

    df.to_csv("preprocessed/" + dataset + ".csv", index=False)

preprocess("raw_data", "ride1")
preprocess("raw_data", "ride2")
preprocess("mock_data", "ride1_extension")
preprocess("mock_data", "ride2_extension")
preprocess("mock_data", "ride3")
