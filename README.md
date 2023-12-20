# Car Data ETL (Extract, Transform, Load) Project Using Python

## Introduction

Welcome to the Car Data ETL Project by João Henrique. This project showcases a practical application of Python in an ETL (Extract, Transform, Load) process, focusing on car data. It involves extracting data from various file formats, transforming it for uniformity, and loading it into a MySQL database.

## Project Overview

1. **Data Download and Extraction:**
   - Download a zip file containing car data from a remote server.
   - Extract CSV, JSON, and XML files from the zip file.

2. **Data Extraction:**
   - Use Python's Pandas library to read data from each file format.

3. **Data Transformation:**
   - Perform currency conversion from USD to EUR.

4. **Data Load:**
   - Load the transformed data into a MySQL database.

5. **Query Data:**
   - Execute SQL queries to interact with the database.

## Technical Aspects

- Utilizes Python libraries like `requests`, `pandas`, `xml.etree.ElementTree`, and `mysql.connector`.
- Implements currency conversion using web scraping techniques.
- Provides a comprehensive guide for setting up and running the project.

## Execution Guide

- **Setting Up:**
  - Ensure required Python libraries are installed.
  - Download your Kaggle credentials and replace the placeholder in the code.

- **Running the Code:**
  - The script is divided into functions, each handling a part of the ETL process.
  - Run the entire script to see the ETL process or step through each function individually.

- **Logging:**
  - Logs are written to `log_file.txt`, useful for debugging or tracking.

## Requirements

- Python (version 3.11.3)
- MySQL (version 8.0.34)
- Additional Python libraries: `pandas`, `requests`, `xml.etree.ElementTree`, `mysql.connector`, `glob`, `datetime`, `zipfile`, `json`

## Installation

You can install these libraries using pip:

```sh
pip install requests zipfile36 pandas glob2 mysql-connector-python datetime
```

## License

The source code is available under the MIT license. See LICENSE for more information.

## Acknowledgments

This project was inspired by various resources and similar projects in the field of data science. Special thanks to all contributors and the open-source community.

© Copyright 2023 João Henrique. All rights reserved.
