import spreadsheet_validation as sv
import pandas as pd
import numpy as np 
from datetime import datetime

# Lendo o Ficheiro de input
path_input=r'C:\Users\emere\Desktop\Celfinet\PT\June\Input\Vantage Towers_PT TowerDB Apr21.xlsx'
#test = '/content/teste_dates.xlsx'
sheetname = 'Final Delivery'
skiprows = 6
skipcolumns = 1
list_columns = ["Site Code","Site Name","EVO Site ID","Macro Region","Region","Province","Municipality","Nr. Inhabitants","Address","Altitude","Latitude","Longitude","Ground Register","Categorization by inhabitants","Categorization by Transmission Sys","Categorization by Transmission Sys (sub-cluster)","Categorization by Site Type","Other internal categorisation I","Categorisation by connectivity","Technology VOD","Technology VOD: Auxiliar","Fibre / Microwave","Type of Structure","Tower Height (m)","Floor space","Floor space (availability)","Status","Infrastructure ready (existing)/ to be ready (new)","Infrastructure to be dismantled by","Date when Vodafone active equipment is removed","Infrastructure to be shared by","Core site type","Transmission Hub Site (YES/NO)","Transmission Hub Site (inc. with/without Shelters)","Transmission Site (inc. with/without Shelters)","Room configuration","An Indoor + Outdoor Site","Climate Control (YES/NO)","Air Conditioning (YES/NO)","Free-Air Cooling (YES/NO)","Power Supply ","Active/Passive DAS","Strategic Site (YES/NO)","Critical Site (YES/NO)","	If a Non-Critical and non-Transmission Hub Site, Category 1 or Category 2","Is the Site a WIP site","Indicative completion date?","Capital expenditure incurred to the MSA Effective Date","Indicative capital expenditure required to complete the site build","Vertical Infrastructure ","Site Type","Technology_VOD","Fibre/Microwave","Power Supply","# Antennas","# Minilinks","	Details of Operator Equipment installed at the Site","Site Configuration","	NOS shared site (Yes/No)","	MEO shared site (Yes/No)","Details of any Active Sharing involving Operator applicable in respect of the Site (and, where applicable, the type of Active Sharing);","	Details of the access arrangements applicable at each Site (including any access restrictions and applicable public access requirements).","Sites under Hawkins arrangements (Yes/No)","Hawkins Sites (Yes/No)","NOS Crossed Site (Yes/No)","BTS Sites (Yes/No)","Energy Provider ","POD ID","Annual Energy Consumption (kWh)","Annual Energy cost (€)","Total Energy Cost (Energy provider + Landlord)","# Lease Contracts","Countepart","Total Annual Lease (€)","Current annual lease fees (€)","Current energy lease fees (€)","Current annual other fees (€)","Annual Lease fees + Annual Other fees","Sub-Lease","(Latest) residual duration until expiring date","Maturity Cluster - Expiring date","(Latest) residual duration until expiring date after renewal","Maturity Cluster - Expiring date after renewal","Type of lease contract","Reason for no lease fee","Comments to Lease Contracts","NOS (1/0)","Total Revenues NOS (€)","Annual Hosting fee NOS (€)","Annual Energy fee NOS (€)","Annual Maintenance fee NOS (€)","Annual Other Services fee NOS (€)","Tenancy duration until expiring date NOS","Maturity Clusters NOS","MEO (1/0)","Total Revenues MEO (€)","Annual Hosting fee MEO (€)","Annual Energy fee MEO (€)","Annual Maintenance fee MEO (€)","Annual Other Services fee MEO (€)","Tenancy duration until expiring date MEO","Maturity Clusters MEO","OTMOs (1/0)","Total Revenues OTMOs (€)","Annual Hosting fee OTMOs (€)","Annual Energy fee OTMOs (€)","Annual Maintenance fee OTMOs (€)","Annual Other Services fee OTMOs (€)","Tenancy duration until expiring date OTMOs","Maturity Clusters OTMOs","Total # of 3rd Party Tenants","Name of 3rd Party Tenants","Type of Sharing","Total Hosting Fee & Services from 3rd Party Tenants (€)","Annual Hosting fee from 3rd Party Tenants (€)","Annual Energy fee from 3rd Party Tenants (€)","Annual Maintenance fee from 3rd Party Tenants (€)","Other Services fee from 3rd Party Tenants (€)","Weighted Average tenancy duration until expiring date","Total # of Tenants","Macro Cluster Tenancy","Comments to Tenant Agreements","Macro Cluster Type of contract","Easement (Servitù di passaggio)","Turistic Sites","Sites_As_Metered_Estimated","Strategic_Site_Bucket","Critical_Site_Beyond_10","First_Active_Sharing_Deployment_Type ","First_Active_Sharing_Start_Date","First_Active_Sharing_End_Date ","Subsequent_Sharing_Arrangement","Legacy_Site_Agreement_Terminated(Yes/NO)","Decommissioned Sites(True/false)"]
columns_integer_convert = ['Nr. Inhabitants','Tower Height (m)', 'Floor space','Floor space (availability)','Annual Energy Consumption (kWh)','Annual Energy cost (€)','Total Energy Cost (Energy provider + Landlord)','Current annual lease fees (€)','Current energy lease fees (€)','Current annual other fees (€)','Annual Lease fees + Annual Other fees','Total Revenues NOS (€)','Annual Hosting fee NOS (€)','Annual Energy fee NOS (€)','Annual Maintenance fee NOS (€)','Annual Other Services fee NOS (€)','OTMOs (1/0)','Total Revenues OTMOs (€)','Annual Hosting fee OTMOs (€)','Annual Energy fee OTMOs (€)','Annual Maintenance fee OTMOs (€)','Annual Other Services fee OTMOs (€)','MEO (1/0)','Total Revenues MEO (€)','Annual Hosting fee MEO (€)','Annual Energy fee MEO (€)','Annual Maintenance fee MEO (€)','Annual Other Services fee MEO (€)','Total Hosting Fee & Services from 3rd Party Tenants (€)','Annual Hosting fee from 3rd Party Tenants (€)','Annual Energy fee from 3rd Party Tenants (€)','Annual Maintenance fee from 3rd Party Tenants (€)','Other Services fee from 3rd Party Tenants (€)','Total # of Tenants', 'First_Active_Sharing_Deployment_Type ']
towerdb = sv.read_files(path_input, sheetname, skiprows, skipcolumns,columns_integer_convert)
towerdb = towerdb[list_columns]

