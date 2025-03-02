# Vietnam Jobs Data

## Introduction

Vietnam Jobs Data is a project focused on collecting, processing, and analyzing job market data in Vietnam. The goal is to create a comprehensive dataset that provides valuable insights for job seekers, employers, and researchers interested in labor market trends. The job data is crawled from the following three platforms:

- VietnamWorks

- Joboko

- CareerViet

## Project Structure

The project follows a structured directory format:

```
Vietnam_Jobs_Data/
├── config/            # Configuration files
├── data/              # Storage for collected and processed data
├── etl/               # Extract, Transform, Load (ETL) scripts
├── pipelines/         # Data processing pipelines
├── src/               # Source code for different modules
├── main.py             # Main script to execute the project
├── merge.ipynb         # Jupyter Notebook for merging and inspecting data
├── requirements.txt    # List of required dependencies
```

## Installation

To install and run this project, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/HoangHai0810/vietnam_jobs_data.git
cd vietnam_jobs_data
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Run the crawler

You can run crawler files in folder `pipelines`

### Merge data

Open and run the `merge.ipynb` notebook to merge and inspect data.

### Running DBT Pipelines

To run the DBT (Data Build Tool) pipelines for data transformation, follow these steps:

#### Navigate to the pipelines/dbt/ directory:
```bash
cd pipelines/dbt
```
#### Initialize the DBT project:
```bash
dbt init
```
Run DBT models:
```bash
dbt run
```
## Contact

The project is developed by a team of four members:

1. Trung Nguyen-Phu - **Github**: https://github.com/boo283
2. Thi Nguyen-Chi - **Github**: https://github.com/nchiht
3. Anh Hoang-Hai - **Github**: https://github.com/HoangHai0810
4. Duc Bui-Le-Trong - **Github**: https://github.com/builetrongduc

