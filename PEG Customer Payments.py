#!/usr/bin/env python

import pandas as pd
import datetime
from sqlalchemy import create_engine
import pymysql

pd.set_option('mode.chained_assignment', None)

def load_data(cols: list):
  sqlEngine  = create_engine('mysql+pymysql://root:pass123@127.0.0.1', pool_recycle=3600)
  df = pd.read_sql("select * from peg.customerpayments", sqlEngine.connect());

  return df.set_axis(cols, axis='columns', inplace=False)

def main():
  cols = ['Customer Id', 'Contract Id', 'Name', 'Product Type', 'Country', 'Contract Status', 'Sum Paid To Date', 'Expected Total Amount', 'Date']
  df = load_data(cols)

  # Convert Date column from string to datetime data type
  df['Date'] = pd.to_datetime(df['Date'])

  # Filter last day of months
  filtered_month_ends = df.loc[df['Date'].dt.is_month_end]

  # Extract Month and Year
  filtered_month_ends['Month'] = df['Date'].dt.month_name()
  filtered_month_ends['Year'] = df['Date'].dt.year

  # Sort Months
  months = ['January', 'February', 'March', 'April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  filtered_month_ends['Month'] = pd.Categorical(filtered_month_ends['Month'], categories=months, ordered=True)

  filtered_month_ends.sort_values(['Month'], inplace=True)

  # Calculate RE
  filtered_month_ends['RE'] = (filtered_month_ends['Sum Paid To Date'] / filtered_month_ends['Expected Total Amount'])

  aggregated_RE = filtered_month_ends.groupby(['Month', 'Country', 'Product Type']).agg({'RE': 'mean'}).reset_index()

  # Replace NaN with 0
  aggregated_RE['RE'] = aggregated_RE['RE'].fillna(0)

  # Save to Excel
  aggregated_RE.to_excel(r'PEG Customer Payments.xlsx', sheet_name='Customer RE', index=False)
  print("Data saved to Excel\n\n")

  # RE by Month and Product Name
  month_product_RE = filtered_month_ends.groupby(['Month', 'Name']).agg({'RE': 'mean'}).reset_index()
  print('{}:\n{}\n'.format("Month Product RE",month_product_RE))

  # RE by Month and Status
  month_status_RE = filtered_month_ends.groupby(['Month', 'Contract Status']).agg({'RE': 'mean'}).reset_index()
  print('{}:\n{}'.format("Month Status RE",month_status_RE))
  print(month_status_RE)

if __name__ == "__main__":
  main()