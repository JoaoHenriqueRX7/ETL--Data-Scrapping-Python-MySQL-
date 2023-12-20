# Student Performance Analysis and Admission Automation

## Introduction
This repository hosts a comprehensive Python application designed to streamline the process of analyzing student performance and automating the generation of admission letters. Utilizing a robust ETL pipeline, the application processes student examination data, assesses eligibility based on predefined criteria, and produces personalized admission letters for successful candidates. The results are neatly compiled into a formatted Excel workbook, complete with hyperlinks for easy navigation.

## Features
- **Data Extraction and Loading:** Integrates with Kaggle to download a dataset containing student performance metrics.
- **Data Transformation:** Implements Python's powerful pandas library to clean and transform the data, ensuring it meets the necessary standards for processing.
- **Performance Assessment:** Evaluates student scores against set benchmarks to determine eligibility for admission.
- **Automated Letter Generation:** Utilizes docxtpl to create personalized admission letters for each successful student, storing them in a designated directory.
- **Excel Dashboard Creation:** Leverages openpyxl to craft a styled Excel dashboard that provides a user-friendly interface to view student performance and access individual admission letters.

## How to Use
1. Clone the repository to your local machine.
2. Ensure you have the necessary Python libraries installed (pandas, openpyxl, faker, and docxtpl).
   ```sh
   pip install pandas openpyxl faker seaborn docxtpl
   ```
   
## Project root
```sh
│
├── download/                    # Directory where the dataset is downloaded
├── extracted_files/             # Directory where the dataset is extracted
├── admitted_students/           # Output directory for admission letters
├── admission_lists/             # Output directory for the Excel dashboard
├── project_assets/              # Directory for project assets like templates
│   ├── kaggle.json              # Kaggle API credentials
│   └── admission_template.docx  # Template for admission letters
└── main.py                      # Main script to run the project
```

## Requirements:
- Python 3.x
- MySQL 8.x

## License

The source code is available under the MIT license. See LICENSE for more information.

## Acknowledgments

This project was inspired by various resources and similar projects in the field of data science. Special thanks to all contributors and the open-source community.

© Copyright 2023 João Henrique. All rights reserved.
