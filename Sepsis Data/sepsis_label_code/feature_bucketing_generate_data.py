
# generate #   lab_new,  respiratoryCharting_new, nurseCharting_MAP_GCS_new  intakeOutput_new  for feature extracting

import pandas as pd
import numpy as  np
import json
import math

file_path = '/Users/xuzhenxing/Documents/eicu-database-2.0/'
result_path = '/Users/xuzhenxing/Documents/eICU_AKI_Sepsis/'


def extracting_fea(admit_f,discharge_f,feature_name_f, feature_item_f,interval_f,p_ID_f,lab_f,featureDirection_f):

    feature_name_f = feature_name_f
    num_time_slice = math.ceil(discharge_f/interval_f)
    p_ori_infor = lab_f[lab_f['patientunitstayid']==p_ID_f]

    p_ori_infor.to_csv(result_path+'testing/'+str(p_ID_f)+'ori_feature_information.csv',index=False)

    p_result = []

    for i in range(num_time_slice):
        # print('slice_i',i)
        if i==0:
            start = -1440 # lab values is also used before 24h,(1440 min) admitted in ICU
        else:
            start = i * interval_f

        end = (i+1) * interval_f
        if start <= discharge_f:
            fea_ori = list(p_ori_infor.loc[(p_ori_infor['feature_item']==feature_item_f)&(p_ori_infor['feature_offset']>=start)&(p_ori_infor['feature_offset']<=end),'feature_result'])
            # print('fea',feature_item_f,fea_ori)
            if len(fea_ori)>0:
                if featureDirection_f=='min':
                    if feature_name_f =='Urine':
                        max_min_fea = sum(fea_ori) # for urine, we need to sum
                    else:
                        max_min_fea = min(fea_ori)
                else:
                    max_min_fea = max(fea_ori)

                fea_final = max_min_fea
            else:
                fea_final = np.nan # empty

            p_result.append(fea_final)

        else:
            break
    # print('p_result',p_result)
    return p_result




patient = pd.read_csv(file_path+'patient.csv',index_col=False)
patient_ICU_ID = list(set(patient['patientunitstayid']))
print('len(patient_ICU_ID)',len(patient_ICU_ID))

lab_feature = ['PaO2','Bilirubin','Platelets','Creatinine']
lab_feature_source = ['paO2','total bilirubin','platelets x 1000','creatinine']

respiratoryCharting_feature = ['FiO2']
respiratoryCharting_feature_source = ['FIO2 (%)','FiO2']

nurseCharting_feature = ['MAP','GCS']
nurseCharting_feature_source = ['MAP (mmHg)','Arterial Line MAP (mmHg)','Score (Glasgow Coma Scale)','Glasgow coma score'] # in nurseCharting.csv,nurseCharting_feature_source in column "nursingchartcelltypevallabel"

intakeOutput_feature = ['Urine']
intakeOutput_feature_source = [
'Urine, L neph:',
'Urine Output-Urine Output',
'Urine Output-RIGHT Nephrouretero Stent Urine Output',
'Urine Output-Nephrostomy',
'Urine Output-Foley',
'Urine Output-foley',
'Urine Output-FOLEY',
'Urine Output (mL)-Urethral Catheter',
'Urine Output (mL)-Urethral Catheter',
'Urine Output (mL)-Urethral Catheter',
'URINE CATHETER',
'Urine',
'Urinary Catheter Output: Urethral 16 Fr.',
'Urinary Catheter Output: Urethral',
'Urinary Catheter Output: Suprapubic',
'Urinary Catheter Output: Nephrostomy R',
'Urinary Catheter Output: Nephrostomy L',
'Urinary Catheter Output: Coude Urethral 18 Fr.',
'Urinary Catheter Output: Coude Urethral 16 Fr.',
'Urinary Catheter Output: Coude Urethral 14 Fr.',
'Urinary Catheter Output: Coude Urethral',
'Urinary Catheter Output: Condom Urethral',
'Urinary Catheter Output: Condom External'
]

