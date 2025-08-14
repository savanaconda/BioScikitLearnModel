import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as selector
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 1. Import and set up data
print("1. Importing and set up data...")
# Data set from https://github.com/INRIA/scikit-learn-mooc/blob/main/datasets/ames_housing_no_missing.csv
ames_housing = pd.read_csv("./datasets/ames_housing_no_missing.csv")

parser = argparse.ArgumentParser(description="Parser to determine whether or not to generate plot.")
parser.add_argument("--plot", action="store_true", help="Generates plot to visualize data.")
args = parser.parse_args()

target_name = "SalePrice"
data, target = ames_housing.drop(columns=target_name), ames_housing[target_name]
target = (target > 200_000).astype(int)

numerical_features = [
  "LotFrontage", "LotArea", "MasVnrArea", "BsmtFinSF1", "BsmtFinSF2",
  "BsmtUnfSF", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "LowQualFinSF",
  "GrLivArea", "BedroomAbvGr", "KitchenAbvGr", "TotRmsAbvGrd", "Fireplaces",
  "GarageCars", "GarageArea", "WoodDeckSF", "OpenPorchSF", "EnclosedPorch",
  "3SsnPorch", "ScreenPorch", "PoolArea", "MiscVal",
]
categorical_features = data.columns.drop(numerical_features)
data_numerical = data[numerical_features]
data_categorical = data.drop(columns=numerical_features)

# 2. Visual data exploration
if args.plot:
    print("2. Visualizing data exploration...")
    initial_analysis = sns.pairplot(
        data=ames_housing,
        vars = numerical_features[:3],
        hue = target_name,
        palette="Spectral",
        plot_kws={"alpha": 0.9},
        height=3,
        diag_kind="hist",
        diag_kws={"bins": 30},
    )
    plt.show()
    print(f"Numerical data:\n", data_numerical.describe())
    print(f"Categorical data:\n", data_categorical.describe())
else:
    print("2. Skipping plotting... (to plot, add '--plot' arg)")

# 3. Preprocessing
print("3. Preprocessing...")
categorical_preprocessor = OneHotEncoder(handle_unknown="ignore")
numerical_preprocessor = StandardScaler()
preprocessor = ColumnTransformer(
    [
        ("one-hot-encoder", categorical_preprocessor, categorical_features),
        ("standard_scaler", numerical_preprocessor, numerical_features),
    ]
)

# 4. Set up model and run pipeline
print("4. Setting up model and running pipeline...")
predictive = LogisticRegression(max_iter=500)
model = make_pipeline(preprocessor, predictive)

# 5. Cross validate and process results
print("5. Cross validating and processing results...")
start = time.time()
cv_iterations = 10
# Cross validation breaks up training and testing data
cv = cross_validate(model, data, target, cv=cv_iterations)
elapsed_time = time.time() - start
scores = cv["test_score"]


model_name = model.__class__.__name__
print(f"\n\nModel used was {model_name} with {cv_iterations} cross validation iterations "
      f"and a fitting time of {elapsed_time:.3f} seconds\n\n"
      +
      f"Target predictor was {target_name} and used {len(numerical_features)} numerical features and {len(categorical_features)} categorial features.\n\n"
      +
      f"Accuracy was {scores.mean():.3f} +/- {scores.std():.3f}")


# --------------For later--------------
# - Plot accuracy over cross-validation iterations to compare performance of two different models
# - Experiment with test train ratio
