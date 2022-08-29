# extract 6 durgs from infusionDrug_filled_weight and convert their unit into mcg/kg/min
#  Dopamine # Dobutamine, Phenylephrine  Vasopressin # Epinephrine # Norepinephrine

import pandas as pd
import numpy as  np
import json

file_path = '/Users/xuzhenxing/Documents/eicu-database-2.0/'
result_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'
weight_path = result_path


# read all patients and  obtain ID
patient = pd.read_csv(file_path + 'patient.csv', index_col=False)
patient_ICU_ID = list(set(patient['patientunitstayid']))

# read infusion table
infusionDrug_filled_weight = pd.read_csv(result_path+'infusionDrug_filled_weight.csv',index_col=False)

# read medication table
medication = pd.read_csv(file_path+'medication.csv',index_col=False)

# compute  in a uniform unit for each drug (Dopamine,Dobutamine,Epinephrine,Norepinephrine) based on infusionDrug_filled_weight
infusionDrug = infusionDrug_filled_weight
print('len(infusionDrug)',len(infusionDrug))

# filtering records with for example, non in drug_rate
#(1) drug_rate without missing
infusionDrug = infusionDrug[(infusionDrug['drugrate'].notna())&(~infusionDrug['drugrate'].isin(['off','OFF','ERROR','0','UD']))]
#(2) drug_infusionoffset without missing; there is no rows with missing in infusionoffset column
# infusionDrug = infusionDrug[(infusionDrug['infusionoffset'].notna())]

print('len(infusionDrug)_without nan in drugrate',len(infusionDrug)) #

# infusionDrug = infusionDrug[infusionDrug['drugamount']==0] There is no records for drugamount == 0

# for  drug--Dopamine
Dopamine_mcg_kg_min = ['Dopamine','Dopamine ()','Dopamine (Unknown)','DOPamine MAX 800 mg Dextrose 5% 250 ml  Premix (mcg/kg/min)',
                       'dopamine (mcg/kg/min)','Dopamine (mcg/kg/min)','DOPamine STD 15 mg Dextrose 5% 250 ml  Premix (mcg/kg/min)','DOPamine STD 400 mg Dextrose 5% 250 ml  Premix (mcg/kg/min)',
                       'DOPamine STD 400 mg Dextrose 5% 500 ml  Premix (mcg/kg/min)']
Dopamine_mcg_kg_hr = ['Dopamine (mcg/kg/hr)',]
Dopamine_ng_kg_min = ['Dopamine (nanograms/kg/min)']

Dopamine_mcg_hr = ['Dopamine (mcg/hr)',]
Dopamine_mcg_min = ['Dopamine (mcg/min)']

Dopamine_mg_hr = ['Dopamine (mg/hr)',]
Dopamine_ml_hr = ['Dopamine (ml/hr)']

Dopamine_name = Dopamine_mcg_kg_min + Dopamine_mcg_kg_hr + Dopamine_ng_kg_min + Dopamine_mcg_hr + Dopamine_mcg_min + Dopamine_mg_hr + Dopamine_ml_hr

# for drug_Norepinephrine
Norepinephrine_mcg_kg_min = ['Norepinephrine', 'Norepinephrine (Unknown)','Norepinephrine (mcg/kg/min)']
Norepinephrine_mcg_kg_hr = ['Norepinephrine (mcg/kg/hr)']
Norepinephrine_mg_kg_min = ['Norepinephrine (mg/kg/min)']

Norepinephrine_mcg_min = ['Norepinephrine (units/min)',
                          'Norepinephrine MAX 32 mg Dextrose 5% 250 ml (mcg/min)',
                          'Norepinephrine MAX 32 mg Dextrose 5% 500 ml (mcg/min)',
                          'Norepinephrine STD 32 mg Dextrose 5% 282 ml (mcg/min)'
                        , 'Norepinephrine STD 32 mg Dextrose 5% 500 ml (mcg/min)'
                        , 'Norepinephrine STD 4 mg Dextrose 5% 250 ml (mcg/min)'
                        , 'Norepinephrine STD 4 mg Dextrose 5% 500 ml (mcg/min)'
                        , 'Norepinephrine STD 8 mg Dextrose 5% 250 ml (mcg/min)'
                        , 'Norepinephrine STD 8 mg Dextrose 5% 500 ml (mcg/min)'
                        , 'Norepinephrine (mcg/min)'
                        , 'Levophed (mcg/kg/min)'
                        , 'levophed  (mcg/min)'
                        , 'levophed (mcg/min)'
                        , 'Levophed (mcg/min)']
