#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import xlsxwriter
from datetime import date
import gspread


def price_sheet_create():

    gc = gspread.service_account(filename='./.app_info/my-test-project-9203-a1d4481e7db0.json')
    sh = gc.open("MLS_Order_Config")


    # Read data
    df_codes = pd.DataFrame(sh.sheet1.get_all_records())
    df_shamrock = pd.read_csv("./PriceLists/Shamrock.csv")
    df_sysco = pd.read_csv("./PriceLists/Sysco.csv", skiprows=1)

    # Join dataframes
    df_codes["SH Prices"] = pd.merge(df_codes, df_shamrock, how='left', left_on = 'Shamrock', right_on = 'Product')["Price"]
    df_codes["Sysco Prices"] = pd.merge(df_codes, df_sysco, how='left', left_on = 'Sysco', right_on = 'SUPC')['Case $'].astype(float)

    # Drop irrelevant columns
    df_codes.drop(columns=['Shamrock', 'Sysco', 'Western Deli code', 'Notes', 'Notes 1'], inplace=True)

    # Type casting
    df_codes['Shamrock Prices'] = df_codes['SH Prices']
    df_codes.drop(columns='SH Prices', inplace=True)

    # Unit conversion
    df_codes['Sysco Prices'] = df_codes['Sysco Prices'] / df_codes['Conv Sys']
    df_codes['Sysco Prices'] = df_codes['Sysco Prices'].round(2)

    df_codes['Shamrock Prices'] = df_codes['Shamrock Prices'] / df_codes['Conv Shm']
    df_codes['Shamrock Prices'] = df_codes['Shamrock Prices'].round(2)

    df_codes['Costco'] = df_codes['Costco'].apply(lambda x: x if type(x)==float else None)
    df_codes['Costco'] = df_codes['Costco'] / df_codes['Conv Cos']
    df_codes['Costco'] = df_codes['Costco'].round(2)

    df_codes['R Depot'] = df_codes['R Depot'].apply(lambda x: x if type(x)==float else None)
    df_codes['R Depot'] = df_codes['R Depot'] / df_codes['Conv Dep']
    df_codes['R Depot'] = df_codes['R Depot'].round(2)


    df_codes['WD Price'] = df_codes['WD Price'].apply(lambda x: x if type(x)==float else None)
    df_codes['WD Price'] = df_codes['WD Price'] / df_codes['Conv WD']
    df_codes['WD Price'] = df_codes['WD Price'].round(2)

    # Create dataframe to store conversions and par levels
    df_info = df_codes.drop(columns=['Shamrock Prices', 'Sysco Prices', 'WD Price', 'Costco', 'R Depot'
    ])

    # Drop conversion columns
    df_codes.drop(columns=['Conv Sys', 'Conv WD', 'Conv Cos', 'Conv Dep', 'Conv Shm', 'Par Levels', 'Daily'], inplace=True)

    # Rename colunms
    df_codes.rename(columns={'WD Price':'WD', 'Sysco Prices':'Sysco', 'Shamrock Prices':'Shamrock'}, inplace=True)


    description_col_name = 'Item to order'
    today = str(date.today())

    # Spacer column
    df_codes['<-PS/OG->'] = ''
    df_codes[description_col_name] = ''

    # List of vendor names for iteration below
    vendor_names = ['Price Sheet', 'WD', 'Costco', 'R Depot', 'Sysco', 'Shamrock']

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("MLS_prices-order.xlsx", engine='xlsxwriter')

    workbook  = writer.book

    for i in range(len(vendor_names)):
        
        if i == 0:        
            
            # Convert the price sheet dataframe to an XlsxWriter Excel object.
            df_codes['Daily Usage'] = df_info['Daily']
            df_codes['Reorder Level'] = df_info['Par Levels']
            df_new = df_codes
            df_new.to_excel(writer, sheet_name='Price Sheet')

            # Get the xlsxwriter workbook and worksheet objects.
            worksheet = writer.sheets['Price Sheet']        
        
        else: 
            
            # Create new dataframes with lowest price product list for each vendor
            df_codes[description_col_name] = df_codes.loc[df_codes[vendor_names[i]] == df_codes.loc[:, ['Sysco', 'WD', 'Shamrock', 'Costco', 'R Depot']].min(axis=1)]['Description']
            df_codes['Daily Usage'] = df_info.loc[df_info['Description'] == df_codes[description_col_name]]['Daily']
            df_codes['Reorder Level'] = df_info.loc[df_info['Description'] == df_codes[description_col_name]]['Par Levels']
            df_codes['On Hand'] = ''
            df_codes['Ordered'] = ''
            
            # Sort by selected items
            df_new = df_codes.loc[df_codes[description_col_name].notnull()]
            df_new = df_new.append(df_codes.loc[df_codes[description_col_name].isnull()])

            df_new = df_new.loc[df_codes[vendor_names[i]] >= 0]
    #       
            # Convert each dataframe to an XlsxWriter Excel object.
            df_new.to_excel(writer, sheet_name=vendor_names[i])

            # Get the xlsxwriter worksheet object for each vendor's order guide.
            worksheet = writer.sheets[vendor_names[i]]
            
        # Light green background, black face
        format1 = workbook.add_format({'bg_color':   '#eef2e6',
                                       'font_color': '#000000',
                                       'border': True,
                                       'bold': True})

        # Formatting for row coloring
        data_format1 = workbook.add_format({'bg_color': '#dedede'})
        data_format2 = workbook.add_format({'bg_color': '#ffffff'})

        for row in range(1, df_new.shape[0]+1, 2):
            worksheet.set_row(row, cell_format=data_format1)
            worksheet.set_row(row + 1, cell_format=data_format2)

        # Set conditional formatting to highlight lowest value in each row
        worksheet.conditional_format('C2:$G'+str(df_new.shape[0] + 1), {'type':     'formula',
                                            'criteria': '=C2=MIN($C2:G2)',
                                            'format':    format1})

        # Adjust column widths
        writer.sheets[vendor_names[i]].set_column(0, 0, 5)
        writer.sheets[vendor_names[i]].set_column(1, 1, 25)
        writer.sheets[vendor_names[i]].set_column(2, 6, 10)
        writer.sheets[vendor_names[i]].set_column(8, 8, 25)
        writer.sheets[vendor_names[i]].set_column(9, 12, 12)

        worksheet.freeze_panes(1, 0)  # Freeze the first row.

    # Save the xlsx
    writer.save()

