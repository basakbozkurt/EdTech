# 📊 Google Play Store & Apple App Store App Dataset

This repository contains metadata and analysis scripts related to app rankings from **Google Play Store** and **Apple App Store** between 2017 and 2023. The dataset includes information about free and paid apps, their categories, and rankings across 12 different countries.

---
## 📂 Dataset Overview

Below is a description of the datasets used in this project.

### **🟢 Google Play Store Datasets**
| 📄 File Name                           | 🧱 Columns | 📝 Description | ⚙️ Notes |
|----------------------------------|------------|----------------|----------|
| `unique_apps_playstore_free.csv`  | `app_id`, `data`, `earliest_date`, `latest_date` | A list of unique free apps from 2017 to 2023. | Includes 6,711 missing values in the `data` column and one row with all values missing. |
| `unique_apps_playstore_paid.csv`  | `app_id`, `data`, `earliest_date`, `latest_date` | A list of unique paid apps from 2017 to 2023. | |
| `classification_playstore_free.csv`  | _to be added_ | Category labels for free apps in the dataset. | |
| `classification_playstore_paid.csv`  | _to be added_ | Category labels for paid apps in the dataset. | |
| `all_countries_playstore_free.csv`  | _to be added_ | Free app rankings across 12 countries (2017–2023). | |
| `all_countries_playstore_paid.csv`  | _to be added_ | Paid app rankings across 12 countries (2017–2023). | |
| `unique_apps_playstore_free_titles.csv` | `app_id`, `data`, `earliest_date`, `latest_date`, `title` | Cleaned version of free apps dataset with titles extracted from the `data` column. | Title extracted into new column. Based on `unique_apps_playstore_free.csv`. |


### **🔵 Apple App Store Datasets**
| 📄 File Name                           | 📝 Description |
|----------------------------------|--------------|
| `unique_apps_appstore_free.csv`  | A list of unique free apps from 2017 to 2023. |
| `unique_apps_appstore_paid.csv`  | A list of unique paid apps from 2017 to 2023. |
| `all_countries_appstore_free.csv`  | Free app rankings across 12 countries (2017-2023). |
| `all_countries_appstore_paid.csv`  | Paid app rankings across 12 countries (2017-2023). |

---

## 📌 Notes:
- The datasets are stored in the `data/raw/` folder but **are not included in this repository**.
- The analysis scripts and notebooks provided in this repository reference these datasets.


