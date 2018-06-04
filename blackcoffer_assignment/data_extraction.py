import numpy as np
import pandas as pd
import nltk
from bs4 import BeautifulSoup

from data_analysis import dataAnalyzer

"""
This function creates an index from the given data
"""

def createIndex(page, max_number_of_pages):
    list_of_items = page.split("\n")
    index = {}
    
    skippable_index = -1
    key = 0
    for i,item in enumerate(list_of_items):
        # print(item+"\n")
        try:
            item = item.replace(".", "")
            list_of_words = nltk.tokenize.word_tokenize(item)
            # print(list_of_words)
            if(i == skippable_index):
                continue
            if(list_of_words[-1].isdigit()):
                index[key] = [item[:item.rfind(" ")],int(list_of_words[-1])]
                key = key + 1
            else:    
                page_number = list_of_items[i+1]
                page_number = page_number.split(" ")
                # k = 1
                # while(int(page_number[-1])>max_number_of_pages or page_number[-1].isdigit() is False):
                #     print("page is greater than maximum page")
                #     page_number = list_of_items[i+1+k]
                #     print("page number  is:")
                #     print(page_number)
                #     page_number = page_number.split(" ")
                #     k = k + 1
                index[key] = [item,int(page_number[-1])]
                skippable_index = i+1
                key = key + 1
        except ValueError as error:
            continue
        except IndexError as error:
            continue    
        
            
    return index

"""
Parser function that parses the file content
"""
def parser(file):
    """
        parsing different sections
        1. management discussion and analysis section
        2. quanttative and qualitative section
        3. risk factor section
    """

    query_Str1 = "management\'s discussion and analysis"
    query_Str2 = "quantitative and qualitative disclosures about market risk"
    query_Str3 = "risk factors"

    analyzed_data = {
            "mda" : {},
            "qqmdr": {},
            "rf": {}
    }
    soup = BeautifulSoup(file, "lxml")
    
    """
    Finding the index table from the page to look for Management's Discussion and Analysis, Quantitative and Qualitative Disclosures about Market Risk, 
    Risk Factors if they exist.
    """
    
    pages = soup.select("page")
    

    #sending the index page to create index
    print("no of pages: {0}".format(len(pages)))
    try:
        if(len(pages)):
            index = createIndex(pages[0].text, len(pages))

            # getting the pagenumbers for required sections
            
            for key,value in index.items():
                
                f_mda = f_qqdmr = f_rf = False
                if value[0].find(query_Str1)!=-1 or value[0].find(query_Str2)!=-1 or value[0].find(query_Str3)!=-1:
                    section=""
                    start_number = index[key][1]
                    end_number = index[key+1][1]
                    k = 2
                    while end_number > len(pages) and key + k < len(index.keys()):
                        print("key = {0}".format(key+k))
                        print(index[key+k][1])
                        end_number = index[key + k][1]
                        k = k + 1
                    print("page number is {0} to {1}".format(start_number, end_number))
                    
                    for i in range(start_number, end_number):
                        print("index = "+str(i))
                        if value[0].find(query_Str1)!=-1:
                            section = section + pages[i].text
                            f_mda = True
                        elif value[0].find(query_Str2)!=-1:
                            section = section + pages[i].text
                            f_qqdmr = True
                        else:
                            section = section + pages[i].text
                            f_rf = True
                    if f_mda:
                        analyzed_data["mda"] = dataAnalyzer(section, 1)        
                    elif f_qqdmr:
                        analyzed_data["qqdmr"] = dataAnalyzer(section, 2)                
                    elif f_rf:
                        analyzed_data["rf"] = dataAnalyzer(section, 3)            
        else:
            pass
    except IndexError:
        f_mda = f_qqdmr = f_rf = False
        print(pages)
        for page in pages:
            page = page.lower()
            if not f_mda or not f_rf or not f_qqdmr or page.find("Part")!=0:
                f_mda = f_rf = f_qqdmr = False    
            elif page.find(query_Str1)!=-1 or f_mda:
                analyzed_data["mda"] = dataAnalyzer(page.text, 1)
                f_mda = True 
                f_rf = False
                f_qqdmr = False
            elif page.find(query_Str2)!=-1 or f_qqdmr:
                analyzed_data["mda"] = dataAnalyzer(page.text, 1)
                f_mda = False 
                f_rf = False
                f_qqdmr = True
            elif page.find(query_Str3)!=-1 or f_rf:
                analyzed_data["mda"] = dataAnalyzer(page.text, 1)
                f_mda = False 
                f_rf = True
                f_qqdmr = False
            
                

    return analyzed_data
    
    
    
#####################################################