# Lendo o ficheiro de output para cruzar com o ficheiro de input
path_df_output = r'C:\Users\emere\Desktop\Celfinet\PT\June\Output\TowerDB_Portugal_20210630.csv'
df_output = pd.read_csv(path_df_output, encoding='latin')
df_output = df_output[['Site Code', 'Date_Of_Equipment_Removal']]

# Merge files to get Date of equipament removal columns from output file
towerdb = towerdb.merge(df_output, on='Site Code')

"""
#Change datetime format
date_format = '%d/%m/%Y'
columns_date_convert = ['Infrastructure ready (existing)/ to be ready (new)','Date when Vodafone active equipment is removed','Infrastructure to be shared by', 'First_Active_Sharing_Start_Date',	'First_Active_Sharing_End_Date ','Subsequent_Sharing_Arrangement'] #, 'Date_Of_Equipment_Removal']
towerdb = sv.change_date_format(towerdb, columns_date_convert, date_format)
"""

# On the air sites which have blank values
status_columns = 'Status'
status = 'In Service'
on_air_columns = ['Site Code', 'Categorization by Transmission Sys','Categorization by Site Type',\
                  'Sites_As_Metered_Estimated', 'Infrastructure ready (existing)/ to be ready (new)', \
                  'Climate Control (YES/NO)', 'Strategic Site (YES/NO)', 'Critical Site (YES/NO)',\
                  'Is the Site a WIP site', 'Power Supply ', 'Strategic_Site_Bucket', \
                  'Critical_Site_Beyond_10','Legacy_Site_Agreement_Terminated(Yes/NO)', \
                  'Decommissioned Sites(True/false)']

path_on_air = r'C:\Users\emere\Desktop\Celfinet\PT\validations\on_air_sites_blank_values.xlsx'
# how can I highlight the blank cell before convert to xlsx
sv.on_air_sites_check(towerdb, on_air_columns, status_columns, status, path_on_air)

#towerdb.to_csv('/content/towerdb_pt_output.csv',index=False)
#towerdb.head(2)

# Read msa files to match site code information from towerdb file
msa_path = r'C:\Users\emere\Desktop\Celfinet\PT\20200917 - PT MSA Initial Site List - Final (1).xlsx'
msa_sheet = 'MSA Initial Site List'
msa_skiprows = 4
msa_skipcol = 0
col = 'Site Code'
msa_file = pd.read_excel(msa_path, sheet_name = msa_sheet,usecols='B',skiprows = msa_skiprows)
msa_file.columns = [col]

site_column = 'Site Code'
bts_column = 'BTS Sites (Yes/No)'
cond = 'No'
path_to_save = r'C:\Users\emere\Desktop\Celfinet\PT\validations'
country = 'PT'
msa = [i for i in msa_file['Site Code']]
tow = [i for i in towerdb['Site Code']]

# return 2 df, first are the new sites with no BTS flags marked
# Second is the sites that are demerged dates than current date
df1, df2 = sv.check_new_sites(towerdb, msa, tow, site_column, bts_column, cond, path_to_save, country)