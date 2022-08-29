# build a json file to save basic information for each patient
import pandas as pd
import numpy as  np
import json

file_path = '/Users/xuzhenxing/Documents/eicu-database-2.0/'
result_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'
weight_path = result_path

# read basic weight
with open(weight_path + 'patient_basic_information.json', 'r') as load_f:
    basic_weight = json.load(load_f)


# read infusion table
infusionDrug = pd.read_csv(file_path+'infusionDrug.csv',index_col=False)

# infusionDrug = infusionDrug.head(1000) # testing

patient_ID_s = list(set(infusionDrug['patientunitstayid']))
print('patient_ID_s',len(patient_ID_s))

# add three columns that is used to save infusion_start, end, and value
infusionDrug['drug_start'] = 0
infusionDrug['drug_end'] = 0
infusionDrug['drug_value'] = 0

# fill weight with missing using value from basic weight
count = 0
for p in patient_ID_s:
    p_ID = p
    # print('p_ID', p_ID)
    p_basic_weight = basic_weight[str(p_ID)]["Weight"]

    # p_testing_before = infusionDrug.loc[infusionDrug['patientunitstayid']==p_ID]
    # p_testing_before.to_csv(result_path+'testing/testing_'+str(p_ID)+'before.csv',index=False)

    # fill missing weight
    infusionDrug.loc[(infusionDrug['patientunitstayid']==p_ID) & (pd.isnull(infusionDrug['patientweight'])),'patientweight'] = p_basic_weight

    # p_testing_after = infusionDrug.loc[infusionDrug['patientunitstayid']==p_ID]
    # p_testing_after.to_csv(result_path+'testing/testing'+str(p_ID)+'_after.csv',index=False)
    # print('p_basic_weight', p_basic_weight)

    count = count + 1
    print('count',count)

    # if count>10:
    #     break


num_missing_weight = infusionDrug.loc[pd.isnull(infusionDrug['patientweight']),'patientunitstayid']

print('len(num_missing_weight)',len(set(num_missing_weight)))

infusionDrug.to_csv(result_path+'infusionDrug_filled_weight.csv',index=False)


# compute  in a uniform unit for each drug (Dopamine,Dobutamine,Epinephrine,Norepinephrine)

# first drug--Dopamine
