# read lab,  and only select 4 columns: 'patientunitstayid', 'labresultoffset', 'labname', 'labresult', rename columns name
lab = pd.read_csv(file_path+'lab.csv',index_col=False)
lab = lab.loc[lab['labname'].isin(lab_feature_source)]
lab = lab[['patientunitstayid','labresultoffset','labname','labresult']]
lab = lab.rename(columns={"labresultoffset": "feature_offset",
                          "labname": "feature_item",
                          "labresult":"feature_result"
                          })
lab.to_csv(result_path+'testing/lab_new.csv',index=False)


# addressing respiratoryCharting # change FIO2 (%) to FiO2  # rename columns name
respiratoryCharting = pd.read_csv(file_path+'respiratoryCharting.csv',index_col=False)
respiratoryCharting = respiratoryCharting.loc[respiratoryCharting['respchartvaluelabel'].isin(respiratoryCharting_feature_source)] # only extract FiO2 from respiratoryCharting.csv
# respiratoryCharting.loc[respiratoryCharting['respchartvaluelabel']=='FIO2 (%)','respchartvaluelabel'] = 'FiO2'
respiratoryCharting['respchartvaluelabel'] = 'FiO2'
respiratoryCharting = respiratoryCharting[['patientunitstayid','respchartoffset','respchartvaluelabel','respchartvalue']]

respiratoryCharting = respiratoryCharting.rename(columns={"respchartoffset": "feature_offset",
                          "respchartvaluelabel": "feature_item",
                          "respchartvalue":"feature_result"
                          })
respiratoryCharting.to_csv(result_path+'testing/respiratoryCharting_new.csv',index=False)


# addressing nurseCharting, and only select 4 columns ['patientunitstayid','nursingchartoffset','nursingchartcelltypevallabel','nursingchartvalue']
# change 'MAP (mmHg)','Arterial Line MAP (mmHg)',   --> MAP
# change 'Score (Glasgow Coma Scale)','Glasgow coma score' --> GCS
# rename column name
nurseCharting = pd.read_csv(file_path+'nurseCharting.csv',index_col=False)
nurseCharting = nurseCharting.loc[(nurseCharting['nursingchartcelltypevallabel'].isin(nurseCharting_feature_source))&(nurseCharting['nursingchartcelltypevalname'].isin(['GCS Total','Value']))]
nurseCharting = nurseCharting[['patientunitstayid','nursingchartoffset','nursingchartcelltypevallabel','nursingchartvalue']]
nurseCharting.loc[nurseCharting['nursingchartcelltypevallabel'].isin(['MAP (mmHg)','Arterial Line MAP (mmHg)']),'nursingchartcelltypevallabel'] = 'MAP'
nurseCharting.loc[nurseCharting['nursingchartcelltypevallabel'].isin(['Score (Glasgow Coma Scale)','Glasgow coma score']),'nursingchartcelltypevallabel'] = 'GCS'
# rename
nurseCharting = nurseCharting.rename(columns={"nursingchartoffset": "feature_offset",
                          "nursingchartcelltypevallabel": "feature_item",
                          "nursingchartvalue":"feature_result"
                          })

nurseCharting.to_csv(result_path+'testing/nurseCharting_MAP_GCS_new.csv',index=False)


# addressing urine in intakeOutput
intakeOutput = pd.read_csv(file_path+'intakeOutput.csv',index_col=False)
intakeOutput = intakeOutput.loc[intakeOutput['celllabel'].isin(intakeOutput_feature_source)]
intakeOutput = intakeOutput[['patientunitstayid','intakeoutputoffset','celllabel','cellvaluenumeric']]
# change the value in intakeOutput_feature_source --> Urine
intakeOutput['celllabel'] = 'Urine'
# rename
intakeOutput = intakeOutput.rename(columns={"intakeoutputoffset": "feature_offset",
                          "celllabel": "feature_item",
                          "cellvaluenumeric":"feature_result"
                          })

intakeOutput.to_csv(result_path+'testing/intakeOutput_new.csv',index=False)



















