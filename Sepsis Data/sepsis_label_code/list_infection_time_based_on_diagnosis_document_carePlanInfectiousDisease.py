# integrated infection time information based on results from diagnosis and carePlanInfectiousDisease table

import pandas as pd
import json

file_path = '/Users/xuzhenxing/Documents/eicu-database-2.0/'
infection_from_diagnosis_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'

# read carePlanInfectiousDisease
carePlanInfectiousDisease = pd.read_csv(file_path + 'carePlanInfectiousDisease.csv', index_col=False)
# read from
with open(infection_from_diagnosis_path + 'list_infection_time_from_diagnosis.json', 'r') as load_f:
    list_infection_time_from_diagnosis = json.load(load_f)

count = 0
# list_len_larger is used to count the number of patients whose length of infection time list is more than 0.
list_len_larger = 0

for i in list_infection_time_from_diagnosis:
    count = count + 1
    p_ID = i
    print('p_ID',p_ID)
    infection_dia = list_infection_time_from_diagnosis[p_ID]
    infection_care = list(carePlanInfectiousDisease.loc[carePlanInfectiousDisease['patientunitstayid']==int(p_ID),'cplinfectdiseaseoffset'])

    infection_dia_care = infection_dia + infection_care
    # print('infection_dia', infection_dia)
    # print('infection_care', infection_care)
    # print('infection_dia_care',infection_dia_care)
    #
    # print('set -----',list(set(infection_dia_care)))

    # remove repeat and rank
    infection_dia_care = list(set(infection_dia_care))
    infection_dia_care.sort()
    # print('rank -----', infection_dia_care)

    list_infection_time_from_diagnosis[p_ID] = infection_dia_care

    print('count',count)
    if len(infection_dia_care)>0:
        list_len_larger = list_len_larger +1

print('list_len_larger',list_len_larger)
# save dic file
with open(infection_from_diagnosis_path + "list_infection_time.json", "w") as outfile:
    json.dump(list_infection_time_from_diagnosis, outfile,indent=4)

print('it is over.')



