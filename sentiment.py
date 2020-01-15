from typing import TextIO, List, Union, Dict, Tuple
from operator import itemgetter
# PART I: File I/O, strings, lists

def is_word(token: str) -> bool:
    '''Return True IFF token is an alphabetic word optionally containing
    forward slashes or dashes.
    
    >>> is_word('Amazing')
    True
    >>> is_word('writer/director')
    True
    >>> is_word('true-to-life')
    True
    >>> is_word("'re")
    False
    >>> is_word("1960s")
    False
    '''
    
    for char in token:
        if not (char.isalpha() or char in '-/'):
            return False
    return True


def get_word_list(statement: str) -> List[str]:
    '''Return a list of words contained in statement, converted to lowercase. 
    Use is_word to determine whether each token in statement is a word.
    
    >>> get_word_list('A terrible , 1970s mess of true-crime nonsense from writer/director Shyamalan .')
    ['a', 'terrible', 'mess', 'of', 'true-crime', 'nonsense', 'from', 'writer/director', 'shyamalan']
    '''
    return_list=[ ]
    words=statement.split(' ')
    for word in words:
        word=word.lower()
        if is_word(word):
            return_list.append(word)
    return return_list
#import doctest
#doctest.testmod()

  
    

def judge(score: float) -> str:
    '''Return 'negative' if score is 1.5 or less.
    Return 'positive' if score is 2.5 or more.
    Return 'neutral' otherwise.
    >>> judge(1.3)
    'negative'
    >>> judge('1.8')
    'neutral'
    >>> judge('3.4')
    'positive'
    '''
    if float(score) <= 1.5:
        return 'negative'
    elif float(score)>=2.5:
        return 'positive'
    else:
        return 'neutral'
    



def word_kss_scan(word: str, file: TextIO) -> Union[None, float]:
    '''Given file composed of rated movie reviews, return the average score
    of all occurrences of word in file. If word does not occur in file, return None.
    [examples not required]
    '''
    num1=0
    total=0
    new=file.readlines()
    for item in new:
        statement=get_word_list(item.rstrip('\n'))
        if word in statement:
            num=statement.count(word)
            num1+=statement.count(word)
            total+=num*float(item[0])
                   
    if num1!=0:
        return total/num1  
    else:
        return None
    



# PART II: Dictionaries 

def extract_kss(file: TextIO) -> Dict[str, List[int]]:
    '''Given file composed of rated movie reviews, return a dictionary
    containing all words in file as keys. For each key, store a list
    containing the total sum of review scores and the number of times
    the key has occurred as a value, e.g., { 'a' : [12, 4] }
    [examples not required]
    
    
    '''
    kss_dic={}
    for line in file:
        tokenlist=line.lower().strip().split(' ')
        for token in tokenlist:
            if is_word(token):
                if token in kss_dic:
                    kss_dic[token][0]+= int(line[0])
                    kss_dic[token][1]+=1
                else:
                    kss_dic[token]=[int(line[0]),1]
        
    return kss_dic

    
def word_kss(word: str, kss: Dict[str, List[int]]) -> Union[float, None]:
    '''Return the Known Sentiment Score of word if it appears in kss. 
    If word does not appear in kss, return None.
    [examples not required]
    '''    
    
    if word in kss:
        return kss.get(word)[0] / kss.get(word)[1]
    else:
        return None





             
             
def statement_pss(statement: str, kss: Dict[str, List[int]]) -> Union[float, None]:
    '''Return the Predicted Sentiment Score of statement based on
    word Known Sentiment Scores from kss.
    Return None if statement contains no words from kss.'''
    
    count=0
    total=0
    for word in get_word_list(statement):
        if word in kss:
            count+=1
            total+=kss.get(word)[0]/kss.get(word)[1]
    if count!=0:
        return total/count
    else:
        return None




# PART III: Word Frequencies

def score(item: Tuple[str, List[int]]) -> float:
    '''Given item as a (key, value) tuple, return the
    ratio of the first and second integer in value
    >>>score(('film',[45,20]))
    2.25
    '''

    return item[1][0] / item[1][1]


def most_extreme_words(count, min_occ, kss, pos):
    '''Return a list of lists containing the count most extreme words
    that occur at least min_occ times in kss.
    Each item in the list is formatted as follows:
    [word, average score, number of occurrences]
    If pos is True, return the most positive words.
    If pos is False, return the most negative words.
    [examples not required]
    count: how many extreme words should it return
    min_occ: at least how many times each word should have occurred in the dataset
    kss: the dataset dictionary
    pos: whether the user is looking for the most positive or the most negative words.
    '''
    return_list = []
    for item in kss.items():
        if item[1][1] >= min_occ:
            new_list = [item[0], score(item), item[1][1]]
            return_list.append(new_list)
            
    if pos:
        # descending order
        return_list = sorted(return_list, key=itemgetter(1), reverse=True)
    else:
        # ascending order
        return_list = sorted(return_list, key=itemgetter(1))

    return return_list[0: count]

    
def most_negative_words(count, min_occ, kss):
    '''Return a list of the count most negative words that occur at least min_occ times in kss.
    '''
    
    return most_extreme_words(count, min_occ, kss, False)
    
def most_positive_words(count, min_occ, kss):
    '''Return a list of the count most positive words that occur at least min_occ times in kss.
    '''
    
    return most_extreme_words(count, min_occ, kss, True)

        
    
if __name__ == "__main__":

# Pick a dataset    
    dataset = 'tiny.txt'
    #dataset = 'small.txt'
    #dataset = 'medium.txt'
    #dataset = 'full.txt'
    
    # Your test code here
    with open(dataset, 'r') as file:
        print(word_kss_scan('brando',file))
    
    with open(dataset, 'r') as file:
        print(extract_kss(file))
        
    statement_pss("1 Brando is Brando , but for this one it 's not enough", {'brando': [6.0, 4], 'seems': [0.0, 1], 'uninspired': [0.0, 1], 'by': [0.0, 1], 'the': [8.0, 3], 'heist': [0.0, 1], 'script': [0.0, 1], 'and': [0.0, 1], 'is': [5.0, 3], 'phoning': [0.0, 1], 'it': [1.0, 2], 'marlon': [4.0, 1], 'incredible': [4.0, 1], 'as': [4.0, 1], 'patriarch': [4.0, 1], 'of': [4.0, 1], 'but': [1.0, 1], 'for': [1.0, 1], 'this': [1.0, 1], 'one': [1.0, 1], 'not': [1.0, 1], 'enough': [1.0, 1]})
    pass



