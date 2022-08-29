#In eICU- CRD, microbiology data were not well populated due to the limited availability of microbiology interfaces; instead, infection was identified according to documented diagnosis.
# reference title: A Machine-Learning Approach for Dynamic Prediction of Sepsis-Induced Coagulopathy in Critically Ill Patients With Sepsis

# generate dic for list_infection_time_based_on_diagnosis_document and save as dic={}, ICUID is key for each patient, and list saves time
# based on diagnosis.csv table

import pandas as pd
import json

file_path = '/Users/xuzhenxing/Documents/eicu-database-2.0/'
result_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'

# read all patients and will use ID
patient = pd.read_csv(file_path + 'patient.csv', index_col=False)
patient_ICU_ID = list(set(patient['patientunitstayid']))
diagnosis = pd.read_csv(file_path + 'diagnosis.csv', index_col=False)

diagnosis_p = set(diagnosis['patientunitstayid'])
print('len(diagnosis_p)',len(diagnosis_p))

# find all rows including "infection" information
diagnosis_infection = diagnosis.astype(str) # convert all items in table into str
diagnosis_infection = diagnosis_infection[diagnosis_infection['diagnosisstring'].str.contains('infect|sepsis')]  # keep rows with "infection" or "infections",or"sepsis"
diagnosis_infection.to_csv(result_path+'diagnosis_infection.csv',index=False)

# build dic to save infection time
infection_time = {}
count_flag = 0
num_p_infection_time_larger_0 = 0

for i in patient_ICU_ID:
    count_flag = count_flag + 1
    p_ID = i # i is int in patient_ICU_ID
    print('p_ID',p_ID)
    p_infection_time = diagnosis_infection.loc[diagnosis_infection['patientunitstayid']==str(p_ID),'diagnosisoffset'] # note that, str(p_ID), because we have addreesed in above lines: diagnosis.astype(str)
    # print('p_infection_time_ori',p_infection_time)
    p_infection_time = list(set(p_infection_time))
    # print('p_infection_time_remove_repeat', p_infection_time)

    # convert item to int and rank
    p_infection_time = list(map(int, p_infection_time))
    p_infection_time.sort()
    # print('p_infection_time_order', p_infection_time)

    infection_time[str(p_ID)] = p_infection_time
    if len(p_infection_time)>0:
        num_p_infection_time_larger_0 = num_p_infection_time_larger_0 + 1
    print('count_flag', count_flag)

    # if count_flag==50:
    #     break

print('len(num_p_infection_time_larger_0)',num_p_infection_time_larger_0)
# save dic file
with open(result_path + "list_infection_time_from_diagnosis.json", "w") as outfile:
    json.dump(infection_time, outfile,indent=4)

print('it is over.')