Norepinephrine_mcg_hr = ['Norepinephrine (mcg/hr)']

Norepinephrine_mg_min = ['Norepinephrine (mg/min)']
Norepinephrine_mg_hr = ['Norepinephrine (mg/hr)','Levophed (mg/hr)','Norepinephrine ()']

Norepinephrine_ml_hr = ['Norepinephrine (ml/hr)'
                        , 'norepinephrine Volume (ml) (ml/hr)'
                        , 'levophed (ml/hr)'
                        , 'Levophed (ml/hr)'
                        , 'NSS with LEVO (ml/hr)'
                        , 'NSS w/ levo/vaso (ml/hr)','norepinephrine Volume (ml)']

Norepinephrine_name = Norepinephrine_mcg_kg_min + Norepinephrine_mcg_kg_hr + Norepinephrine_mg_kg_min + Norepinephrine_mcg_min + Norepinephrine_mcg_hr + Norepinephrine_mg_min + Norepinephrine_mg_hr + Norepinephrine_ml_hr

# for drug_dobutamine
Dobutamine_mcg_kg_min = ['dobutrex (mcg/kg/min)']
Dobutamine_mg_kg_min = ['dobutrex (mg/kg/min)']

Dobutamine_name = Dobutamine_mcg_kg_min + Dobutamine_mg_kg_min


# for drug_Epinephrine
Epinephrine_mcg_kg_min = ['Epinephrine','Epinephrine (mcg/kg/min)']
Epinephrine_mg_kg_min = ['Epinephrine (mg/kg/min)']

Epinephrine_mcg_min = ['EPI (mcg/min)'
                    , 'Epinepherine (mcg/min)'
                    , 'EPINEPHrine(Adrenalin)MAX 30 mg Sodium Chloride 0.9% 250 ml (mcg/min)'
                    , 'EPINEPHrine(Adrenalin)STD 4 mg Sodium Chloride 0.9% 250 ml (mcg/min)'
                    , 'EPINEPHrine(Adrenalin)STD 4 mg Sodium Chloride 0.9% 500 ml (mcg/min)'
                    , 'EPINEPHrine(Adrenalin)STD 7 mg Sodium Chloride 0.9% 250 ml (mcg/min)'
                    , 'Epinephrine (mcg/min)']
Epinephrine_mcg_hr = ['Epinephrine (mcg/hr)','Epinephrine ()']
Epinephrine_mg_hr = ['Epinephrine (mg/hr)']
Epinephrine_ml_hr = ['Epinephrine (ml/hr)']

Epinephrine_name = Epinephrine_mcg_kg_min + Epinephrine_mg_kg_min + Epinephrine_mcg_min + Epinephrine_mcg_hr + Epinephrine_mg_hr + Epinephrine_ml_hr


# for drug Phenylephrine

Phenylephrine_mcg_kg_min = ['Phenylephrine','Phenylephrine (mcg/kg/min)', 'Phenylephrine (mcg/kg/min) (mcg/kg/min)']
Phenylephrine_mg_kg_min = ['Phenylephrine (mg/kg/min)']
Phenylephrine_mcg_min = ['Phenylephrine  MAX 100 mg Sodium Chloride 0.9% 250 ml (mcg/min)',
                         'Phenylephrine (mcg/min)',
                         'Phenylephrine (mcg/min) (mcg/min)',
                        'Phenylephrine  STD 20 mg Sodium Chloride 0.9% 250 ml (mcg/min)',
                        'Phenylephrine  STD 20 mg Sodium Chloride 0.9% 500 ml (mcg/min)']
Phenylephrine_mcg_hr = ['Phenylephrine (mcg/hr)']
Phenylephrine_mg_hr = [ 'Phenylephrine ()','Phenylephrine (mg/hr)']
Phenylephrine_ml_hr = ['Phenylephrine (ml/hr)','Volume (ml) Phenylephrine','Volume (ml) Phenylephrine ()']

Phenylephrine_name = Phenylephrine_mcg_kg_min + Phenylephrine_mg_kg_min + Phenylephrine_mcg_min + Phenylephrine_mcg_hr + Phenylephrine_mg_hr + Phenylephrine_ml_hr

