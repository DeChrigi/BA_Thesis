# BA_Thesis
Bachelor Thesis Repository
This repository contains the complete analysis process of a bachelor thesis dealing with the investigation of company networks and their ownership structures. Using Python and Jupyter Notebooks, various data sources are transformed, networks are modelled, visualized and analyzed.

01_transform_and_cleanse.ipynb
Transformation and cleaning of raw data for further analysis.

02_cartel_network.ipynb
Creation of a network between companies and  cartels.

03_shareholder_networks.ipynb
Creation of networks and calculation of measures between companies and their shareholders.

04_connected_shareholder_network.ipynb
Creation of networks and calculation of measures in which the shareholder files are connected into one graph with all companies that have shareholder files.

05_connected_cartel_network.ipynb
Merge between the measures (Herfindal Index) and shareholder measures calculated in 03 and the cartel file described in 02.

90_identify_missing_investor_identities.ipynb
Detection of missing or incomplete data on investors.

91_identify_cartels_with_most_files.ipynb
Analysis on which cartels have the most shareholder files (e.g., greathern than 80% coverage)

92_reduced_company_centrality_metrics.ipynb
Analysis of the reduced cartel networks (One graph for each cartel) for the cartels which have greater than 80% coverage.

linear_regression.ipynb
Statistical analysis using linear regression to investigate correlations between network metrics and company characteristics. (Proof of Concept)

qantas_network.ipynb
Initial analysis of a company and their shareholders.
