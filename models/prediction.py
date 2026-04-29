from sklearn.linear_model import LinearRegression

def predict_by_zone(df):
    results = {}

    if df.empty:
        return results

    for zone in df["zone"].dropna().unique():
        df_zone = df[df["zone"] == zone]

        if len(df_zone) < 3:
            continue

        X = df_zone[["duree_heures"]]
        y = df_zone["impact_numerique"]

        model = LinearRegression()
        model.fit(X, y)

        prediction = model.predict([[5]])[0]
        results[zone] = round(prediction, 0)

    return results