# for drug Vasopressin
Vasopressin_mcg_kg_min = ['Vasopressin','Vasopressin (Unknown)','Vasopressin (units/kg/min)','Vasopressin (mcg/kg/min)']
Vasopressin_mcg_kg_hr = ['Vasopressin 40 Units Sodium Chloride 0.9% 100 ml (units/kg/hr)']

Vasopressin_mcg_min = ['Vasopressin ()'
                        'Vasopressin 40 Units Sodium Chloride 0.9% 100 ml (units/min)'
                        , 'Vasopressin 40 Units Sodium Chloride 0.9% 100 ml (Unknown)'
                        , 'Vasopressin 40 Units Sodium Chloride 0.9% 200 ml (units/min)'
                        , 'Vasopressin (mcg/min)'
                        , 'vasopressin (units/min)'
                        , 'Vasopressin (units/min)'
                        , 'VAsopressin (units/min)'
                       ]
Vasopressin_mcg_hr = ['Vasopressin 20 Units Sodium Chloride 0.9% 100 ml (units/hr)'
                        , 'Vasopressin 20 Units Sodium Chloride 0.9% 250 ml (units/hr)'
                        , 'Vasopressin 40 Units Sodium Chloride 0.9% 100 ml (units/hr)'
                        , 'Vasopressin (units/hr)']

Vasopressin_ml_hr = ['vasopressin (ml/hr)', 'Vasopressin (ml/hr)']

Vasopressin_mg_hr = ['Vasopressin (mg/hr)']
Vasopressin_mg_min = ['Vasopressin (mg/min)']

Vasopressin_name = Vasopressin_mcg_kg_min + Vasopressin_mcg_kg_hr + Vasopressin_mcg_min + Vasopressin_mcg_hr + Vasopressin_ml_hr + Vasopressin_mg_hr + Vasopressin_mg_min


# combine all drugs units, there are 9 lists for units
mcg_kg_min = Dopamine_mcg_kg_min + Norepinephrine_mcg_kg_min + Dobutamine_mcg_kg_min + Epinephrine_mcg_kg_min + Phenylephrine_mcg_kg_min + Vasopressin_mcg_kg_min
mcg_kg_hr = Dopamine_mcg_kg_hr + Norepinephrine_mcg_kg_hr + Vasopressin_mcg_kg_hr
ng_kg_min = Dopamine_ng_kg_min
mg_kg_min = Norepinephrine_mg_kg_min + Dobutamine_mg_kg_min + Epinephrine_mg_kg_min + Phenylephrine_mg_kg_min

mcg_hr = Dopamine_mcg_hr + Norepinephrine_mcg_hr + Epinephrine_mcg_hr + Phenylephrine_mcg_hr + Vasopressin_mcg_hr
mcg_min = Dopamine_mcg_min + Norepinephrine_mcg_min + Epinephrine_mcg_min + Phenylephrine_mcg_min + Vasopressin_mcg_min
mg_min = Norepinephrine_mg_min + Vasopressin_mg_min
mg_hr = Dopamine_mg_hr + Norepinephrine_mg_hr + Epinephrine_mg_hr + Phenylephrine_mg_hr + Vasopressin_mg_hr
ml_hr = Dopamine_ml_hr + Norepinephrine_ml_hr + Epinephrine_ml_hr + Phenylephrine_ml_hr + Vasopressin_ml_hr


# only focus on 6 drugs
drug_name_six = mcg_kg_min + mcg_kg_hr + ng_kg_min + mg_kg_min + mcg_hr + mcg_min + mg_min + mg_hr + ml_hr
infusionDrug = infusionDrug.loc[infusionDrug['drugname'].isin(drug_name_six)]

# using medication table to extract these 6 drugs

medication = medication.loc[medication['drugname'].isin(drug_name_six)]
medication.to_csv(result_path+'medication_6.csv',index=False)

print('sssssss')
# add three columns that is used to save infusion_start, infusion_end, and value
infusionDrug['drug_standard_rate'] = 0
infusionDrug['drug_start'] = 0
infusionDrug['drug_end'] = 0
infusionDrug['drug_duration'] = 0


