import pandas as pd
from warnings import simplefilter # suppresses warning, allows > 100 columns to be created in new dataframe
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

general_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='General')
finance_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='Finance')
ela_math_science_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx',sheet_name='ELA Math Science')
iar_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='IAR')
iar_2_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='IAR (2)')
sat_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='SAT')
isa_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='ISA')
dlm_aa_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='DLM-AA')
dlm_aa_2_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='DLM-AA (2)')
cte_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='CTE')
teacher_out_to_field_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='TeacherOutofField')
discipline_df = pd.read_excel('23-RC-Pub-Data-Set.xlsx', sheet_name='Discipline')

print(general_df)

# create condensed version of discipline data sheet
discipline_condensed_df = pd.DataFrame()
rcdts = discipline_df.iloc[:,0]
discipline_condensed_df['RCDTS'] = rcdts.copy()
school_name = discipline_df.iloc[:,2]
discipline_condensed_df['School Name'] = school_name.copy() # school name
city = discipline_df.iloc[:,4]
discipline_condensed_df['City'] = city.copy() # city
school_type = discipline_df.iloc[:,8]
discipline_condensed_df['School Type'] = school_type.copy() # school type
number_of_discipline_incidents = discipline_df.iloc[:,11]
discipline_condensed_df['# of Discipline Incidents'] = \
    number_of_discipline_incidents.copy() # school type

# delete empty rows
def delete_row(df): # find all the non-missing values ONLY
    return df[df['School Name'].notna()]

# delete rows with empty cell under School Name
finance_condensed_df = delete_row(discipline_condensed_df)

# discipline condensed excel file xlsx
discipline_condensed_df.to_excel('discipline_condensed.xlsx', index=False)

# sort by alphabetical order
discipline_condensed_df = discipline_condensed_df.sort_values(
    by='School Name', ascending=True
)

discipline_condensed_df.to_excel('discipline_condensed.xlsx', index=False)

# create condensed version of finance data sheet
finance_condensed_df = pd.DataFrame()
rcdts = finance_df.iloc[:,0]
finance_condensed_df['RCDTS'] = rcdts.copy()
school_name = finance_df.iloc[:,2]
finance_condensed_df['School Name'] = school_name.copy() # school name
city = finance_df.iloc[:,4]
finance_condensed_df['City'] = city.copy() # city
school_type = finance_df.iloc[:,8]
finance_condensed_df['School Type'] = school_type.copy() # school type
total_per_pupil_expenditures_subtotal = finance_df.iloc[:,26]
finance_condensed_df['$ Total Per-Pupil Expenditures - Subtotal'] = \
    total_per_pupil_expenditures_subtotal.copy() # school name

# finance condensed file
finance_condensed_df.to_excel('finance_condensed.xlsx', index=False)
# delete rows with emtpy cell under School Name
finance_condensed_df = delete_row(finance_condensed_df)

finance_condensed_df.to_excel('finance_condensed.xlsx', index=False)

# lookup name of school, name of school column, $ Total Per-Pupil Expenditures - Subtotal column, false
discipline_finance_condensed_df = pd.merge(
    discipline_condensed_df,
    finance_condensed_df.iloc[:,4],
    left_index=True,
    right_index=True,
    how='outer'
)

# delete rows with emtpy cell under School Name
discipline_finance_condensed_df = delete_row(discipline_finance_condensed_df)

discipline_finance_condensed_df.to_excel('discipline_finance_condensed.xlsx', index=False)

discipline_finance_condensed_df = discipline_finance_condensed_df.sort_values(
    by='$ Total Per-Pupil Expenditures - Subtotal',
    ascending=True
)

discipline_finance_condensed_df.to_excel('discipline_finance_condensed.xlsx', index=False)

def incident_amounts_provided(df):
    # conversion of non-numeric values to NaN and then filtering rows based on those values
    numeric_mask = pd.to_numeric(df['# of Discipline Incidents'], errors='coerce').notna()
    return df[numeric_mask]

incident_amounts_df = incident_amounts_provided(discipline_condensed_df)

incident_amounts_df.to_excel('incident_amounts_provided.xlsx', index=False)