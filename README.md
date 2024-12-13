# YouTube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit

# Overview:
  This project is designed to extract data from YouTube channels using the YouTube API, process it, and store it for further analysis. The collected data is initially stored as documents in a MongoDB Atlas database and later transformed into SQL records for comprehensive data analysis. The core functionality of the project follows the Extract, Transform, Load (ETL) process. Features include:

# Approach:

  - Harvest YouTube channel data using the YouTube API by providing a 'Channel ID' and Store channel data in MongoDB Atlas as documents
  -  Convert MongoDB data into SQL records for data analysis
  -  Implement Streamlit to present code and data in a user-friendly UI and Execute data analysis using SQL queries and Python integration.
  -  
# Tools Used 

   - Python (Scripting)
     
   - MongoDB
     
   - MySQL
     
   - API Integration
# Methods
Step 1: Install/Import Modules
      
      - Install/Import the necessary modules: Streamlit, Pandas, PyMongo, Googleapiclient.discovery, and mysql.connector.

Step 2: Methods

        - Get YouTube Channel Data: Fetches YouTube channel data using a Channel ID
        - Get Playlist Videos: Retrieves all video IDs for a provided playlist ID.
        - Get Video and Comment Details: Returns video and comment details for the given   video IDs.

        - Insert Data into MongoDB: Inserts channel data into MongoDB Atlas as a document.
        - Convert MongoDB Document to Dataframe: Fetches MongoDB documents and converts them into dataframes for SQL data insertion.

        - Data Analysis: Conducts data analysis using SQL queries and Python integration.

Step 3: Run the Project with Streamlit

        To run the YtAPiproject.py using a virtual environment, first, open the command prompt in the project directory. Create a virtual environment using python -m venv venv and activate it with .\venv\Scripts\activate (Windows) or source venv/bin/activate (macOS/Linux). Install the required libraries using pip install -r requirements.txt or manually with pip install streamlit google-api-python-client pymongo mysql-connector-python pandas. Then, run the app with streamlit run python.py to open the UI in a web browser. Finally, deactivate the environment with deactivate when done.

# Result
    This project is designed to harvest YouTube data using the YouTube API, store it in MongoDB, and convert it into SQL format for analysis. It leverages Streamlit, Python, and various ETL techniques. The project showcases expertise in Python, MongoDB, SQL, API integration, and data management tools. 
  -
    
  
