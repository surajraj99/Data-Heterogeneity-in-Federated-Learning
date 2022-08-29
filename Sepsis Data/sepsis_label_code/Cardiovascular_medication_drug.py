# extract 6 durgs from medication.csv table
#  Dopamine # Dobutamine, Phenylephrine  Vasopressin # Epinephrine # Norepinephrine
# reference: https://github.com/MIT-LCP/eicu-code/blob/master/concepts/pivoted/pivoted-med.sql

import pandas as pd
import numpy as  np
import json

file_path = '/Users/xuzhenxing/Documents/eicu-database-2.0/'
result_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'
weight_path = result_path


# read all patients and  obtain ID
patient = pd.read_csv(file_path + 'patient.csv', index_col=False)
patient_ICU_ID = list(set(patient['patientunitstayid']))

# read basic weight
with open(weight_path + 'patient_basic_information.json', 'r') as load_f:
    basic_weight = json.load(load_f)

# read medication table
medication = pd.read_csv(file_path+'medication.csv',index_col=False)


# add drug name column
medication['drugname_structured'] = ''

medication.loc[medication['drughiclseqno'].isin([2060, 2059]),'drugname_structured'] = 'Dopamine'
medication.loc[medication['drughiclseqno'].isin([8777, 40]),'drugname_structured'] = 'Dobutamine'
medication.loc[medication['drughiclseqno'].isin([37410, 36346, 2051]),'drugname_structured'] = 'Norepinephrine'
medication.loc[medication['drughiclseqno'].isin([37407, 39089, 36437, 34361, 2050]),'drugname_structured'] = 'Epinephrine'
medication.loc[medication['drughiclseqno'].isin([337028, 35517, 35587, 2087]),'drugname_structured'] = 'Phenylephrine'
medication.loc[medication['drughiclseqno'].isin([38884, 38883, 2839]),'drugname_structured'] = 'Vasopressin'

# check the drugname to find these six drugs and assign the new name in drugname_structured

medication.loc[~medication['drugname'].notna(),'drugname'] ='This is NULL'
medication['drugname'] = medication['drugname'].str.lower()

medication.loc[(medication['drugname'].str.contains('dobutamine')),'drugname_structured'] = 'Dobutamine'
medication.loc[(medication['drugname'].str.contains('dobutrex')),'drugname_structured'] = 'Dobutamine'

medication.loc[(medication['drugname'].str.contains('norepinephrine')),'drugname_structured'] = 'Norepinephrine'
medication.loc[(medication['drugname'].str.contains('levophed')),'drugname_structured'] = 'Norepinephrine'

medication.loc[(medication['drugname'].str.contains('epinephrine')),'drugname_structured'] = 'Epinephrine'

medication.loc[(medication['drugname'].str.contains('phenylephrine')),'drugname_structured'] = 'Phenylephrine'

medication.loc[(medication['drugname'].str.contains('vasopressin')),'drugname_structured'] = 'Vasopressin'


df = medication























