import pandas as pd

df = pd.read_csv("datav1.csv")
result = (
    df.groupby("name", as_index=False)
    .agg(
        category=("category", list),  # Collect subcategories as a list
        weburl=("website url", "first"),        # Take the first value for weburl
        img_url=("img url", "first"),      # Take the first value for img_url
    )
)
result.to_csv("datav3.csv", index=False)