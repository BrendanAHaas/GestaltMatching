# GestaltMatching
A Gestalt Matching algorithm for cleaning up dirty data using a reference file.  Based on python's difflib library.


Introduction
Many hand-entered datasets are exceptionally dirty and filled with typos, infrequently-used abbreviations, or other inconsistencies.  When training a machine learning algorithm, it is helpful to have all entries in a column referring to the same object (for instance, the city BALTIMORE) be entered in exactly the same way (rather than BALTMORE, a typo, BLTMRE, an abbreviation, or some other inconsistent spelling).
The Gestalt Matching algorithm aims to use a reference file known to contain correct entries, compare these entries against those in the dirty input dataset, and appropriately update the entries in the dirty dataset to have the correct spellings (BALTMORE AND BLTMRE would be replaced with BALTIMORE).  This will result in an automatically cleansed dataset without erroneous entries, improving our ability to train successful machine learning algorithms with the data we're provided.


Method
Python's difflib library allows us to write a Gestalt Matching algorithm.  This algorithm compares two different strings and gives them a similarity score based on several factors such as characters used, matching lengths of the string, and other factors.  Thus, a string such as BALTMORE will be found to have a high similarity score when compared to the string BALTIMORE.  This can be used to identify matches between strings and update similar strings to the proper spellings found in the reference file.  Each string in the input file 


Algorithm Inputs
Needed Inputs
file1:  The dirty dataframe that we are trying to clean up.
file2:  The clean reference dataframe known to contain correct entries
file1col:  The column name from file1 with strings to be corrected
file2col:  The column name from file2 with the correct strings to be matched to

Optional Inputs
file1matchingcol:  Column name for column in file1 that has to match file2matchingcol.  
file2matchingcol:  Column name for column in file2 that has to match file1matchingcol.
  -As an example for the above columns, you may be trying to correct inproperly entered City Names.  In order to find maching city names, you may want to specify that you can only find matches so long as columns containing the city's State also match.  Thus, BALTMORE would only match with BALTIMORE if the columns denoting the city's states both read MD for Maryland.
appendcols:  List of columns to append to file1 from file2.
  -The reference file may contain additional data that you would like to add to the input dataframe once a match is found.  For example, once we identify BALTMORE should be BALTIMORE, we may also want to append on the reference column's latitude and longitude values to our input dataframe.  These column names can be added to the appendcols argument to ensure that this happens.
matchthreshold:  The minimium matching score for a match to be found.  Values range from 0.0 to 1.0.
  -By default the matching score is set very low (0.001) to ensure a match is always found.  However, this may lead to undesirable matches (for example, the closest match to NAVY PIER in our reference file may be NAVARRE BEACH, a clearly incorrect pairing).  Raising the matchthreshold parameter decreases the probability of matches being found, but also decreases the likely hood of an incorrect match.
verbose:  Determines whether print statements in the code will be used.  False by default.
    
    
Algorithm Outputs
repdf:  A dataframe showing which replacements were made and the similarity score between the input and matching reference value.
nomatchdf:  A dataframe showing which entries in the input file did not have any identified matches (likely due to matchthreshold being set high, or no proper match existing in the reference file) and the entries with the highest similarity scores.
UpdatedData.csv:  A copy of the input dirty dataframe (file1) with the input values being replaced with the identified matches shown in repdf.
