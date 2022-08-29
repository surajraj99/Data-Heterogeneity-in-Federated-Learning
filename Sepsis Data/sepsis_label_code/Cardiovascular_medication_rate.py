# convert uniform unit for  4 durgs Dopamine # Dobutamine, Epinephrine # Norepinephrine   to mcg/kg/min

# Phenylephrine to   standard unit is ug/min  or mcg/min
# Vasopressin to standard unit is  units/min
# and compute drug rate

import pandas as pd
import numpy as  np
import json

file_path = '/Users/xuzhenxing/Documents/eicu-database-2.0/'
result_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'
weight_path = result_path

# read medication_filled_weight table
medication_filled_weight = pd.read_csv(result_path+'medication_filled_weight.csv',index_col=False)
print('len(medication_filled_weight)',len(medication_filled_weight))
# add drug rate column
medication_filled_weight['rate'] = 0
# delete rows whose dosage column is null and >0
medication_filled_weight = medication_filled_weight[medication_filled_weight['dosage'].notna()]

df = medication_filled_weight
medicationid_id = list(df['medicationid'])

print('len(medicationid_id)',len(medicationid_id))


# these 4 drugs standard units is mcg/kg/min
df_Dopamine = ['mcg/kg/min','mg','MG','ML','Ml','mL']
df_Dobutamine = ['mg','MG','ML','mL','mcg/kg/min',]
df_Norepinephrine = ['MG','MCG','mg','ML','mL','mcg/kg/min']
df_Epinephrine = ['mg','MG','ML','mL','MCG','mcg']


df_Phenylephrine = ['mg','ML','MG','mcg','MCG','mL'] # standard unit is ug/min  or mcg/min
df_Vasopressin = ['unit(s)','Units','ml','ML','mL','UNIT','UNITS'] # standard unit is  units/min

# for four drugs
four_uniform_unit_drug_name = ['Dopamine','Dobutamine','Norepinephrine','Epinephrine']
mcg_kg_min_four_drug = ['mcg/kg/min']
mg_MG_four_drug = ['mg','MG']
ml_ML_four_drug = ['ML','Ml','mL','ml']
MCG_four_drug = ['MCG']

# for Phenylephrine
one_Phenylephrine_name = ['Phenylephrine']
mg_MG_one_Phenylephrine = ['mg','MG']
mcg_MCG_one_Phenylephrine = ['mcg','MCG']
ml_ML_one_Phenylephrine = ['ML','mL']

# for Vasopressin drug
one_Vasopressin_name = ['Vasopressin']
unit_one_Vasopression = ['unit(s)','Units','UNIT','UNITS']
ml_one_Vasopression = ['ml','ML','mL']


# df.to_csv(result_path+'testing/medication_filled_weight_without_missing.csv',index=False)

count = 0
abnormal_num = 0

