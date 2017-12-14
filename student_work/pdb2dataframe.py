# This Module Contains functions to help change the pdb output from ibp-ng into a useable pandas dataframe
import numpy as np
import pandas as pd
import re

# finds start and end of data in an array of string
def find_data_startend(filelines,startkey='MODEL',endkey='ENDMDL'):
        # filelines: an array of strings, taken from readlines on a *.pdb file
        # startkey, endkey: key word phrases that indicate the beginning and end of data
        # returns start and end values
        
        
        sk = re.compile(startkey) # regular expression for the start search
        ek = re.compile(endkey) # regular expression for the end search
        
        # start and end of data file
        start = None
        end = None
        
        # find start and end of atom list
        for j in np.arange(len(filelines)):
            
            # check line for start
            if start!=None:
                pass # we found start, so skip step
            elif sk.match(filelines[j]):
                #print('Matches! Index: '+str(j))
                start = j+1
                
            
            # check line for end
            if ek.match(filelines[j]):
                #print('Matches! Index: '+str(j))
                end = j
                break
        
        # if 'start' or 'end' doesn't return a value
        if start==None:
            raise Exception('No model start in file! Filename: '+str(filelines))
        elif end==None:
            raise Exception('No model end in file! Filename: '+str(filelines))
        
        return start,end
            

        
# reads file and returns atom locations as a single vector (x1,y1,z1,x2,y2,...etc.)
def atom_locations(file,columns=[6,7,8], startend='f'):
    # file: name of file to be read
    # columns (optional): columns in file where x,y,z coordinates located
    # startend (optional): indicates beginning and ending lines of data. 'f' finds these automatically.
    # returns: atom locations as a single vector (x1,y1,z1,x2,y2,...etc.)
    
    # Reads file as array of lines then closes the file
    f = open(file,'r')
    filelines = f.readlines()
    f.close()
    
    
    # if start and end not defined, finds start and end of model data
    if startend=='f':
        start,end = find_data_startend(filelines)
    
    # if start and end defined, uses the defined start and end points
    else:
        try: start,end = startend[0],startend[1]
        except: 
            raise ValueError('startend was not a valid array!')
            
        if any([type(start)!=int,type(end)!=int]):
            raise ValueError('startend needs to be an array of integers.')
    
    
    # finds number of atoms in file and creates data vector of correct length
    totalatoms = len(filelines[start:end])
    atom_positions = np.zeros(totalatoms*3) # x,y,z for each atom

    #print('total atoms: '+str(totalatoms)+'; coordinate vector: '+
    #          str(np.shape(atom_positions)))

    # For Loop Extracting Molecule Information for This Model
    for i in np.arange(totalatoms):
        # positions cast as float
        atom_positions[3*i:3*i+3] = np.array([filelines[start:end][i].split()[k] for k in columns],
                                                 dtype=float)
        # Note: the standard column numbers are: 6,7, & 8
        # Note: Will throw an error if columns are not numeric
        
    return atom_positions    
