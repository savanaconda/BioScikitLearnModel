# BioScikitLearnModel
Model(s) on bio data utilizing scikit-learn python library. The main file for this work is **bio_model_reefdata.py**

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
I preprocessed the data using OneHotEncoder for categorical feature (Site) and StandardScaler for numerical features (Fish and Invertebrate Mean Densities). This did basic data normalization.



### 4. Imputation (cleaning up NaNs)
 Many of the models I experimented with could not handle missing (NaN) values, which there were a good amount of as some site contained some species and others did not. I used Scikit-learn's SimpleImputter with the "most frequent" strategy. Whether or not this is the ideal strategy would be something to explore further.

### 5. Running the models (with cross validation)

Finally, I actually ran trained and tested the data with cross validation of 10 different model runs. I used the cross_validate method from sklearn.model_selection which handles splitting of training and testing data. I experimented with two different model types: **LogisticRegression** and **RandomForestRegressor**.

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

Also this was a fairly basic analysis. Much more work could be done to explore better model types, tweak model parameters, or make adjustments to data such as useful a different imputation strategy. For me personally, this was a fun exercise to explore scientific data and make my own models as a follow along the MOOC Machine Learning in Python with Scikit-Learn course.

Thank you to MOOC and Reef Check for providing the resources that allowed me to do this project :)


## Additional Notes

The initial upload uses housing data from the MOOC Machine Learning in Python course to establish model structure.
