import pandas as pd

# Read the CSV file
df = pd.read_csv("datav1.csv")

# Group the data by 'name' and aggregate the relevant columns
result = (
    df.groupby("name", as_index=False)
    .agg(
        category=("category", lambda x: list(x.unique())),  # Collect unique subcategories as a list
        weburl=("website url", "first"),                   # Take the first value for weburl
        img_url=("img url", "first")                       # Take the first value for img_url
    )
)

# Save the aggregated data to a new CSV file
result.to_csv("datav3.csv", index=False)

print("Aggregated data saved to 'datav3.csv'")
