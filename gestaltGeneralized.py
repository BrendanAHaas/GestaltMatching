import pandas as pd
import numpy as np
import difflib


def load_dataframe(file):
    
    #Read the file into a dataframe
    try: #First try pipe-separated variables
        df=pd.read_csv(file, sep="|", encoding='latin1', low_memory=False) #low_memory suppresses dtype error
        print('Loaded dataframe as pipe-separated variables.')
    except:
        try: #Second try tab-separated variables
            df=pd.read_csv(file, sep="\t", encoding='latin1', low_memory=False)
            print('Loaded dataframe as tab-separated variables.')
        except:
            try: #Third try comma-separated variables
                df=pd.read_csv(file, sep=",", encoding='latin1', low_memory=False)
                print('Loaded dataframe as comma-separated variables.')
            except:
                print('Unable to load file as pipe, tab, or comma-separated.')
    
    return(df)

def gestalt(file1, file2, file1col, file2col, file1matchingcol = None, 
            file2matchingcol = None, appendcols = None, matchthreshold = 0.001,
            verbose = False):
    #file1:  Data with names to correct
    #file2:  Reference dataframe
    #file1col:  Column name in file1 with strings to be corrected/matched
    #file2col:  Column name in file2 with strings to be corrected/matched
    #file1matchingcol:  Column name for column in file1 that has to match file2matchingcol
    #file2matchingcol:  Column name for column in file2 that has to match file1matchingcol
    #appendcols:  List of columns to append to file1 from file2 
    #matchthreshold:  Minimium matching score for a match to be found.  Values range from 0.0 to 1.0
    # default value is set very small (0.001) to ensure matches are always found, by default
    #verbose:  Determines whether print statements in code will be used.  False by default.
    
    
    ###LOAD DATAFRAMES AND REMOVE ROWS MISSING NECESSARY INFORMATION###
    #Load dataframes
    df1 = load_dataframe(file1)
    df2 = load_dataframe(file2)
    newdf = df1 #Copy of df1 for later
    
    #Remove NAN entries from reference columns 
    df2 = df2.dropna(subset=[file2col])
    if file2matchingcol != None:
        df2 = df2.dropna(subset=[file2matchingcol])
        
        
        
    if file1matchingcol != None and file2matchingcol != None:  #If two columns are needed to match
        #Get all possible entries with their values in needed matchcol
        names = df1[file1col].tolist() #Convert column to list
        names = [str(i) for i in names] #Convert entries to strings
        namesmatch = df1[file1matchingcol].tolist()
        namesmatch = [str(i) for i in namesmatch]
        namescombolist = []
        
        #Remove duplicate entries, only get all unique combinations
        for index, entry in enumerate(names):
            namescombolist.append([names[index], namesmatch[index]])
        namescomboset = set(tuple(row) for row in namescombolist)
        #All unique entries now in the following form:
        # namescomboset = {(entry1, matchingcol1), (entry2, matchingcol2), ...}
        if verbose == True:
            print(str(len(namescomboset)) + ' different inputs in first dataframe to replace.')
        
        df1list = []
        df2list = []
        simlist = []
        nomatchlist = []
        nomatchclosestlist = []
        nomatchsimlist = []
        
        for item in namescomboset:
            #Find options by identifying entries with matching values from specified columns
            entry = item[0].rstrip() #Strip whitespace from end of our entry
            df2reduced = df2[df2[file2matchingcol] == item[1]]
            options = df2reduced[file2col].tolist()
            optionsset = set(options)
            
            match = difflib.get_close_matches(entry, optionsset, n=1, cutoff = matchthreshold)
            if match != []: #If a match is found
                df1list.append(item[0])
                df2list.append(match[0])
                simscore = difflib.SequenceMatcher(None, entry, match[0]).ratio()
                #If value is an exact match, set score = 1
                # The scoring system has a length factor, so short strings may have scores
                #  less than 1, even for exact matches
                if entry == match[0]: 
                    simscore = 1
                simlist.append(simscore)
                if verbose == True:
                    print(str(entry) + ':  ' + str(match[0]) + '.  Score: ' + str(simscore))
            else: #If no match above the threshold value
                nomatchlist.append(item[0])
                nomatchclosest = difflib.get_close_matches(entry, optionsset, n=1, cutoff = 0.001)
                if nomatchclosest != []: #If match was found with lower threshold
                    nomatchclosestlist.append(nomatchclosest[0])
                    nomatchclosestscore = difflib.SequenceMatcher(None, entry, nomatchclosest[0]).ratio()
                    nomatchsimlist.append(nomatchclosestscore)
                    if verbose == True:
                        print('No match meeting criteria for:  ' + str(entry) + '.')
                        print('  Closest match and score:  ' + str(nomatchclosest[0]) +', ' + str(nomatchclosestscore))
                else: #If still no match b/c of column-matching restriction
                    nomatchclosestlist.append('')
                    nomatchsimlist.append('0.0')
                    if verbose == True:
                        print('No match meeting criteria for:  ' + str(entry) + '.')
                    
    
    if file1matchingcol == None or file2matchingcol == None: #If not dependent on other cols matching:
        #Identify entries in columns of interest, convert to strings
        names = df1[file1col].tolist() #Convert column to list
        names = [str(i) for i in names] #Convert entries to strings
        namesset = set(names)
        if verbose == True:
            print(str(len(namesset)) + ' different inputs in first dataframe to replace.')

        options = df2[file2col].tolist()
        options = [str(i) for i in options] #Convert entries to strings
        optionsset = set(options)
        if verbose == True:
            print(str(len(optionsset)) + ' different replacement options in second dataframe.')

        df1list = []
        df2list = []
        simlist = []
        nomatchlist = []
        nomatchclosestlist = []
        nomatchsimlist = []

        for item in namesset:
            entry = item.rstrip() #Strip whitespace from end of item
            match = difflib.get_close_matches(entry, optionsset, n=1, cutoff = matchthreshold)
            if match != []:  #If we found a match above the matchthreshold value
                df1list.append(item)
                df2list.append(match[0])
                simscore = difflib.SequenceMatcher(None, entry, match[0]).ratio()
                #If value is an exact match, set score = 1
                # The scoring system has a length factor, so short strings may have scores
                #  less than 1, even for exact matches
                if entry == match[0]:
                    simscore = 1
                simlist.append(simscore)
                if verbose == True:
                    print(str(entry) + ':  ' + str(match[0]) + '.  Score: ' + str(simscore))
            else: #If no match above the threshold value
                nomatchlist.append(item)
                nomatchclosest = difflib.get_close_matches(entry, optionsset, n=1, cutoff = 0.001)
                nomatchclosestlist.append(nomatchclosest[0])
                nomatchclosestscore = difflib.SequenceMatcher(None, entry, nomatchclosest[0]).ratio()
                nomatchsimlist.append(nomatchclosestscore)
                if verbose == True:
                    print('No match above threshold value for:  ' + str(entry) + '.')
                    print('  Closest match and score:  ' + str(nomatchclosest[0]) +', ' + str(nomatchclosestscore))
            
    #Output replacement list as df:
    repdf = pd.DataFrame(list(zip(df1list, df2list, simlist)),
                        columns = ['Input', 'Replacement', 'Similarity Score'])
    repdf.to_csv('C:/Users/Administrator/Documents/GestaltAlgorithm/ReplacementList.csv', sep="|", index=False)

    #Output values with no matches as 1 column df:
    nomatchdf = pd.DataFrame(list(zip(nomatchlist, nomatchclosestlist, nomatchsimlist)),
                             columns = ['Items Without Matches', 'Closest Match', 'Similarity Score'])
    nomatchdf.to_csv('C:/Users/Administrator/Documents/GestaltAlgorithm/NoMatchList.csv', sep="|", index=False)

    #Create new output dataframe using the replacements
    for index, value in enumerate(df1list):
        newdf[file1col] = newdf[file1col].replace(value, df2list[index])

    #Add appendcols to new dataframe if applicable
    if appendcols != None:
        for entry in appendcols: #Create empty columns for these values
            newdf[entry] = np.nan
        for entry in appendcols: #Add in appended columns
            for item in df2list:
                val = df2.loc[df2[file2col] == item, entry].iloc[0]
                newdf.loc[newdf[file1col] == item, entry] = val
                

    #Save new dataframe
    newdf.to_csv('C:/Users/Administrator/Documents/GestaltAlgorithm/UpdatedData.csv', sep="|", index=False)                
        
        
        
#####Run the algorithm

#Define Variables
file1 = 'C:/Users/Administrator/Documents/GestaltAlgorithm/TFMView.csv'
file2 = 'C:/Users/Administrator/Documents/GestaltAlgorithm/GEONAMES_SHEET2.csv'
file1col = 'Last CLM City'
file2col = 'CITY_NAME_TX'
file1matchingcol = 'Last CLM State'
file2matchingcol = 'STATE_CD'
#file1matchingcol=None
#file2matchingcol=None
appendcols = ['LATITUDE_CN', 'LONGITUDE_CN']

#Run function
gestalt(file1=file1, file2=file2, file1col=file1col, file2col=file2col,
       file1matchingcol=file1matchingcol, file2matchingcol=file2matchingcol,
       appendcols=appendcols, matchthreshold = 0.8, verbose = True)