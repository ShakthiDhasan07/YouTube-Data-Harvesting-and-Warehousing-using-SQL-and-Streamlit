# YouTube Data Harvesting and Warehousing using SQL and Streamlit

## Overview:
This project is designed to extract data from YouTube channels using the YouTube API, process it, and store it for further analysis. The collected data is initially stored as documents in a MongoDB Atlas database and later transformed into SQL records for comprehensive data analysis. The core functionality of the project follows the Extract, Transform, Load (ETL) process. Key features of the project include:

---

## Approach:

- **Harvest YouTube Channel Data**: Extract YouTube channel data by providing a 'Channel ID' and store the data in MongoDB Atlas as documents.
  
- **Convert MongoDB Data into SQL**: Transform MongoDB data into SQL records for further data analysis.
  
- **Streamlit Integration**: Implement Streamlit to present the code and data in a user-friendly UI.
  
- **Data Analysis**: Perform data analysis using SQL queries and Python integration.

---

## Tools Used:

- **Python** (Scripting)
- **MongoDB**
- **MySQL**
- **API Integration**

---

## Methods:

### Step 1: Install/Import Modules
Install and import the necessary modules:
- Streamlit
- Pandas
- PyMongo
- Googleapiclient.discovery
- mysql.connector

### Step 2: Methods

- **Get YouTube Channel Data**: Fetches YouTube channel data using a Channel ID.
  
- **Get Playlist Videos**: Retrieves all video IDs for a provided playlist ID.
  
- **Get Video and Comment Details**: Returns video and comment details for the given video IDs.
  
- **Insert Data into MongoDB**: Inserts channel data into MongoDB Atlas as a document.
  
- **Convert MongoDB Document to Dataframe**: Fetches MongoDB documents and converts them into dataframes for SQL data insertion.
  
- **Data Analysis**: Conducts data analysis using SQL queries and Python integration.

### Step 3: Run the Project with Streamlit

To run the `YtAPiproject.py` using a virtual environment, follow these steps:

1. Open the command prompt in the project directory.
  
2. Create a virtual environment using `python -m venv venv` and activate it:
   - For Windows: `.\venv\Scripts\activate`
   - For macOS/Linux: `source venv/bin/activate`
  
3. Install the required libraries using:
   - `pip install -r requirements.txt` or manually:
     - `pip install streamlit google-api-python-client pymongo mysql-connector-python pandas`
  
4. Run the app with:
   - `streamlit run python.py` to open the UI in a web browser.
  
5. When done, deactivate the environment using:
   - `deactivate`

---

## Result:

This project focuses on harvesting YouTube data using the YouTube API, storing it in MongoDB, and converting it into SQL format for analysis. It integrates Streamlit, Python, and various ETL techniques. The project highlights expertise in Python, MongoDB, SQL, API integration, and data management tools. It effectively reduces manual data processing and storage by automating the entire process.
