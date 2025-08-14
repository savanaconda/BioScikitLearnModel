import pandas as pd
from functools import reduce

# Reads from csv and filters dataframe down to only the desired columns.
def read_and_filter_data(file_name, desired_columns):
    data = pd.read_csv(file_name)
    
    columns_to_drop = data.columns.difference(desired_columns)
    filtered_data = data.drop(columns=columns_to_drop)
    
    return filtered_data
    s
# Generates a list of data frames containing data for each species in list.
def generate_per_species_dfs(list_of_species, data):
    # Initialize data frames list.
    list_of_dfs=[]

    # For each species, create a df with site, year, mean, and se (with columns renamed). Then add to data_frames list.
    for sp in list_of_species:
        species_data_wcc = data[data['Classcode']==sp]
        species_data = species_data_wcc.drop(columns='Classcode')
        species_data.rename(columns={"MeanDens60m": sp + "_M", "Dens_SE": sp + "_SE"}, inplace=True)
        list_of_dfs.append(species_data)

    return list_of_dfs


############### Main Method ###############
# Script that combines Washington only data is combined into format with the means and standard errors of the 
# four algae, four fish, and four invert species with the highest amount of data.
# This is written to a CSV file.

print('Combining data...')

output_file_path = '../datasets/Combined_washington_data.csv'

## Files ##
wa_algae_file = './data/Algae_Washington_Survey_means_2024.csv'
wa_fish_file = './data/Fish_Washington_Survey_means_2024.csv'
wa_invert_file = './data/Invert_Washington_Survey_means_2024-PTA.csv'

desired_columns = ["Site", "Year", "MeanDens60m", "Dens_SE", "Classcode"]

## Aggregate Washington Data ##

# summarize_nonzero_species_counts in data_exploration.py showed that these for the top 4 algae species for which we have the most data
top_wa_algae_species = ['Sugar Kelp', 'Acid Weed', '5-Ribbed Kelp', 'Bull Kelp']

# summarize_nonzero_species_counts in data_exploration.py showed that these for the top 4 fish species for which we have the most data
top_wa_fish_species = ['Striped Perch', 'Buffalo Sculpin', 'Shiner Perch', 'Forage Fish']

# summarize_nonzero_species_counts in data_exploration.py showed that these for the top 4 invertebrate species for which we have the most data
top_wa_invert_species = ['Kelp Crab', 'Rock Crab', 'Mottled Star', 'Large Anemone']


filtered_algae_data = read_and_filter_data(wa_algae_file, desired_columns)
filtered_fish_data = read_and_filter_data(wa_fish_file, desired_columns)
filtered_invert_data = read_and_filter_data(wa_invert_file, desired_columns)

# Create new df with one row for each site and year combo
wa_sites_df = pd.DataFrame(filtered_algae_data['Site'].unique(), columns=['Site'])
wa_years_df = pd.DataFrame(filtered_algae_data['Year'].unique(), columns=['Year'])
new_df = wa_sites_df.merge(wa_years_df, how='cross')

# Initialize data frames list.
list_of_dfs = [new_df]

# For each species, create a df with site, year, mean, and se (with columns renamed). Then add to data_frames list.
algae_sp_dfs = generate_per_species_dfs(top_wa_algae_species, filtered_algae_data)
fish_sp_dfs = generate_per_species_dfs(top_wa_fish_species, filtered_fish_data)
invert_sp_dfs = generate_per_species_dfs(top_wa_invert_species, filtered_invert_data)
list_of_dfs =  list_of_dfs + algae_sp_dfs + fish_sp_dfs + invert_sp_dfs

# Merge all data frames together
result = reduce(lambda  left,right: pd.merge(left,right,how="left", on=['Site','Year']), list_of_dfs)

# Write result to csv
result.to_csv(output_file_path, index=False)
print('Data written to ', output_file_path)