# drop outlier rows for example: drugrate values are ['UD','OFF',....] base on infusiondrugid
#Outliers
# 30\.br\
# 50 mcg/min
# 50mcg/min\.br\
# Date\Time Correction
# Documentation undone
# OFF\.br\
# OFF\.br\\.br\
outlier_infusiondrugid = [74337607,74899582,74549893,17126335,74404071,
74631589,
74622962,
1965005,
2008197,
1971092,
1966796]

# addressing drugrate, keep drugrate>0
infusionDrug = infusionDrug[~infusionDrug['infusiondrugid'].isin(outlier_infusiondrugid)]
infusionDrug["drugrate"] = pd.to_numeric(infusionDrug["drugrate"], downcast="float")
infusionDrug = infusionDrug[infusionDrug['drugrate']>0]

# addressing drug_start, because there is no missing for infusionoofset, we directly cope the infusionoff for drug_start
infusionDrug["infusionoffset"] = pd.to_numeric(infusionDrug["infusionoffset"], downcast="float")
infusionDrug["drug_start"] = infusionDrug["infusionoffset"]


print('len(infusionDrug)',len(infusionDrug))

# convert unit to stardard rate (mcg/kg/min)
    # microgram (mcg,ug), nanogram (ng), milligram (mg)
    # 1 ng = 0.001 mcg;


df = infusionDrug
# addressing: mcg_kg_min   it is standard, the unit of drugamount is mg
# df.loc[df['drugname'].isin(mcg_kg_min), 'drug_standard_rate'] = df.loc[df['drugname'].isin(mcg_kg_min), 'drugrate']
# df.loc[df['drugname'].isin(mcg_kg_min), 'drug_duration'] = (1000*df.loc[df['drugname'].isin(mcg_kg_min), 'drugamount'])/((df.loc[df['drugname'].isin(mcg_kg_min), 'drugrate'])*(df.loc[df['drugname'].isin(mcg_kg_min), 'patientweight']))

# addressing_mcg_kg_hr;  mcg_kg_hr/60
# df.loc[df['drugname'].isin(mcg_kg_hr), 'drug_standard_rate'] = df.loc[df['drugname'].isin(mcg_kg_hr), 'drugrate']/60 # 1hour
# df.loc[df['drugname'].isin(mcg_kg_hr), 'drug_duration'] = (1000*df.loc[df['drugname'].isin(mcg_kg_hr), 'drugamount'])/((df.loc[df['drugname'].isin(mcg_kg_hr), 'drugrate']/60)*(df.loc[df['drugname'].isin(mcg_kg_hr), 'patientweight']))

# # addressing ng_kg_min 1 ng = 0.001 ug (mcg)
# df.loc[df['drugname'].isin(ng_kg_min), 'drug_standard_rate'] = df.loc[df['drugname'].isin(ng_kg_min), 'drugrate']*0.001
# df.loc[df['drugname'].isin(ng_kg_min), 'drug_duration'] = (1000*df.loc[df['drugname'].isin(ng_kg_min), 'drugamount'])/((0.001*df.loc[df['drugname'].isin(ng_kg_min), 'drugrate'])*(df.loc[df['drugname'].isin(ng_kg_min), 'patientweight']))

# # addressing mg_kg_min, 1 mg = 1000 ug (mcg)
# df.loc[df['drugname'].isin(mg_kg_min), 'drug_standard_rate'] = df.loc[df['drugname'].isin(mg_kg_min), 'drugrate']*1000 #
# df.loc[df['drugname'].isin(mg_kg_min), 'drug_duration'] = (1000*df.loc[df['drugname'].isin(mg_kg_min), 'drugamount'])/((1000*df.loc[df['drugname'].isin(mg_kg_min), 'drugrate'])*(df.loc[df['drugname'].isin(mg_kg_min), 'patientweight']))

# addressing mcg_hr, mcg_hr/ (weight*60)  1h = 60 mins
# df.loc[df['drugname'].isin(mcg_hr), 'drug_standard_rate'] = (df.loc[df['drugname'].isin(mcg_hr), 'drugrate'])/(df.loc[df['drugname'].isin(mcg_hr), 'patientweight'])/60 #
# df.loc[df['drugname'].isin(mcg_hr), 'drug_duration'] = (1000*df.loc[df['drugname'].isin(mcg_hr), 'drugamount'])/(df.loc[df['drugname'].isin(mcg_hr), 'drugrate']/60) # note that, do not consider weight



