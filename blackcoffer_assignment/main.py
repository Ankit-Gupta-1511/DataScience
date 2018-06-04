import pandas as pd
import numpy as np
from data_extraction import parser
"""
Importing the ciklist in pandas
"""
cik_list = pd.read_excel("Assignment/cik_list.xlsx")
writer = pd.ExcelWriter('outputs/analysis.xlsx', engine='xlsxwriter')

# print(cik_list)

"""
Adding the host link
"""

host_link = "https://www.sec.gov/Archives/"

cik_list['SECFNAME'] = host_link + cik_list['SECFNAME']


"""
Getting the page from the link and sending the contents to the parser
"""

import urllib
for i,record in cik_list.iterrows():
    print(record)
    link = record['SECFNAME']
    # print(link)
    page = urllib.request.urlopen(link)
    """
    Cleaning of the response data: 
    The data consist of several page tags but they are not ended correctly instead they are ended in group(</page></page></page></page>) at the end of the document due to bs4.
    1. Removing the </page> present at the last of the document
    2. Adding the </page> at required position
    3. Removing any wrong occurence of </page>
    """
    page = str(page.read().decode('utf8')).lower()
    # step 1
    page = page.replace("</page>","")
    #step 2
    page = page.replace("<page>","</page><page>")
    #step 3
    page = page.replace("</page>","",1)
    # sending the correct html data to the parser
    analyzed_data = parser(page)
    print("analysis done...")
    print(analyzed_data)
    """
    Adding the record to pandas dataframe
    """

    for key in analyzed_data.keys():
        for subkey in analyzed_data[key].keys():
            cik_list.at[i, key+"_"+subkey] = analyzed_data[key][subkey]
    
# Convert the dataframe to an XlsxWriter Excel object.
cik_list.to_excel(writer, sheet_name='output')

# Close the Pandas Excel writer and output the Excel file.
writer.save()    
