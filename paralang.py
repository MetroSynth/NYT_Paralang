import collections, requests, lxml
from bs4 import BeautifulSoup

class Paralang():
    def __init__(self):
        self.cn_dict = self.buildDict('./data/cedict_ts.u8')
        
    def articleText(self,target_url):
        page = requests.get(target_url) #reads the page into an object
        s = BeautifulSoup(page.text, "lxml") #native bs4 object
        parag_text = [tag.getText() for tag in s.findAll('p')] #article text is all <p> tags on NYT CN
        full_text = ''.join(parag_text)
        article_sentences = full_text.split('。')
        return article_sentences

    def buildDict(self,source):
        dictfile = open(source, encoding='utf8').readlines()
        dictlines = [i for i in dictfile if i[0] != '#'] #removes all lines that start with a '#'
        splitters = [i.split(' ') for i in dictlines]
        entry = collections.namedtuple('entry',['traditional','simplified','definition'])
        cn_collection = [entry(i[0],i[1],' '.join(i[2:]).rstrip('\n')) for i in splitters]
        return cn_collection

    def walkthrough(self,test_string,file):
        last_exact = None
        if len(test_string) == 0:
            return
        for i in range(1,len(test_string)+1):
            contained_match,exact_match = False,False
            search_str = test_string[0:i] #ss = search_string
            #print('searching:',search_str)
            for entry in self.cn_dict:
                if search_str in entry.traditional or search_str in entry.simplified:
                    contained_match = True
                    if search_str == entry.traditional or search_str == entry.simplified:
                        #print('Exact Match:',entry)
                        last_exact = entry
                        last_match = search_str
                        exact_match = True
            if exact_match == False and contained_match == False:
                break
        if last_exact is not None:
            file.write('{}|{}'.format(last_exact.simplified,last_exact.definition).encode('utf-8'))
            file.write(u'\n'.encode('utf-8'))
            #print('{}|{}'.format(last_exact.simplified,last_exact.definition))
            result_string = test_string[len(last_match):]
        else:
            result_string = test_string[len(search_str):]
        #print('Remaining string:',result_string)
        self.walkthrough(result_string,file)

    def run(self,target_url):
        article = self.articleText(target_url)
        with open('./vocab.txt','wb') as file:
            for sentence in article:
                file.write(('Chinese Text: {}'+u'\n'.format(sentence)).encode('utf-8'))
                #print('Chinese Text: {}'.format(sentence))
                self.walkthrough(sentence,file)
            print('Writing vocabulary table is complete.')
        
target_url = 'https://cn.nytimes.com/china/20170505/china-airplane-boeing-airbus/'
p = Paralang()
p.run(target_url)