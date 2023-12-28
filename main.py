import pandas as pd
import numpy as np
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
    try:
        return df[df['School Name'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing school names')

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

def incident_numbers_reported(df):
    # conversion of non-numeric values to NaN and then filtering rows based on those values
    numeric_mask = pd.to_numeric(df['# of Discipline Incidents'],
                                 errors='coerce').notna()
    if numeric_mask is None:
        raise ValueError
    return df[numeric_mask]

incident_numbers_df = incident_numbers_reported(discipline_condensed_df)

incident_numbers_df.to_excel('incident_numbers_reported.xlsx', index=False)

# pivot table - total student incident numbers of each city
total_incident_num_per_city_df = pd.pivot_table(incident_numbers_df,
                                                values='# of Discipline Incidents',
                                                columns='City',
                                                aggfunc='sum'
                                                )
total_incident_num_per_city_df.to_excel('sum_of_incidents_per_city_pivot_table.xlsx',
                                        index=False)

# pivot table - total student incident numbers per school type
total_incident_num_per_city_df = pd.pivot_table(incident_numbers_df,
                                                values='# of Discipline Incidents',
                                                columns='School Type',
                                                aggfunc='sum'
                                                )
total_incident_num_per_city_df.to_excel('sum_of_incidents_per_school_type_pivot_table.xlsx', index=False)


# highlight the lowest number of incidents
def highlight_min(data, color='#1dd7f3'):
    '''
    highlight the maximum in a Series or DataFrame
    '''
    attr = 'background-color: {}'.format(color)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_min = data == data.min()
        return [attr if v else '' for v in is_min]
    else:  # from .apply(axis=None)
        is_min = data == data.min().min()
        return pd.DataFrame(np.where(is_min, attr, ''),
                            index=data.index, columns=data.columns)

incident_numbers_df = incident_numbers_df.style.apply(highlight_min, subset=['# of Discipline Incidents'])

incident_numbers_df.to_excel('incident_numbers_reported.xlsx', index=False)

# SAT Math Average Score (High Schools only and eventually calculate its averages of each county)
sat_condensed_df = pd.DataFrame()
rcdts = sat_df.iloc[:,0]
sat_condensed_df['RCDTS'] = rcdts.copy()
school_name = sat_df.iloc[:,2]
sat_condensed_df['School Name'] = school_name.copy() # school name
city = sat_df.iloc[:,4]
sat_condensed_df['City'] = city.copy()
county = sat_df.iloc[:,5]
sat_condensed_df['County'] = county.copy()
school_type = sat_df.iloc[:,8]
sat_condensed_df['School Type'] = school_type.copy() # school type
sat_reading_average_score = sat_df.iloc[:,10]
sat_condensed_df['SAT Reading Average Score'] = sat_reading_average_score.copy()
sat_math_average_score = sat_df.iloc[:,11]
sat_condensed_df['SAT Math Average Score'] = sat_math_average_score.copy()

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)

# filter data to only high schools
sat_condensed_df = sat_condensed_df.loc[(sat_condensed_df['School Type'] == 'HIGH SCHOOL')]

# delete empty rows
def empty_grade_value(df): # removes rows that have at least 1 average score null
    try:
        return df[df['SAT Reading Average Score'].notna() | df['SAT Math Average Score'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing SAT Reading Average Score or SAT Math Average Score values')

sat_condensed_df = empty_grade_value(sat_condensed_df)

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)

# create new columns -> Total Score, Average Score (Total Score / 1600), and Percentage
sat_condensed_df['Total SAT Score'] = sat_condensed_df['SAT Reading Average Score'] + \
                                            sat_condensed_df['SAT Math Average Score']
sat_condensed_df['SAT Score Percentage'] = sat_condensed_df['Total SAT Score'] / 1600
sat_condensed_df['SAT Score Percentage'] = sat_condensed_df['SAT Score Percentage']\
                                               .astype(str)\
                                               .str[2:4]\
                                               + '%'

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)
#sat_condensed_df.to_csv('sat_condensed.csv', index=False)

sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '9%', 'SAT Score Percentage'] = '90%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '8%', 'SAT Score Percentage'] = '80%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '7%', 'SAT Score Percentage'] = '70%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '6%', 'SAT Score Percentage'] = '60%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '5%', 'SAT Score Percentage'] = '50%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '4%', 'SAT Score Percentage'] = '40%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '3%', 'SAT Score Percentage'] = '30%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '2%', 'SAT Score Percentage'] = '20%'
sat_condensed_df.loc[sat_condensed_df['SAT Score Percentage'] == '1%', 'SAT Score Percentage'] = '10%'

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)

