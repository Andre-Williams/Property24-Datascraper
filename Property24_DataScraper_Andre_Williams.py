import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import demjson

def TrendandStatistics(Suburb):
    for Sub in Suburb:
        URL = "https://www.property24.com/cape-town/{}/property-trends/{}".format(Sub[0], Sub[1])
        req = requests.get(URL)

        soup = BeautifulSoup(req.content, 'html.parser')
        soup.prettify()

        script_list = []


        for script in soup.findAll("script", attrs={'type':'text/javascript'}):
            script_list.append(script)

        Graph_data = str(script_list[13]).split(";")
        writer = pd.ExcelWriter("Output/{}_Property Trends and Statistics.xlsx".format(Sub[0]), engine='xlsxwriter')

        for row in Graph_data:
            row = row.strip()

            if row[0:15] != "areaTrends.draw":
                pass

            else:
                if row[15:25] == "AnnualSale":
                    result = re.search('Graph(.*)', row)
                    str_data = result.group(1)[1:-1].split(", ")
                    js_obj = str_data[1]
                    dict_data = demjson.decode(js_obj)

                    df_cols = []
                    for cols in dict_data['cols']:
                        df_cols.append(cols['id'])

                    df_rows = []

                    for rows in dict_data['rows']:
                        row_data = []
                        for val in rows['c']:
                            if val['f'] == None:
                                row_data.append(val['v'])
                            else:
                                if val['f'].isnumeric() == True:
                                    row_data.append(int(val['f']))
                                else:
                                    row_data.append(val['f'])

                        df_rows.append(row_data)
                        row_data = []

                    df = pd.DataFrame(df_rows, columns=df_cols)
                    df.rename(columns={'NumberOfSales': 'No. of Sales', 'AverageAskingPrice': 'Avg. Asking Price', 'AverageSalePrice': 'Avg. Sale Price'}, inplace=True)
                    df.to_excel(writer, sheet_name='Annual')

                if row[15:25] == "Properties":
                    result = re.search('Graph(.*)', row)
                    str_data = result.group(1)[1:-1].split(", ")
                    js_obj = str_data[1]
                    dict_data = demjson.decode(js_obj)

                    df_cols = []
                    for cols in dict_data['cols']:
                        df_cols.append(cols['id'])

                    df_rows = []

                    for rows in dict_data['rows']:
                        row_data = []
                        for val in rows['c']:
                            row_data.append(val['v'])
                        df_rows.append(row_data)
                        row_data = []

                    df = pd.DataFrame(df_rows, columns=df_cols)
                    df.rename(columns={'NewToMarket': 'New to Market', 'TotalOnMarket': 'Total on Market'}, inplace=True)
                    df["Total on Market"] = df["New to Market"] + df["Total on Market"]
                    df.to_excel(writer, sheet_name='Properties For Sale')

                if row[15:25] == "AverageLis":
                    result = re.search('Graph(.*)', row)
                    str_data = result.group(1)[1:-1].split(", ")
                    js_obj = str_data[1]
                    dict_data = demjson.decode(js_obj)

                    df_cols = []
                    for cols in dict_data['cols']:
                        df_cols.append(cols['id'])

                    df_rows = []

                    for rows in dict_data['rows']:
                        row_data = []
                        for val in rows['c']:
                            if type(val['v']) != type(str()):
                                row_data.append(val['f'])
                            else:
                                row_data.append(val['v'])
                        df_rows.append(row_data)
                        row_data = []

                    df = pd.DataFrame(df_rows, columns=df_cols)
                    df.rename(columns={'Bedrooms': 'No. of Bedrooms', 'AverageListPrice': 'Average List Price'},inplace=True)
                    df.to_excel(writer, sheet_name='Average Bedroom')

                if row[15:25] == "SoldProper":
                    result = re.search('Graphs(.*)', row)
                    str_data = result.group(1)[1:-1].split(", ")
                    js_obj = str_data[2]
                    dict_data = demjson.decode(js_obj)

                    df_cols = []
                    for cols in dict_data['cols']:
                        df_cols.append(cols['id'])

                    df_rows = []

                    for rows in dict_data['rows']:
                        row_data = []
                        for val in rows['c']:
                            if val['f'] == None:
                                row_data.append(val['v'])
                            else:
                                if val['f'].isnumeric() == True:
                                    row_data.append(int(val['f']))
                                else:
                                    row_data.append(val['f'])

                        df_rows.append(row_data)
                        row_data = []

                    df = pd.DataFrame(df_rows, columns=df_cols)
                    del df['NumberOfProperties_Popular2']
                    del df['PriceOfProperties_Popular2']
                    df.rename(columns={'NumberOfProperties_Popular1': 'No. of Sales',
                                       'PriceOfProperties_Popular1': 'Average Sold Price'},
                              inplace=True)
                    df.to_excel(writer, sheet_name='Sectional Units')

                if row[15:25] == "AreaDemogr":
                    result = re.search('Graphs(.*)', row)
                    str_data = result.group(1)[1:-1].split(", ")
                    js_obj = str_data[1]
                    dict_data = demjson.decode(js_obj)

                    df_cols = []
                    for cols in dict_data['cols']:
                        df_cols.append(cols['id'])

                    df_rows = []

                    for rows in dict_data['rows']:
                        row_data = []
                        for val in rows['c']:
                            if type(val['v']) != type(str()):
                                float_num = round(float(val['v']), 3)
                                row_data.append(float_num)
                            else:
                                row_data.append(val['v'])
                        df_rows.append(row_data)
                        row_data = []

                    df = pd.DataFrame(df_rows, columns=df_cols)
                    df.rename(columns={'DemographicsType': 'Demographics Type'},
                              inplace=True)
                    df.to_excel(writer, sheet_name='Age')

        df2_cols = []
        for table in soup.findAll("table", attrs={'class': 'table table-striped'}):
            for heading in table.findAll('th'):
                df2_cols.append(heading.get_text())

        df2_rows = []
        row_val = []
        for table in soup.findAll("tbody"):
            for rows in table.findAll('tr'):
                for val in rows.findAll('td'):
                    if val.get_text().isnumeric() == True:
                        row_val.append(int(val.get_text()))
                    else:
                        row_val.append(val.get_text())
                df2_rows.append(row_val)
                row_val = []

        df2 = pd.DataFrame(df2_rows, columns=df2_cols)
        df2.to_excel(writer, sheet_name='Bedroom')

        writer.save()

TrendandStatistics([["green-point","11017"],
                    ["clifton","11015"],
                    ["camps-bay","11014"],
                    ["vredehoek","9166"]])

# TrendandStatistics([["cape-town-city-centre","9138"]])



