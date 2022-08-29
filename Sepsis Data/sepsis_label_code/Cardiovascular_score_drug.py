# generate drugs of cardiovascular score and rate
#'Dopamine','Norepinephrine','Dobutamine','Epinephrine','Phenylephrine','Vasopressin'
# Note that: the unit of 'Dopamine','Norepinephrine','Dobutamine','Epinephrine',   is mcg/kg/min
# 'Phenylephrine'  the unit is mcg/min
#  'Vasopressin'  the unit is min

import pandas as pd
import json

file_path = '/Users/xuzhenxing/Documents/eicu-database-2.0/'
result_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'
weight_path = result_path


# read all patients and  obtain ID
patient = pd.read_csv(file_path + 'patient.csv', index_col=False)
patient_ICU_ID = list(set(patient['patientunitstayid']))

# read medication_rate table, which has standard drug rate
medication_rate = pd.read_csv(result_path+'medication_rate.csv',index_col=False)
patient_only_drug = len(set(medication_rate['patientunitstayid']))
print('len(patient_only_drug)',patient_only_drug)

# infusionDrug = infusionDrug
drugList = ['Dopamine','Norepinephrine','Dobutamine','Epinephrine','Phenylephrine','Vasopressin']
# # build a dic to save cardiovascular drug records
cardiovascular_score_drug = {}

medication_rate = medication_rate
medication_rate['rate']=medication_rate['rate'].round(4)

count = 0
for i in patient_ICU_ID:
    print('count',count)

    p_ID = i
    print('p_ID',p_ID)
    p_infusionDrug = medication_rate.loc[medication_rate['patientunitstayid']==p_ID]
    p_infusionDrug_each = {}

    for j in drugList:
        # print("p_infusionDrug",p_infusionDrug)

        p_each_drug = p_infusionDrug[p_infusionDrug['drugname_structured'] == j]

        # rank by drug_time in terms of each drug
        df = p_each_drug
        df['drug_time_Rank'] = df['drugstartoffset'].rank(ascending=1)

        # df['drug_time_Rank'] = df['drugorderoffset'].rank(ascending=1)

        df = df.set_index('drug_time_Rank')
        df = df.sort_index()

        p_drug_time_rate = {}

        p_drug_time_rate['drug_start'] = list(df['drugstartoffset'])
        p_drug_time_rate['drug_end'] = list(df['drugstopoffset'])
        p_drug_time_rate['rate'] = list(df['rate'])

        p_infusionDrug_each[j] = p_drug_time_rate

    cardiovascular_score_drug[str(i)] = p_infusionDrug_each

    count = count +1
    # if count>200:
    #     break

# save dic file
with open(result_path + "cardiovascular_score_drug.json", "w") as outfile:
    json.dump(cardiovascular_score_drug, outfile,indent=4)

print('it is over.')



