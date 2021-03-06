#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 17:00:58 2020

@author: mikkel
"""
import pandas as pd
import numpy as np

# Function calculating the number an proportional overlap of similar HLA-ligands 
# above a certain threshold BLOSUM-score between two viruses.

def blosumOverlap(blosum, virus1, virus2, virus1_name, virus2_name):
    
    threshold = 0.8
    
    hla_list = ['HLA-A02:01', 'HLA-A01:01', 'HLA-A03:01', 'HLA-A24:02', 'HLA-A11:01', 
                'HLA-A26:01', 'HLA-A32:01', 'HLA-A68:01', 'HLA-A25:01', 'HLA-A31:01', 
                'HLA-A29:02', 'HLA-A23:01', 'HLA-B07:02', 'HLA-B08:01', 'HLA-B15:01', 
                'HLA-B51:01', 'HLA-B44:02', 'HLA-B18:01', 'HLA-B35:01', 'HLA-B44:03', 
                'HLA-B40:01', 'HLA-B13:02', 'HLA-B27:05', 'HLA-B57:01', 'HLA-B35:03', 
                'HLA-B38:01', 'HLA-B58:01', 'HLA-C07:01', 'HLA-C04:01', 'HLA-C07:02', 
                'HLA-C06:02', 'HLA-C12:03', 'HLA-C05:01', 'HLA-C02:02', 'HLA-C03:04', 
                'HLA-C03:03', 'HLA-C01:02', 'HLA-C15:02']
    
    # Creating dataframe to store calculated values for every HLA allele
    df_virus_compare = pd.DataFrame(columns = [virus1_name + ' SB', virus2_name + ' SB', 'Identical Icores', 'Proportional overlap'], index = hla_list)
     
    for i in hla_list:
        # Selecting the rows containing BLOSUM-score above threshold for the current HLA allele
        # and obtaining the I-cores for each HLA allele from the same viruses
        temp_blosum_hla = blosum.loc[blosum['HLA'] == i]
        temp_virus_SP = temp_blosum_hla.loc[temp_blosum_hla['BLOSUM score'] > threshold]
        temp_virus1_hla = virus1.loc[virus1['HLA'] == i]['Icore'].unique()
        temp_virus2_hla = virus2.loc[virus2['HLA'] == i]['Icore'].unique()
        
        # Calculating the number of HLA-ligands in the two viruses and the number of similar 
        # HLA-ligands with a BLOSUM-score above the threshold
        size_of_SB_virus1 = np.size(temp_virus1_hla)
        size_of_SB_virus2 = np.size(temp_virus2_hla)
        size_of_SP = len(temp_virus_SP.index)
        
        # Selecting the peptide space based on the minimum observed HLA-ligands in the two viruses 
        # and calculating the porportional overlap
        peptide_space = min(size_of_SB_virus1, size_of_SB_virus2)
        prop_overlap =  size_of_SP / peptide_space * 100
        
        # Store values as a row in the dataframe
        df_virus_compare.loc[i] = [size_of_SB_virus1 , size_of_SB_virus2, size_of_SP, prop_overlap]
        sorted_df_virus_compare = df_virus_compare.sort_values('Proportional overlap', ascending = False)
     
    return sorted_df_virus_compare


