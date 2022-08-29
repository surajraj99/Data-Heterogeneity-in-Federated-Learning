# generate dic for list_infection_time and save as dic={}, ICUID is key for each patient, and list saves time
# based on list_culture_time; list_antibiotic_time

import pandas as pd
import json

file_path_patient = '/Users/xuzhenxing/Documents/eicu-database-2.0/'

file_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'

# read all patients and will use ID
patient = pd.read_csv(file_path_patient + 'patient.csv', index_col=False)
patient_ICU_ID = list(set(patient['patientunitstayid']))

with open(file_path + 'list_antibiotic_time_without_72_with_all_route.json', 'r') as load_f:
    list_antibiotic_time_without_72h_consider = json.load(load_f)

with open(file_path + 'list_culture_time.json', 'r') as load_f:
    list_culture_time = json.load(load_f)
# save infection time for each patient, all_infection_time  is a dic, ICUID is key for each patient, and list saves time
all_infection_time = {}
count = 0
m = 0
num_antibiotic_time = 0
num_culture_time = 0
count_infection = 0

for p in patient_ICU_ID:
    count = count + 1
    print('count', count)

    p_ID = str(p)
    print('p_ID', p_ID)

    p_antibiotic_time = list_antibiotic_time_without_72h_consider[p_ID]

    print('p_antibiotic_time', p_antibiotic_time)

    p_culture_time = list_culture_time[p_ID]
    print('p_culture_time', p_culture_time)

    infection_time = []

    if len(p_antibiotic_time) > 0:
        num_antibiotic_time = num_antibiotic_time + 1

    if len(p_culture_time) > 0:
        num_culture_time = num_culture_time + 1

    if len(p_antibiotic_time) > 0 and len(p_culture_time) > 0:

        m = m + 1
        print('length of m_both_time larger 0',m)

        # rank and remove repeat time item
        p_antibiotic_time = list(set(p_antibiotic_time))
        p_antibiotic_time.sort()

        p_culture_time = list(set(p_culture_time))
        p_culture_time.sort()

        # if antibiotic time first, If antibiotics were given  first, then the cultures must have been obtained within 24 hours (24*60 = 1440 mins).
        antibiotic_time_first_based_infection_time = []
        for i in p_antibiotic_time:
            for j in p_culture_time:
                if j - i < 1440:  # 24 hour
                    antibiotic_time_first_based_infection_time.append(i)
        # if culture time first,  If cultures were obtained  first, then antibiotic must have been ordered within 72 hours (72*60 = 4320 mins).
        culture_time_first_based_infection_time = []
        for ii in p_culture_time:
            for jj in p_antibiotic_time:
                if jj - ii < 4320:
                    culture_time_first_based_infection_time.append(ii)

        # combine  culture_time_first_based_infection_time and  culture_time_first_based_infection_time
        infection_time = infection_time + antibiotic_time_first_based_infection_time + culture_time_first_based_infection_time
        if len(antibiotic_time_first_based_infection_time) > 0 and len(culture_time_first_based_infection_time) > 0:
            print('count_infection', count_infection)
            count_infection = count_infection + 1

        print('infection_time', infection_time)
        infection_time = list(set(infection_time))
        infection_time.sort()

    all_infection_time[p_ID] = infection_time

# save dic file
with open(file_path + "list_all_infection_time.json", "w") as outfile:
    json.dump(all_infection_time, outfile,indent=4)

print('it is over.')


print('num_antibiotic_time', num_antibiotic_time)
print('num_culture_time',num_culture_time)
print('num_antibiotic_time and num_culture_time',m)
print('count_infection',count_infection)

print('sssssss')



