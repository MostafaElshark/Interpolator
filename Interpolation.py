import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re
import sys
if len(sys.argv) == 1:
    print("No file was dropped\n")
    print("please Drag and Drop the file")
    exit()
first = sys.argv[1]
second = sys.argv[2]
Corpus1 = pd.read_csv(first, encoding='latin-1')
corpus2 = pd.read_csv(second, encoding='latin-1')

def get_date_format(date): # get the date format
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return "%Y-%m-%d"
    elif re.match(r"^\d{2}-\d{2}-\d{4}$", date):
        return "%d-%m-%Y"
    elif re.match(r"^\d{2}/\d{2}/\d{4}$", date):
        return "%m/%d/%Y"
    elif re.match(r"^\d{4}/\d{2}/\d{2}$", date):
        return "%Y/%d/%m"
    elif re.match(r"^\d{4}\d{2}\d{2}$", date):
        return "%Y%m%d"
    elif re.match(r"^\d{2}\d{2}\d{4}$", date):
        return "%d%m%Y"
    elif re.match(r"^\d{4}/\d{2}/\d{4}$", date):
        return "%Y/%m/%d"
    elif re.match(r"^\d{2} \w{3} \d{4}$", date):
        return "%d %b %Y"
    elif re.match(r"^\d{2} \w{4,9} \d{4}$", date):
        return "%d %B %Y"
    else:
        return None

def removeNan(df): # remove nan from the top based on the first column
    h = df.columns[1]
    for i in range(len(df)):
        if df[h][i] == df[h][i]:
            return df[i:]

def removenanfromlast(df): # remove nan from the bottom based on the first column
    h = df.columns[1]
    for i in range(len(df))[::-1]:
        if df[h][i] == df[h][i]:
            return df[:i+1]

def get_df_name(df): # get the name of the file
    name = Path(df).stem
    return name

def interpolatetwopoints(df1, df2): # interpolate between two points
    try:
        getform = get_date_format(df1['DATE'].iloc[1].astype(str))
        df1['DATE'] = pd.to_datetime(df1['DATE'], format=getform)
    except:
        getform = get_date_format(df1['DATE'].iloc[1])
        df1['DATE'] = pd.to_datetime(df1['DATE'], format=getform)
    try:
        getform = get_date_format(df2['DATE'].iloc[1].astype(str))
        df2['DATE'] = pd.to_datetime(df2['DATE'], format=getform)
    except:
        getform = get_date_format(df2['DATE'].iloc[1])
        df2['DATE'] = pd.to_datetime(df2['DATE'], format=getform)
    newdf1 = Corpus1.set_index('DATE')
    newdf2 = corpus2.set_index('DATE')
    thenewdf = newdf1.join(newdf2, how='outer')
    thenewdf = removeNan(thenewdf) # remove nan from the top based on the first column
    thenewdf = removenanfromlast(thenewdf) # remove nan from the bottom
    firsto = get_df_name(first)
    secondo = get_df_name(second)
    thenewdf = thenewdf.interpolate(method='linear')
    thenewdf.to_csv(r"C:\Users\MrM\Desktop\internship project\mydata\Interpolated\Interpolated_" +firsto +"_"+ secondo+".csv", index=True)
    return

interpolatetwopoints(Corpus1, corpus2)

