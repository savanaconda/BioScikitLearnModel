import pandas as pd

# Reads from csv and filters dataframe down to only the desired columns.
def read_and_filter_data(file_name, desired_columns):
    data = pd.read_csv(file_name)
    
    columns_to_drop = data.columns.difference(desired_columns)
    filtered_data = data.drop(columns=columns_to_drop)
    
    return filtered_data

# Summarizes how many data points there are for each species (includes only non-zero counts).
def summarize_nonzero_species_counts(file_name, data):
    nonzero = data[data["MeanDens60m"] != 0.0]
    value_counts = nonzero["Classcode"].value_counts()
    
    print(file_name)
    print(value_counts)
    print(f'\n\n')
    return


############### Main Method ###############
#
# Explores the algae, fish, and invertebrate data from California, Oregon and Washington.
#

## Files ##
# Algae
ca_algae_file = './data/Algae_California_Survey_means_2024.csv'
or_algae_file = './data/Algae_Oregon_Survey_means_2024.csv'
wa_algae_file = './data/Algae_Washington_Survey_means_2024.csv'

# Fish
ca_fish_file = './data/Fish_California_Survey_means_2024.csv'
or_fish_file = './data/Fish_Oregon_Survey_means_2024.csv'
wa_fish_file = './data/Fish_Washington_Survey_means_2024.csv'

# Invertebrates
ca_invert_file = './data/Invert_California_Survey_means_2024.csv'
or_invert_file = './data/Invert_Oregon_Survey_means_2024.csv'
wa_invert_file = './data/Invert_Washington_Survey_means_2024-PTA.csv'

algae_files = [ca_algae_file, or_algae_file, wa_algae_file]
fish_files = [ca_fish_file, or_fish_file, wa_fish_file]
invert_files = [ca_invert_file, or_invert_file, wa_invert_file]

## Desired Columns ##
desired_algae_columns = ["Site", "Year", "MeanDens60m", "Dens_SE", "Classcode"]
desired_fish_columns = desired_algae_columns
desired_invert_columns = desired_algae_columns


## Summarize data for all files ##
run_algae = True
run_fish = True
run_invert = True

if run_algae:
    for file in algae_files:
        filtered_data = read_and_filter_data(file, desired_algae_columns)
        summarize_nonzero_species_counts(file, filtered_data)

if run_fish:
    for file in fish_files:
        filtered_data = read_and_filter_data(file, desired_fish_columns)
        summarize_nonzero_species_counts(file, filtered_data)

if run_invert:
    for file in invert_files:
        filtered_data = read_and_filter_data(file, desired_invert_columns)
        summarize_nonzero_species_counts(file, filtered_data)