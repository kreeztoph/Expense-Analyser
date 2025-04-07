import pandas as pd


# Function to apply color coding
def color_code(row,color_column):
    if pd.isna(row[color_column]) or row[color_column] == 0:
        return "background-color: orange"  # Neutral
    elif row[color_column] > 0:
        return "background-color: green"  # Positive delta
    else:
        return "background-color: red"  # Negative delta