for i in medicationid_id:
    print('count',count)

    count = count + 1

    medicationid = i
    # print('medicationid',medicationid)

    dosage = list(df.loc[df['medicationid']==i,'dosage'])[0]
    # print('dosage',dosage)
    drugname = list(df.loc[df['medicationid']==i,'drugname_structured'])[0]
    weight = list(df.loc[df['medicationid']==i,'patientweight'])[0]
    # print('weight',weight)
    drugstartoffset = list(df.loc[df['medicationid']==i,'drugstartoffset'])[0]

    # drugorderoffset = list(df.loc[df['medicationid']==i,'drugorderoffset'])[0]
    drugstopoffset = list(df.loc[df['medicationid']==i, 'drugstopoffset'])[0]

    # print('drugstartoffset',drugstartoffset)
    # print('drugstopoffset', drugstopoffset)

    duration = abs(drugstopoffset-drugstartoffset)+0.1 # add 0.1 to avoid float division by zero
    # print('duration', duration)

    dosage_value_list = dosage.split(' ')
    dosage_value = dosage_value_list[0]

    # print('dosage_value_list', dosage_value_list)

    # dosage_value_list = [] four_uniform_unit_drug_name = ['Dopamine','Dobutamine','Norepinephrine','Epinephrine']

    rate = 0
    try:
        # addressing units for four drugs
        if drugname in four_uniform_unit_drug_name:
            if len(list(set(dosage_value_list) & set(mcg_kg_min_four_drug)))>0: # the unit is mcg/kg/min
                if dosage_value=='5-20': # addressing "5-20 mcg/kg/min", we use 10 as rate
                    rate = 10.0
                else:
                    rate = float(dosage_value)
            elif len(list(set(dosage_value_list) & set(mg_MG_four_drug)))>0:  # the unit is 'mg','MG'
                rate = (1000*float(dosage_value))/(weight*duration) #
            elif len(list(set(dosage_value_list) & set(ml_ML_four_drug)))>0:  # the unit is 'ml','ML'
                if drugname=='Dopamine':
                    rate = (1600 * float(dosage_value)) / (weight * duration)  # 400mg in 250 ml; https://www.uptodate.com/contents/image?imageKey=PULM%2F99963&topicKey=PULM%2F1613&source=see_link
                if drugname =='Dobutamine':
                    rate = (500*float(dosage_value))/(weight*duration) # 250mg in 500 ml; https://www.uptodate.com/contents/image?imageKey=PULM%2F99963&topicKey=PULM%2F1613&source=see_link

                if drugname == 'Norepinephrine':
                    rate = (16 * float(dosage_value)) / (weight * duration)  # 4mg in 250 ml; https://www.uptodate.com/contents/image?imageKey=PULM%2F99963&topicKey=PULM%2F1613&source=see_link
                if drugname == 'Epinephrine':
                    rate = (4 * float(dosage_value)) / (weight * duration)  # 1 mg in 250 ml; https://www.uptodate.com/contents/image?imageKey=PULM%2F99963&topicKey=PULM%2F1613&source=see_link

            elif len(list(set(dosage_value_list) & set(MCG_four_drug)))>0:  # the unit is 'MCG'
                rate = (float(dosage_value))/(weight*duration)

        # addressing units for one_Phenylephrine_name, standard unit is  ug/min  or mcg/min
        if drugname in one_Phenylephrine_name:
            if len(list(set(dosage_value_list) & set(mg_MG_one_Phenylephrine)))>0:
                rate = (1000*float(dosage_value))/(duration) # add 1 to avoid float division by zero
            elif len(list(set(dosage_value_list) & set(mcg_MCG_one_Phenylephrine)))>0:  # the unit is 'MCG'
                rate = (float(dosage_value))/(duration)
            elif len(list(set(dosage_value_list) & set(ml_ML_one_Phenylephrine)))>0:  # the unit is 'ml','ML'
                rate = (4*float(dosage_value))/(duration) #  10mg in 250 ml; https://www.uptodate.com/contents/image?imageKey=PULM%2F99963&topicKey=PULM%2F1613&source=see_link

        # addressing units for Vasopressin drug standard unit is units/min
        if drugname in one_Vasopressin_name:
            if len(list(set(dosage_value_list) & set(unit_one_Vasopression))) > 0: # the unit is ['unit(s)', 'Units', 'UNIT', 'UNITS']
                rate = float(dosage_value) / (duration)
            elif len(list(set(dosage_value_list) & set(ml_one_Vasopression))) > 0: # the unit is ['ml', 'ML', 'mL']
                rate = (20*float(dosage_value)) / (duration) # 1 ml = 20 units reference https://www.rxlist.com/vasostrict-drug.htm

    except:
        abnormal_num = abnormal_num + 1
        print('abnormal number', abnormal_num)

    df.loc[df['medicationid']==medicationid,'rate'] = rate

    # if count>2000:
    #     break

print('abnormal number', abnormal_num)

df_medication_rate = df
df_medication_rate.to_csv(result_path+'medication_rate.csv',index=False)




















