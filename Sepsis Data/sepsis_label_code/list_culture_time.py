# generate dic for list_culture_time and save as dic={}, ICUID is key for each patient, and list saves time
# Json file
# there are 2923 patients with culture information
import pandas as pd
import json

file_path = '/Users/xuzhenxing/Documents/eicu-database-2.0/'
result_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'

# read all patients and will use ID
patient = pd.read_csv(file_path+'patient.csv',index_col=False)

patient_ICU_ID = list(set(patient['patientunitstayid']))

microLab = pd.read_csv(file_path+'microLab.csv',index_col=False)

# build a dic for save culture information
dic = {}
count = 0
for i in patient_ICU_ID:
    count = count +1
    print('count',count)
    each_p_ID = i
    print('each_p_ID',each_p_ID)
    culture_inf = list(microLab.loc[microLab['patientunitstayid']==each_p_ID,'culturetakenoffset'])
    if len(culture_inf)>0:
        # print('culture_inf',culture_inf)
        dic[str(each_p_ID)] = culture_inf  # each_p_ID --> str(each_p_ID)

    else:
        dic[str(each_p_ID)] = culture_inf # each_p_ID --> str(each_p_ID)
        print('empty')

    if count>50:
        break

# save dic file
with open(result_path+"list_culture_time.json", "w") as outfile:
    json.dump(dic, outfile,indent=4)

print('it is over.')


