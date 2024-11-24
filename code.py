import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

students_df=pd.read_csv('Students.csv')
students_df.index=range(1,len(students_df)+1)
students_job_data_df=pd.read_csv('students_job_data_df.csv')


st.title("Enter Student Salary Details")

GWID=st.selectbox("Select GWID",['Select a GWID']+students_df['GWID'].unique().tolist())

if GWID!='Select a GWID':
    st.write("Name for selected GWID:",students_df[students_df['GWID']==GWID])

data_source=st.selectbox("Select Source of Information:",['Select an option',
                                                          'Word of Mouth',
                                                          'Email',
                                                          'Survey Respnse'])
job_seeking_status=st.selectbox("Job Seeking Status:",['Select an option',
                                                       'Employed',
                                                       'Seeking Employment',
                                                       'Not Seeking Employment'])

submitted=None
if job_seeking_status=='Employed':
    with st.form('Enter Student Details'):
        base_salary=st.number_input('Enter Base Salary in $:',value=0,step=1000)
        Bonus = st.number_input("Enter Bonus in $:",value=0,step=1000)
        job_title=st.text_input('Enter Job Title:')
        job_function=st.selectbox("Select a Job Function",['Select an option',
                                                           'Consulting',
                                                           'Finance / Accounting',
                                                           'General Management',
                                                           'Human Resources',
                                                           'Marketing/Sales',
                                                           'Information Technology',
                                                           'Operations / Logistics',
                                                           'Other Job Functions'])
        company_name=st.text_input('Enter Company Name')    
        industry=st.selectbox("Select a Job Function",['Consulting',
                                                       'Consumer Packaged Goods',
                                                       'Energy',
                                                       'Financial Services',
                                                       'Government',
                                                       'Healthcare (Including Products & Services)',
                                                       'Hospitality',
                                                       'Manufacturing',
                                                       'Media / Entertainment',
                                                       'Non-Profit',
                                                       'Real Estate',
                                                       'Retail',
                                                       'Technology',
                                                       'Transport & Logistics Services',
                                                       'Other'])
        job_acceptance_date=st.date_input('Select Job Acceptance Date',datetime.now())
        Job_at_graduation=st.selectbox('Job accepted at the time of graduation',['Select an option','Yes','No'])
        Job_3_months=st.selectbox('Job accepted three months after graduation',['Select an option','Yes','No'])
                                   
        job_title=job_title.capitalize()
        data_entry_timestamp=datetime.now()
        reason_not_seeking_employment=None
        submitted = st.form_submit_button("Submit")

elif job_seeking_status=='Seeking Employment':
    with st.form('Enter Student Details'):
        data_entry_timestamp=datetime.now()
        st.write("Click on submit icon to update details")
        base_salary=None
        Bonus=None
        job_title=None
        job_function=None
        company_name=None
        industry=None
        job_acceptance_date=None
        Job_at_graduation=None
        job_title=None
        Job_3_months=None
        reason_not_seeking_employment=None
        submitted = st.form_submit_button("Submit")

elif job_seeking_status=='Not Seeking Employment':
    with st.form('Enter Student Details'):
        reason_not_seeking_employment=st.selectbox('Select reason for not seeking employment',
                            ['Select an option',
                             'Company-Sponsored Studies',
                             'Continuing Education',
                             'Postponing Job Search',
                             'Starting a New Business',
                             'Not Seeking for other Reasons'])
        base_salary=None
        Bonus=None
        job_title=None
        job_function=None
        company_name=None
        industry=None
        job_acceptance_date=None
        Job_at_graduation=None
        Job_3_months=None
        job_title=None
        data_entry_timestamp=datetime.now()
        submitted = st.form_submit_button("Submit")


if submitted:
    new_row=pd.DataFrame({'GWID':GWID,
                          'Name':students_df[students_df['GWID']==GWID]['Name'],
                          'data_source':data_source,
                          'job_seeking_status':job_seeking_status,
                          'base_salary':base_salary,
                          'Bonus':Bonus,
                          'job_title':job_title,
                          'job_function':job_function,
                          'company_name':company_name,
                          'industry':industry,
                          'job_acceptance_date':job_acceptance_date,
                          'Job_at_graduation':Job_at_graduation,
                          'Job_3_months':Job_3_months,
                          'reason_not_seeking_employment':reason_not_seeking_employment,
                          'data_entry_timestamp':data_entry_timestamp})
    st.write(new_row)
    students_job_data_df=pd.concat([students_job_data_df,new_row])
    students_job_data_df=students_job_data_df.reset_index(drop=True)
    students_job_data_df.to_csv('students_job_data_df.csv',index=False)

next_possible_actions=st.selectbox('Select Next Possible Actions',
                                   ['Select an option',
                                    'Check all the data enteries',
                                    'Visualizations'])

if next_possible_actions=='Check all the data enteries':
    st.write(students_job_data_df[students_job_data_df['GWID']==GWID])
elif next_possible_actions=='Visualizations':
    students_job_data_df_distinct=students_job_data_df.copy()

    students_job_data_df_distinct=students_job_data_df_distinct.sort_values(by=['data_entry_timestamp','GWID'],ascending=False)
    
    students_job_data_df_distinct=students_job_data_df_distinct.drop_duplicates(subset='GWID',keep='first')

    students_job_data_df_final=pd.merge(students_df,students_job_data_df_distinct,on='GWID',how='left')

    #st.write('% of students who are employed',
    #         students_job_data_df_final[students_job_data_df_final['job_seeking_status']=='Employed'].shape[0]/students_job_data_df_final.shape[0]*100,'%')
    st.write('Total Students',students_job_data_df_final.shape[0])

    job_seeking_status_counts=students_job_data_df_final['job_seeking_status'].value_counts(dropna=False)
    plt.figure(figsize=(8,8))
    plt.pie(job_seeking_status_counts,labels=job_seeking_status_counts.index,autopct='%1.0f%%',startangle=140)
    plt.title('Distribution of Students by Job Seeking Status')
    st.pyplot(plt)












