VERSION HISTORY
2020-02-03-2
# ? Fix mismatch between accel and gyro data (for lower end)
# > Preprocess data by removing DC offset with filter
    # > Require study on noise of different levels to determine which is noise (currently manual with no automation)
    # > Might need to add a moving average for post 'elapsed'-multiplication due to fluctuating value of 'elapsed'
    # ? Automate noise detection somehow?
# Renamed tests as '_test'

2020-02-03
# Rotated data to global reference frame
    # Scipy rotation vector