import pandas as pd
import numpy as np
import datetime as dt

log_output = '''
{sheetname}                   Columns Validation
------------------------------------------------
# of Columns received: {total_received}
# of Columns required for billing: {number_missing_columns}
# of Columns transformed from file: 

Name of Missing columns in {sheetname} spreadsheet:
{columns}
'''

def read_files(path, sheetname, n_skiprows, n_skip_columns, columns_integer_convert):
    """
    Params:\n
    path: parth of file in the computer.\n
    n_skiprows: Number of rows to delete in the original file,.\n
    columns_to_convert: Columns to convert the data general type. \n
    n_skipcolumn: Columns to skip in the original file. \n
    endrow = pass 0 to read everything, 1 to count entire
    columns_order: List of columns names in specific order to pass in the engine.\n
    """
    # read file and skip header
    df = pd.read_excel(path, sheet_name = sheetname, skiprows = n_skiprows)
    # skip blank columns to create df
    df = df.iloc[:,n_skip_columns:]

    # define the entiry columns which doesn't have NaN 
    cont = 0
    for i in df.iloc[:,0]:
        if str(i) == 'nan':
            break
        else:
            cont +=1
    df = df.iloc[:cont, :]
    #df.columns = columns_order
    
    # convert intery columns to integer 
    df[columns_integer_convert] = df[columns_integer_convert].fillna(0)
    df[columns_integer_convert] = df[columns_integer_convert].astype('int64')
    
    for i in columns_integer_convert:
        lista = []
        for index in df[i]:
            if index == 0:
                lista.append('')
            else:
                lista.append(index)
        df[i] = lista

    #print(endrow)
    return df

def replace_values(df, column, conditional_value, value_to_change):
    """
    Está voltando para float
    """

    lista = []
    for index in df[column]:
        if index == conditional_value:
            lista.append(value_to_change)
        else:
            lista.append(index)
    df[column] = lista
    

def change_date_format(df, columns_date_convert, format):
    for i in columns_date_convert:
        if len(df[i].value_counts()) > 0:
            df[i] = df[i].dt.strftime(format)

    return df

# Refactorar esse codigo para receber todas as colunas num dic
# Sendo as keys=columns e values= picklist for each column
def check_picklist(df, column, picklist):

    errors = 0
    diff_value = []
    for i in df[column]:
        if i not in picklist:
            errors += 1
            diff_value.append(i)
    
    output=f"""
    Check picklist of column: {column}
    ----------------------------------
    # of error found: {errors}
    different picklist value: {diff_value}
    """
    print(output)

def on_air_sites_check(df, columns, status_column, status, path_write):
    
    # dataframe with a conditional setted
    status_df = df[df[status_column]==status]

    # Empty Dataframe to receive blank lines
    new_df = pd.DataFrame()

    aux = []
    for i in columns:
        df = status_df[status_df[i].isnull()]
        if not df.empty:
            aux.append(df)
    if aux != []:
        new_df = pd.concat(aux)
        new_df.drop_duplicates(inplace=True)
        new_df.to_excel(path_write, index=False)

def check_new_sites(df_towerdb, msa_list, towerdb_list, \
                    site_code_column, bts_column, bts_conditional,\
                    path_save, country):
    # capture current date as string
    current_date = pd.to_datetime('now').date()
    # convert current to timestamp
    current_date = pd.to_datetime(current_date)
    out_msa = []
    #VALIDATION OF ALL NEW SITES
    for i in towerdb_list:
        if i not in msa_list:
            out_msa.append(i)

    df = df_towerdb.copy()
    df['Sites'] = [i for i in df[site_code_column]]
    df.set_index('Sites', inplace=True)
    df = df.filter(items = out_msa, axis=0)

    # Save Information of sites which are new, but doesn't Flag BTS like 'Yes' 
    df_bts = df[df[bts_column] == bts_conditional]

    # Save information os sites with demerged date more than current date
    df_diff_demerged_dates = df[(df['BTS Sites (Yes/No)']=='No') & (df['Infrastructure ready (existing)/ to be ready (new)'] > current_date)]
    
    return df_bts, df_diff_demerged_dates
    #df_bill = df[df['Infrastructure ready (existing)/ to be ready (new)'] > data_atual]
    #df.to_excel(f'{path_save}/{country}_new_sites_errors.xlsx', index=False)

def check_columns(table, output_columns):
    """
    Check the total of number of missing columns and the missing columns in passed table.\n

    Params:\n
    table: contain the columns to be check.\n
    output_columns: columns structure at the final file. 

    Returns:\n
    Number of missing columns and a list that contains the name os missing columns.
    """
    """"
    countries = ['DE':{'towerDB':[],\
                       'lc': [],\
                       'ta':[]}\
                 ,'HU','IE','RO','PT','ES','CZ','GR']"""
    total_received = len(table.columns)
    number_missing_columns = 0
    missing_columns = []

    #Counting of missing columns       
    #if country in contries:      
    for columns in output_columns:
        if columns.lower() not in [labels.lower() for labels in table]:
            number_missing_columns +=1
            missing_columns.append(columns)
    
    return total_received, number_missing_columns, missing_columns

