import requests
import zipfile
import pandas as pd
import xml.etree.ElementTree as ET 
import glob 
import mysql.connector
from datetime import datetime

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/datasource.zip"

file_name = URL.split('/')[-1]

# Path to the downloaded zip file
zip_file_path = 'datasource.zip'  # The name of the zip file

# Path where you want to extract the files
extraction_path = '.'  # Current directory

log_file = "log_file.txt"
target_file = "car_data.csv"

# Downloading the file
def download():
    response = requests.get(URL)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved as {file_name}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    
    # Unzipping the file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
        print(f"Files extracted to {extraction_path}")

# Connect to database
def connect_database(host,user,password,port):
    
    mydb = mysql.connector.connect(
        
    host=host,
    user=user,
    password=password,
    port=port
    
    )   
    return mydb
    
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process,lines=True)
    return dataframe


def extract_from_xml(file_to_process):
        dataframe = pd.DataFrame(columns=["car_model","year_of_manufacture","price","fuel"])
        tree = ET.parse(file_to_process)
        root = tree.getroot() 
        for car in root:
            car_model = car.find("car_model").text
            year_of_manufacture = int(car.find("year_of_manufacture").text)
            price = float(car.find("price").text)
            fuel = car.find("fuel").text
            dataframe = pd.concat([dataframe, pd.DataFrame([{"car_model":car_model,
                                                            "year_of_manufacture":year_of_manufacture,
                                                            "price":price,
                                                            "fuel":fuel}])], ignore_index=True)
        return dataframe

def extract():
    #Create an empty dataframe with the indexes
    extracted_data = pd.DataFrame(columns=['car_model','year_of_manufacture','price','fuel'])
    
    # process all csv files 
    for csv_file in glob.glob('*.csv'):
        extracted_data = pd.concat([extracted_data,pd.DataFrame(extract_from_csv(csv_file))], ignore_index=True)
        
    # process all json files 
    for json_file in glob.glob('*.json'):
        extracted_data = pd.concat([extracted_data,pd.DataFrame(extract_from_json(json_file))], ignore_index=True)
        
    # process all xml files 
    for xml_file in glob.glob('*.xml'):
        extracted_data = pd.concat([extracted_data,pd.DataFrame(extract_from_xml(xml_file))], ignore_index=True)

    return extracted_data

def get_EUR():

    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {  
        'ids': 'usd',  # Request the price of 1 USD in EUR
        'vs_currencies': 'eur'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        
        # Check if 'usd' is in the response data
        if 'usd' in data:
            USD_to_EUR_rate = data['usd']['eur']  # Access the USD/EUR exchange rate
            return USD_to_EUR_rate
        else:
            print('USD data not found in the API response')
    else:
        print('Failed to retrieve data from the API')


def transform(data):

    USD_to_EUR = get_EUR()
    #round to 2 decimals
    data['price'] = round(data['price'],2)
    
    #transform USD to EUR and round
    data['price_EUR'] = round(data['price']* float(USD_to_EUR),2)
    
    return data
    
def load(target_file,data,mydb):
    #load to a csv file
    data.to_csv(target_file)
    mycursor = mydb.cursor()
    
    # Convert the DataFrame to a structured array
    data_records = data.to_records(index=False)
    
    # Create schema
    mycursor.execute("CREATE SCHEMA IF NOT EXISTS `car`")
    
    mycursor.execute("USE car")
    
    #Create a table car if not exists
    mycursor.execute("""
                     CREATE TABLE IF NOT EXISTS car 
                        (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        car_model VARCHAR(255),
                        year_of_manufacture INT, 
                        price FLOAT,
                        price_EUR FLOAT, 
                        fuel VARCHAR(45)
                        )
                    """)
    #make the DML function
    DML = """INSERT INTO car 
        (car_model, year_of_manufacture, price, price_EUR, fuel)
        VALUES (%s, %s, %s, %s, %s)
        """
    for record in data_records:
        VAL = (record.car_model, record.year_of_manufacture, record.price, record.price_EUR, record.fuel)
        mycursor.execute(DML, VAL)
            
    mydb.commit()
    mydb.close()

def get_cars(mydb):
    # Create a cursor object to interact with the database
    mycursor = mydb.cursor()

    # Execute the SELECT query to retrieve all rows from the 'car' table
    mycursor.execute("SELECT * FROM car")

    # Fetch all the rows from the result set
    data = mycursor.fetchall()

    # Close the cursor and the database connection
    mycursor.close()
    mydb.close()
    dataframe = pd.read_sql_query(data)
    print(dataframe)
    return data
    
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 
        
# Download the data
try:
    download()
    log_progress("Data downloaded successfully")
except Exception as e:
    log_progress(f"Error in download: {e}")

# Connect to the database
try:
    mydb = connect_database('127.0.0.1', 'root', '112104', '6666')
    log_progress("Database connected successfully")
except Exception as e:
    log_progress(f"Error in database connection: {e}")

# Extract data
try:
    extracted_data = extract()
    log_progress("Data extraction completed")
except Exception as e:
    log_progress(f"Error in data extraction: {e}")

# Transform data
try:
    transformed_data = transform(extracted_data)
    log_progress("Data transformation completed")
except Exception as e:
    log_progress(f"Error in data transformation: {e}")

# Load data
try:
    rows_inserted = load(target_file, transformed_data, mydb)
    log_progress(f"Data loaded successfully")
except Exception as e:
    log_progress(f"Error in data loading: {e}")
    
# read data
try:
    get_cars()
    log_progress(f"Data readed successfully")
except Exception as e:
    log_progress(f"Error in data reading: {e}")