# highlight the highest Total SAT Score value
def highlight_max(data, color='green'):
    '''
    highlight the maximum in a Series or DataFrame
    '''
    attr = 'background-color: {}'.format(color)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_max = data == data.max()
        return [attr if v else '' for v in is_max]
    else:  # from .apply(axis=None)
        is_max = data == data.max().max()
        return pd.DataFrame(np.where(is_max, attr, ''),
                            index=data.index, columns=data.columns)

sat_condensed_df = sat_condensed_df.style.apply(highlight_max, subset=['Total SAT Score'])

sat_condensed_df.to_excel('sat_condensed.xlsx', index=False)

# isa proficiency
isa_condensed_df = pd.DataFrame()
rcdts = isa_df.iloc[:,0]
isa_condensed_df['RCDTS'] = rcdts.copy()
school_name = isa_df.iloc[:,2]
isa_condensed_df['School Name'] = school_name.copy() # school name
city = isa_df.iloc[:,4]
isa_condensed_df['City'] = city.copy()
county = isa_df.iloc[:,5]
isa_condensed_df['County'] = county.copy()
district_size = isa_df.iloc[:,7]
isa_condensed_df['District Size'] = district_size.copy()
school_type = isa_df.iloc[:,8]
isa_condensed_df['School Type'] = school_type.copy()
isa_proficiency_total_student = isa_df.iloc[:,10]
isa_condensed_df['# ISA Proficiency Total Student'] = isa_proficiency_total_student.copy()
isa_proficiency_male = isa_df.iloc[:,11]
isa_condensed_df['# ISA Proficiency - Male'] = isa_proficiency_male.copy()
isa_proficiency_female = isa_df.iloc[:,12]
isa_condensed_df['# ISA Proficiency - Female'] = isa_proficiency_female.copy()
isa_proficiency_white = isa_df.iloc[:,13]
isa_condensed_df['# ISA Proficiency - White'] = isa_proficiency_white.copy()
isa_proficiency_black_or_african_american = isa_df.iloc[:,14]
isa_condensed_df['# ISA Proficiency - Black or African American'] = \
    isa_proficiency_black_or_african_american.copy()
isa_proficiency_hispanic_or_latino = isa_df.iloc[:,15]
isa_condensed_df['# ISA Proficiency - Hispanic or Latino'] = \
    isa_proficiency_hispanic_or_latino.copy()
isa_proficiency_asian = isa_df.iloc[:,16]
isa_condensed_df['# ISA Proficiency - Asian'] = isa_proficiency_asian.copy()
isa_proficiency_native_hawaiian_or_other_pacific_islander = isa_df.iloc[:,17]
isa_condensed_df['# ISA Proficiency - Native Hawaiian or Other Pacific Islander'] = \
    isa_proficiency_native_hawaiian_or_other_pacific_islander.copy()
isa_proficiency_american_indian_or_alaska_native = isa_df.iloc[:,18]
isa_condensed_df['# ISA Proficiency - American Indian or Alaska Native'] = \
    isa_proficiency_american_indian_or_alaska_native.copy()
isa_proficiency_two_or_more_races = isa_df.iloc[:,19]
isa_condensed_df['# ISA Proficiency - Two or More Races'] = isa_proficiency_two_or_more_races.copy()
isa_proficiency_children_with_disabilities = isa_df.iloc[:,20]
isa_condensed_df['# ISA Proficiency - Children with Disabilities'] = \
    isa_proficiency_children_with_disabilities.copy()

isa_condensed_df.to_excel('isa_condensed.xlsx', index=False)

# if school name AND proficiency values are blank for each column, REMOVE row
def grab_gender_data(df): # find all the non-missing values ONLY
    try:
        return df[df['School Name'].notna() &
                  df['# ISA Proficiency Total Student'].notna() &
                  df['# ISA Proficiency - Male'].notna() &
                  df['# ISA Proficiency - Female'].notna() &
                  df['# ISA Proficiency - White'].notna()]
    except Exception as e:
        print(f'caught {type(e)}: e \n '
              f'Cannot delete rows with missing school names')

# delete rows with empty cell under EVERY proficiency column
isa_condensed_df = grab_gender_data(isa_condensed_df)

# create updated version of isa condensed gender (male/female) data
isa_condensed_df.to_excel('isa_condensed_gender_data.xlsx', index=False)