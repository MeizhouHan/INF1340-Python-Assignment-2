from typing import TextIO, List, Union, Dict, Tuple
from sentiment import *
from operator import itemgetter

def occur_cutoff_kss(min_occ, kss) -> Dict[str, List[int]]:
    '''Return a dictionary containing all the words
    that occur at least min_occ times in kss.
    Each key in the dictionary is word and the value is formatted as follows:
    {word:[aggregate score, number of occurrences]}
    
    [examples not required]
    min_occ: at least how many times each word should have occurred in the dataset
    kss: the full dataset dictionary
    '''
    new_dic={}
    for item in kss:
        if kss.get(item)[1] >= min_occ:
            new_dic[item] = [kss.get(item)[0], kss.get(item)[1]]

    return new_dic


def get_error_list(a_file:TextIO):
    '''return a list of lists that contains number of minimum occurences and its 
    corresponding error.
    sum_error= predicted score-actual score
    '''
    error_list=[]
    
    with open('medium.txt','r') as dic_file:
        file_list=dic_file.readlines() 
    print(file_list[1]) #just to see if readlines works well
    for min_occ in range(15):
        sum_error= 0 
        for line in file_list:
            pss=statement_pss(line, occur_cutoff_kss(min_occ, extract_kss(a_file)))  
            
            if pss is not None:
                sum_error = sum_error + abs(pss-float(line[0]))
                print(sum_error)
                print(pss)
                
             
            else:
                sum_error=sum_error
                #error=|predicted value - actual value| 
                #print(sum_error)
                #print(type(pss))  try to debug
        error_list.append([min_occ,sum_error])
                
            
    return error_list
            
def min_error_occ(error_List:list) -> int:
    '''
    return the min_occ with the least corresponding aggregate error. 
    '''
    error_list=get_error_list(a_file)
    sorted_list=sorted(error_list, key=itemgetter[1])
    
    return sorted_list[0]
    


# Your exploration functions here
# Follow FDR

if __name__ == "__main__":

    # Pick a dataset 
    
    #dataset = 'tiny.txt'
    #dataset = 'small.txt'
    dataset = 'medium.txt'
    #dataset = 'full.txt'
    
        
    # Your exploration testing code here
    with open(dataset, 'r') as a_file:
        print(get_error_list(a_file))  
    #with open(dataset, 'r') as a_file:
        #print(min_error_occ(get_error_list(a_file)))
    pass


