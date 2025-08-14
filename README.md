# BioScikitLearnModel
Model(s) on bio data utilizing scikit-learn python library.

The main file for this work is **bio_model_reefdata.py**. Main libraries used are matplotlib, pandas, seaborn and sklearn. I used venv for package management, see full package list in Additonal Notes section below.


# BioScikitLearnModel
Model(s) on bio data utilizing scikit-learn python library.

This model uses data on the Kelp Forests in Washington State from [Reef Check Foundation](https://www.reefcheck.org/). This data was collected by volunteer divers and contains the density of species of algae, fish, and invertebrates at various designated sites around Washington state. This data was also collected in California and Oregon, but in this analysis, I chose to focus solely on Washington.

This model predicts the mean density of the 4 most recorded species of kelp in the dataset using the mean densities of the 4 most recorded species of fish, 4 most recorded species of invertebrates, and the site names. The model used this 8 numerical features and 1 categorical feature.

I compared the model results for logistic regression vs random forest regression.

## Project Steps

Here are the 5 main steps I completed to finish this project.

### 1. Data Formatting

The original reef check data had columns for Site, Year, Classcode (species), Mean Density, and Standard Error (SE) of Density. There was one row for the density data on each species. I reformatted the data so that there was one column per species mean and species SE. This allowed me to easily use the fish and invertebrate densities as features in the model.

The original data set also contained densities for 33 different species of algae, 13 different species of fish, and 30 different species of invertebrates. To simplify the problem space, I filtered down to the top 4 species of each type (algae, fish, invertebrates) which the most number of data samples. This also ensured that I didn't try to run analysis on species with too little data.

<p align="center">
  <img src="https://github.com/savanaconda/BioScikitLearnModel/blob/main/images/data-table.png" alt="Data table"/>
  <caption>Reformatted Data Table with One Column Per Species Mean and SE</caption>
</p>

Later within the model file itself, I created an additional All_Kelp column which was a sum of the densities of the 4 different species of kelp. This was used as the target data.


### 2. Pairwise Plots

To visually explore the data, I generated pairwise plots across the numerical features (e.g. four fish species densities and four invertebrate species densities). Plots were color coded by bins of kelp density. The bins were divided by mean/2 and mean*2 ([0, mean/2], [mean/2, mean*2], [mean*2, max]). This was chosen somewhat arbitrarily, but I did play around with the binning and tried other divisions like by median.

This visual analysis did not yield any super obvious patterns but it showed the data was generally reasonable.

<p align="center">
  <img src="https://github.com/savanaconda/BioScikitLearnModel/blob/main/images/pairwiseplots-fish.png" alt="Data table"/>
  <caption>Pairwise plots of mean densities of fish species, color coded by kelp density.</caption>
</p>

<p align="center">
  <img src="https://github.com/savanaconda/BioScikitLearnModel/blob/main/images/pairwiseplots-invert.png" alt="Data table"/>
  <caption>Pairwise plots of mean densities of invertebrate species, color coded by kelp density.</caption>
</p>


### 3. Preprocessing (normalization)
I preprocessed the data using [OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html) for categorical feature (Site) and [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) for numerical features (Fish and Invertebrate Mean Densities). This did basic data normalization.



### 4. Imputation (cleaning up NaNs)
 Many of the models I experimented with could not handle missing (NaN) values, which there were a good amount of as some site contained some species and others did not. I used Scikit-learn's [SimpleImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html) with the "most frequent" strategy. Whether or not this is the ideal strategy would be something to explore further.

### 5. Running the models (with cross validation)

Finally, I actually ran trained and tested the data with cross validation of 10 different model runs. I used the cross_validate method from sklearn.model_selection which handles splitting of training and testing data. I experimented with two different model types: [**LogisticRegression**](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) and [**RandomForestRegressor**](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html).

#### Results

The model performance is shown in these screenshots of the results:

<p align="center">
  <img src="https://github.com/savanaconda/BioScikitLearnModel/blob/main/images/reefdata-model-results_logisticregression.png" alt="Data table"/>
  <caption>Model results for logistic regression.</caption>
</p>

<p align="center">
  <img src="https://github.com/savanaconda/BioScikitLearnModel/blob/main/images/reefdata-model-results_randomforestregression.png" alt="Data table"/>
  <caption>Model results for random forest regressor.</caption>
</p>

The logistic regression was much more accurate at 62.5% accuracy. The random forest regressor was only 26.7% accurate. The logistic regression model took logistic regression 0.202 seconds to run the 10 runs and the random forest regressor took 1.356 seconds. In both dimensions, the performed worse random forest regressor.

It is also important to note that the random forest regressor used a continuous form of the kelp target data and the logistic regression used a discretized version of the data. Data was binned as described above, using mean/2 and mean*2 to divide into 3 bins.

## Discussion

Overall, even with logistic regression having the 62.5% accuracy, this is not the best model. This is perhaps not surprising that that fish and invertebrate densities do not provide a full picture for how dense a kelp forest might become. If I did follow ups to this work, I would explore the literature more and gather additional data to select more impactful features. Some ideas for this might be the ocean temperature, average level of sunlight, or the measures of water nutrient density at the sites.

Also this was a fairly basic analysis. Much more work could be done to explore better model types, tweak model parameters, or make adjustments to data such as useful a different imputation strategy. For me personally, this was a fun exercise to explore scientific data and make my own models as a follow along the [MOOC Machine Learning in Python with Scikit-Learn course](https://www.fun-mooc.fr/en/courses/machine-learning-python-scikit-learn/).

Thank you to MOOC and Reef Check for providing the resources that allowed me to do this project :)


## Additional Notes

The initial upload uses housing data from the MOOC Machine Learning in Python course to establish model structure.

### Full packages list

Package                   Version
------------------------- --------------
anyio                     4.9.0
appnope                   0.1.4
argon2-cffi               25.1.0
argon2-cffi-bindings      21.2.0
arrow                     1.3.0
asttokens                 3.0.0
async-lru                 2.0.5
attrs                     25.3.0
babel                     2.17.0
basemap                   2.0.0
basemap_data              2.0.0
beautifulsoup4            4.13.4
black                     25.1.0
bleach                    6.2.0
certifi                   2025.7.14
cffi                      1.17.1
charset-normalizer        3.4.2
click                     8.2.1
comm                      0.2.2
contourpy                 1.3.2
cycler                    0.12.1
Cython                    3.1.2
debugpy                   1.8.15
decorator                 5.2.1
defusedxml                0.7.1
executing                 2.2.0
fastjsonschema            2.21.1
fonttools                 4.59.0
fqdn                      1.5.1
h11                       0.16.0
httpcore                  1.0.9
httpx                     0.28.1
idna                      3.10
ipykernel                 6.30.0
ipython                   9.4.0
ipython_pygments_lexers   1.1.1
ipywidgets                8.1.7
isoduration               20.11.0
isort                     6.0.1
jedi                      0.19.2
Jinja2                    3.1.6
joblib                    1.5.1
json5                     0.12.0
jsonpointer               3.0.0
jsonschema                4.25.0
jsonschema-specifications 2025.4.1
jupyter                   1.1.1
jupyter_client            8.6.3
jupyter-console           6.6.3
jupyter_core              5.8.1
jupyter-events            0.12.0
jupyter-lsp               2.2.6
jupyter_server            2.16.0
jupyter_server_terminals  0.5.3
jupyterlab                4.4.5
jupyterlab_code_formatter 3.0.2
jupyterlab_pygments       0.3.0
jupyterlab_server         2.27.3
jupyterlab_widgets        3.0.15
kiwisolver                1.4.8
lark                      1.2.2
MarkupSafe                3.0.2
matplotlib                3.10.3
matplotlib-inline         0.1.7
mistune                   3.1.3
mypy_extensions           1.1.0
nbclient                  0.10.2
nbconvert                 7.16.6
nbformat                  5.10.4
nest-asyncio              1.6.0
notebook                  7.4.4
notebook_shim             0.2.4
numpy                     2.3.1
overrides                 7.7.0
packaging                 25.0
pandas                    2.3.1
pandocfilters             1.5.1
parso                     0.8.4
pathspec                  0.12.1
pexpect                   4.9.0
pillow                    11.3.0
pip                       25.2
platformdirs              4.3.8
prometheus_client         0.22.1
prompt_toolkit            3.0.51
psutil                    7.0.0
ptyprocess                0.7.0
pure_eval                 0.2.3
pycparser                 2.22
Pygments                  2.19.2
pyparsing                 3.2.3
pyproj                    3.7.1
pyshp                     2.3.1
python-dateutil           2.9.0.post0
python-json-logger        3.3.0
pytz                      2025.2
PyYAML                    6.0.2
pyzmq                     27.0.0
referencing               0.36.2
requests                  2.32.4
rfc3339-validator         0.1.4
rfc3986-validator         0.1.1
rfc3987-syntax            1.1.0
rpds-py                   0.26.0
scikit-learn              1.7.1
scipy                     1.16.0
seaborn                   0.13.2
Send2Trash                1.8.3
setuptools                80.9.0
six                       1.17.0
sniffio                   1.3.1
soupsieve                 2.7
stack-data                0.6.3
terminado                 0.18.1
threadpoolctl             3.6.0
tinycss2                  1.4.0
tornado                   6.5.1
traitlets                 5.14.3
types-python-dateutil     2.9.0.20250708
typing_extensions         4.14.1
tzdata                    2025.2
uri-template              1.3.0
urllib3                   2.5.0
wcwidth                   0.2.13
webcolors                 24.11.1
webencodings              0.5.1
websocket-client          1.8.0
widgetsnbextension        4.0.14
