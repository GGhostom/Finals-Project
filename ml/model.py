from sklearn.ensemble import RandomForestRegressor


def create_model():
    return RandomForestRegressor(
        n_estimators=100,
        max_depth=10
    )