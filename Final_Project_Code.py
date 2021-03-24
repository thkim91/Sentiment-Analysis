# C:\Users\user\Anaconda3\Scripts\ipython

from textblob import TextBlob
from collections import defaultdict
import csv
from nltk.stem.snowball import SnowballStemmer  # For finding a root of word

def replace_mean(sentence):
    ''' The function switches either negative polarity to positive or positive to negative when the sentence contains
        the words in the list, change_mean '''
    change_mean = ['''don't''','''doesn't''','''didn't''','''isn't''', '''aren't''', '''wasn't''','''weren't''']
    for word in change_mean:
        if word in sentence:
            return -((sentence.sentiment.polarity)/2)

    return sentence.sentiment.polarity

def replace_word(sentence):
    ''' The textblob sentitment analysis is not enough for analyzing finance text since it was not made for it.
        The function replace words in sentence to something else so that textblob can correctly measure the polarity'''
    # list of words and their pos/neg polarities
    pos_words = {0.3:'fun', 0.4:'light', 0.5:'love', 0.7:'happiness', 0.8:'win', 1.0:'best'}
    neg_words = {-0.1:'pity', -0.3:'failure', -0.5:'angry', -0.6:'cold', -0.8:'tragic', -1.0:'grim'}
    neu_words = {0:'netural'}

    change_dic = ['homerun','bull','reward','bear','challenge','terrif','recommend','knowledg',
                 'well-inform','miss','achiev','accomplish','approximet','progress','potenti',
                 'more']

    stemmer = SnowballStemmer("english")
    example_words = sentence.words

    for i in example_words:
        stem_of_word = stemmer.stem(i)
        if stem_of_word in change_dic:
            # changing the word to root word
            sentence = sentence.replace(i,stem_of_word)
            # positive
            sentence = sentence.replace('bull',pos_words[0.7])
            sentence = sentence.replace('homerun',pos_words[0.8])
            sentence = sentence.replace('reward',pos_words[0.5])
            sentence = sentence.replace('terrif',pos_words[0.8])
            sentence = sentence.replace('recommend',pos_words[0.4])
            sentence = sentence.replace('knowledg',pos_words[0.5])
            sentence = sentence.replace('well-inform',pos_words[0.5])
            sentence = sentence.replace('achiev',pos_words[0.5])
            sentence = sentence.replace('accomplish',pos_words[0.8])
            sentence = sentence.replace('progress',pos_words[0.3])
            sentence = sentence.replace('potenti',pos_words[0.3])
            # negative
            sentence = sentence.replace('bear',neg_words[-0.8])
            sentence = sentence.replace('challenge',neg_words[-0.5])
            sentence = sentence.replace('miss',neg_words[-0.5])
            # neutral
            sentence = sentence.replace('approximet',neu_words[0.0])
            sentence = sentence.replace('more',neu_words[0.0])

    return sentence

def getting_polarity(contents, cutting_noise = 0):
    num_ex = 1
    whole_paragraph = []        

    for content in contents:
        paragraph = TextBlob(content)
        sentences = paragraph.sentences

        count_pol = 0  # increased when the sentence has pos or neg polarity.
        num_sen = 1  # it counts all of the number of sentences    
        polarity_sen = defaultdict(float)
    
        for sentence in sentences:
            replace_sentence = replace_word(sentence)
            polarity_sen[num_sen] = (replace_mean(replace_sentence))
            
            if polarity_sen[num_sen] > cutting_noise or polarity_sen[num_sen] < -cutting_noise:
                count_pol += 1
            num_sen += 1
        
        if num_ex == 1:
            if count_pol > 0: # sum up only the polarity of sentences that have pos or neg polarity and average them out.
                whole_paragraph.append(['Avg polarity of Corps result',sum(polarity_sen.values())/count_pol])
                
            else:  # if the paragrah has sentences that only have neutral polarity, just give neutral polarity.
                whole_paragraph.append(['Avg polarity of Corps result',sum(polarity_sen.values())])
        
        elif num_ex == 2:
            if count_pol > 0: # sum up only the polarity of sentences that have pos or neg polarity and average them out.
                whole_paragraph.append(['Avg polarity of Analyst Q&A',sum(polarity_sen.values())/count_pol])
                
            else:  # if the paragrah has sentences that only have neutral polarity, just give neutral polarity.
                whole_paragraph.append(['Avg polarity of Analyst Q&A',sum(polarity_sen.values())])
        
        elif num_ex == 3:
            if count_pol > 0: # sum up only the polarity of sentences that have pos or neg polarity and average them out.
                whole_paragraph.append(['Avg polarity of Comment',sum(polarity_sen.values())/count_pol])
                
            else:  # if the paragrah has sentences that only have neutral polarity, just give neutral polarity.
                whole_paragraph.append(['Avg polarity of Comment',sum(polarity_sen.values())])

        num_ex += 1

    return whole_paragraph


''' LET'S USE THE CODE '''

file_names = ['fb_full.txt', 'msft_full.txt', 'goog_full.txt', 'baba_full.txt', 'amzn_full.txt', 
              'aapl_full.txt', 's_full.txt', 'symc_full.txt', 'snap_full.txt', 'bb_full.txt', 'amd_full.txt']


noise_amount = float(input('How much do you want to exclude?: '))

polarity_csv = [] # save the polarity of each texts above into the list
for file in file_names:
    f = open(file,'r')
    text = f.read()
    text = text.replace('\n',' ')

    find_dp1 = text.find('Executives')
    find_dp2 = text.find('Copyright policy:')
    find_dp3 = text.find('Comments')
    find_dp4 = text.find('Share your comment:')
    new_text = text[find_dp1:find_dp2] 

    contents = new_text.split('Question-and-Answer Session') + [text[find_dp3:find_dp4]]
    # contents = new_text.split('////') # Every text has four '/' that separates Corps result and Analyst Q&A
    f.close()
    
    title = file.replace('_full.txt','').upper()
    each_text = [[title]] + getting_polarity(contents,noise_amount) + [[]]

    polarity_csv.append(each_text)

# f = open('all_comp_results_'+str(noise_amount)+'.csv', 'w', encoding='utf-8', newline='')
f = open('all_comp_results_'+str(noise_amount)+'.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)

wr.writerow(['Name','Avg Polarity'])
for polarities in polarity_csv:
    for polarity in polarities:
            wr.writerow(polarity)
f.close()

