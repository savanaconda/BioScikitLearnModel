import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import time
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as selector
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


## 1. Import and set up data ##
print("1. Importing and set up data...")

# Set up command line args
parser = argparse.ArgumentParser(description="Parses command line args.")
parser.add_argument("--plot", action="store_true", help="Add this tag to generate a plot.")
parser.add_argument("--kelp", default='All_Kelp',
                    help="Type of kelp to use in plot. Options are: 'Sugar Kelp_M', 'Acid Weed_M', '5-Ribbed Kelp_M', 'Bull Kelp_M', or 'All_Kelp'. + Default is 'All_Kelp'"
                   )
parser.add_argument("--vars", default='all',
                    help="Which vars to pairwise plot. Options are: 'invert' (or 'i'), 'fish' (or 'f'), or 'all'. Default is 'all'"
                   )
parser.add_argument("--model", default='LogisticRegression',
                    help="Which model to use for predictions. Options are: 'LogisticRegression' or 'RandomForestRegressor'"
                   )
args = parser.parse_args()

# Read file
reef_check_data_og = pd.read_csv("./datasets/Combined_washington_data.csv")

# Get only mean columns (filter out standard error columns)
se_columns = list(reef_check_data_og.filter(regex='_SE', axis=1).columns)
reef_check_data = reef_check_data_og.drop(columns=se_columns)

# Add new column that is sum of all 4 types of kelp
kelp_species = ['Sugar Kelp_M', 'Acid Weed_M', '5-Ribbed Kelp_M', 'Bull Kelp_M']
all_kelp = 'All_Kelp'
reef_check_data[all_kelp] = reef_check_data[kelp_species].sum(axis=1)


# Set target info
target_name = args.kelp
data, target = reef_check_data.drop(columns=target_name), reef_check_data[target_name]

# Create a target column with bins created by threshold values
thresh_target_name = target_name + '_threshold'
reef_check_data[thresh_target_name] = pd.cut(target, 
                             bins=[0, target.mean()*0.5, target.mean()*2, target.max()],  # Define thresholds
                             labels=False, # No labels so output type is int (not category)
                             include_lowest=True) 

fish_cols = ['Striped Perch_M', 'Buffalo Sculpin_M', 'Shiner Perch_M', 'Forage Fish_M']
invert_cols = ['Kelp Crab_M', 'Rock Crab_M', 'Mottled Star_M','Large Anemone_M']
numerical_features = fish_cols + invert_cols

vars_to_use = numerical_features
match args.vars:
    case 'fish':
        vars_to_use = fish_cols
    case 'invert':
        vars_to_use = invert_cols
    case 'all':
        vars_to_use = numerical_features

categorical_features = ['Site']
data_numerical = data[numerical_features]
data_categorical = data[categorical_features]


## 2. Generate pairwise plots ##
print("2. Generating pairwise plots...")
if args.plot:
    sns.set_style("darkgrid")
    initial_analysis = sns.pairplot(
        data=reef_check_data,
        vars = vars_to_use,
        hue = thresh_target_name,
        palette="bright",
        plot_kws={"alpha": 0.9},
        height=3,
        diag_kind="hist",
        diag_kws={"bins": 30},
    )
    initial_analysis.fig.suptitle(target_name, y=1.02) # Adjust y for desired vertical position
    plt.show()
    print(f"Numerical data:\n", data_numerical.describe())
    print(f"Categorical data:\n", data_categorical.describe())
else:
    print("2. Skipping plotting... (to plot, add '--plot' arg)")


## 3. Preprocessing ##
print("3. Preprocessing...")
categorical_preprocessor = OneHotEncoder(handle_unknown="ignore")
numerical_preprocessor = StandardScaler()
preprocessor = ColumnTransformer(
    [
        ("one-hot-encoder", categorical_preprocessor, categorical_features),
        ("standard_scaler", numerical_preprocessor, numerical_features),
    ]
)

# Handle NaNs in dataset
imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')

## 4. Set up model and run pipeline ##
print("4. Setting up model and running pipeline...")

# Update target to the numerical or categorical one depending on model type
predictive = LogisticRegression(max_iter=500)
target = reef_check_data[thresh_target_name]

match args.model:
    case 'RandomForestRegressor':
        predictive = RandomForestRegressor()
        # requires numerical target
        target = reef_check_data[target_name]
    case 'LogisticRegression':
        LogisticRegression(max_iter=500)
        # requires categorical target
        target = reef_check_data[thresh_target_name]

model = make_pipeline(preprocessor, imputer, predictive)


## 5. Cross validate and process results ##
print("5. Cross validating and processing results...")
start = time.time()
cv_iterations = 10
# Cross validation breaks up training and testing data
cv = cross_validate(model, data, target, cv=cv_iterations)
elapsed_time = time.time() - start
scores = cv["test_score"]


print(f"\n\nModel used was {args.model} with {cv_iterations} cross validation iterations "
      f"and a fitting time of {elapsed_time:.3f} seconds\n\n"
      +
      f"Target predictor was {target_name} and used {len(numerical_features)} numerical features and {len(categorical_features)} categorial features.\n\n"
      +
      f"Accuracy was {scores.mean():.3f} +/- {scores.std():.3f}")


# --------------For later--------------
# - Plot accuracy over cross-validation iterations to compare performance of two different models
# - Experiment with test train ratio