# # addressing mcg_min  mcg_min/ (weight)
# df.loc[df['drugname'].isin(mcg_min), 'drug_standard_rate'] = (df.loc[df['drugname'].isin(mcg_min), 'drugrate'])/(df.loc[df['drugname'].isin(mcg_min), 'patientweight']) #
#
# # addressing mg_min  mg_min -> mg_min *1000/weight
# df.loc[df['drugname'].isin(mg_min), 'drug_standard_rate'] = (df.loc[df['drugname'].isin(mg_min), 'drugrate'])/(df.loc[df['drugname'].isin(mg_min), 'patientweight'])*1000 #
#
# # addressing mg_hr , *1000/60/weight
# df.loc[df['drugname'].isin(mg_hr), 'drug_standard_rate'] = (df.loc[df['drugname'].isin(mg_hr), 'drugrate'])/(df.loc[df['drugname'].isin(mg_hr), 'patientweight'])/60*1000 #
#
# # addressing ml_hr , 1 ml = 1000 mg = 1000000 mcg
# df.loc[df['drugname'].isin(ml_hr), 'drug_standard_rate'] = (df.loc[df['drugname'].isin(ml_hr), 'drugrate'])/(df.loc[df['drugname'].isin(ml_hr), 'patientweight'])/60*1000000 #
#
# df["drug_standard_rate"]=df["drug_standard_rate"].round(4)

#
df.to_csv(result_path + 'testing/drugs_unit_converted.csv', index=False)

#
# infusionDrug = df
# # use standard name for each drugs
# Dopamine_name = Dopamine_name
# Norepinephrine_name = Norepinephrine_name
# Dobutamine_name = Dobutamine_name
# Epinephrine_name = Epinephrine_name
# Phenylephrine_name = Phenylephrine_name
# Vasopressin_name = Vasopressin_name
#
# infusionDrug.loc[infusionDrug['drugname'].isin(Dopamine_name),'drugname'] = 'Dopamine'
# infusionDrug.loc[infusionDrug['drugname'].isin(Norepinephrine_name),'drugname'] = 'Norepinephrine'
# infusionDrug.loc[infusionDrug['drugname'].isin(Dobutamine_name),'drugname'] = 'Dobutamine'
#
# infusionDrug.loc[infusionDrug['drugname'].isin(Epinephrine_name),'drugname'] = 'Epinephrine'
# infusionDrug.loc[infusionDrug['drugname'].isin(Phenylephrine_name),'drugname'] = 'Phenylephrine'
# infusionDrug.loc[infusionDrug['drugname'].isin(Vasopressin_name),'drugname'] = 'Vasopressin'
#
# # infusionDrug.to_csv(result_path + 'testing/drugs_change_name.csv', index=False)
#
# infusionDrug = infusionDrug
# drugList = ['Dopamine','Norepinephrine','Dobutamine','Epinephrine','Phenylephrine','Vasopressin']
# # build a dic to save cardiovascular drug records
# cardiovascular_score_drug = {}
#
# count = 0
# for i in patient_ICU_ID:
#     print('count',count)
#
#     p_ID = i
#     print('p_ID',p_ID)
#     p_infusionDrug = infusionDrug.loc[infusionDrug['patientunitstayid']==p_ID]
#     p_infusionDrug_each = {}
#
#     for j in drugList:
#         # print("p_infusionDrug",p_infusionDrug)
#
#         p_each_drug = p_infusionDrug[p_infusionDrug['drugname'] == j]
#
#         # rank by drug_time in terms of each drug
#         df = p_each_drug
#         df['drug_time_Rank'] = df['drug_time'].rank(ascending=1)
#         df = df.set_index('drug_time_Rank')
#         df = df.sort_index()
#
#         p_drug_time_rate = {}
#         p_drug_time_rate['time'] = list(df['drug_time'])
#         p_drug_time_rate['rate'] = list(df['drug_standard_rate'])
#
#         p_infusionDrug_each[j] = p_drug_time_rate
#
#     cardiovascular_score_drug[str(i)] = p_infusionDrug_each
#
#     count = count +1
#     # if count>20:
#     #     break
#
# print('ss')
#
# # save dic file
# with open(result_path + "cardiovascular_score_drug.json", "w") as outfile:
#     json.dump(cardiovascular_score_drug, outfile,indent=4)
#
# print('it is over.')
























