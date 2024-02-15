## Bus Timings App


The major hurdle of this project was extracting, cleaning and converting the data to a desirable file format. The source data was in the form of a pdf file with each of its page containing a few lines of details of the bus followed by a timetable of its trips and bus routes in tabular form. Each table contained a 'Trip','Day' headers as well as place columns through which the bus passed. Each place column further contained three sub-header: 'A'(arrival timing), 'D'(departure timing), and 'Via'(places through which the bus may pass occasionally). The PDF file is 'RMS-EKM-to upload.pdf' and is located in the 'json_file' directory. 

<p align='center'>
  <img src="https://github.com/jithinraj747/Bus-Timings-App/assets/106642456/33d71582-4296-45cb-9759-068fd542b3a6" width=400>
</p> <br>

<p align='center'>
  <img src="https://github.com/jithinraj747/Bus-Timings-App/assets/106642456/de4db834-a5d6-4127-bb12-87931d52a5e5" width=400>
</p> <br><br>

Below is the extracted and cleaned dataframe form of the PDF table from just the first page of the PDF file. 
<p align='center'>
  <img src="https://github.com/jithinraj747/Bus-Timings-App/assets/106642456/7ae43a1b-7c9c-4db2-ae71-b957c71e1097" width=400>
</p> <br><br>

The tabula-py package was used to read, extract, and convert the tables into dataframe form. Since the extracted data contained a lot of noise, and the columns and rows were disorganized, Pandas was used to clean, crop, and fine-tune the dataframes. Finally, the dataframes were merged and converted into JSON format called 'time_tables.json' which would make it easier and faster to read and make queries when testing the application. A list of the names of the places were also separately converted into a JSON file called ''places.json. All files of extraction and conversion to JSON file is located in the 'json_file' directory.

In order to check the functionality of the newly created JSON file, simple python coding was used for querying and streamlit for test-deploying. The user would input details of boarding point and destination which would then filter those dictionaries in JSON file containing these two places. Pandas would then be used to once again convert the filtered data back to dataframes and merge them to create a single dataframe that would attribute to the user's input. 

