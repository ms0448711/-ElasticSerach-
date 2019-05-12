from elasticsearch import Elasticsearch, helpers
import json
import tkinter as tk

class GUI:
    def __init__(self):
        self.window=tk.Tk()
        window=self.window
        window.title("Question Answering System About Studying Abroad")
        #window.geometry("600x370")
        self.q_ent = tk.Entry(window)
        self.pnum_ent = tk.Entry(window)
        self.confirm = tk.Button(window,
        text='Enter',width=15,height=2,command=self.run)
        
        v=tk.StringVar()
        self.q_lab = tk.Label(window,
        textvariable=v)
        v.set("Question: ")
        
        v=tk.StringVar()
        self.pnum_lab = tk.Label(window,
        textvariable=v)
        v.set("Candidate(s)#: ")
        
        self.scrollbar = tk.Scrollbar(window)
        self.scrollbar.grid(row=3,column=4)
        

        self.a_text = tk.Text(window,width=120,height=2,)
        self.a_text.insert('end','Scores Here')

        self.d_text = tk.Text(window,width=120,height=40,yscrollcommand=self.scrollbar.set)
        self.d_text.insert('end',"Data Here")
        
        self.scrollbar.config(command=self.d_text.yview)
        
        

        
        self.ress=None
        
        self.curPage=0
        self.pnum=1
        
        def last_page():
            self.curPage-=1
            self.refresh()
        
        def next_page():
            self.curPage+=1
            self.refresh()
        
        self.lb=tk.Button(window,text='<<',width=15,height=2,command=last_page)
        self.nb=tk.Button(window,text='>>',width=15,height=2,command=next_page)
        self.GUI_positioning()
        tk.mainloop()
    
    def GUI_positioning(self):
        self.q_lab.grid(row=0,column=0)
        self.q_ent.grid(row=0,column=1)
        self.confirm.grid(row=1,column=2)
        self.pnum_lab.grid(row=1,column=0)
        self.pnum_ent.grid(row=1,column=1)
        self.a_text.grid(row=2,column=3)
        self.d_text.grid(row=3,column=3)
        self.lb.grid(row=3,column=0)
        self.nb.grid(row=3,column=1)
    
    def refresh(self):
        self.curPage+=self.pnum
        self.curPage%=self.pnum
        self.a_text.delete('1.0','end')
        self.d_text.delete('1.0','end')
        self.a_text.insert('end',self.ress['hits']['hits'][self.curPage]['_score'])
        self.d_text.insert('end',self.ress['hits']['hits'][self.curPage]['_source']['content'])
        
        
    
    def run(self):
        es=Elasticsearch()
        INDEX_NAME = 'studyabroad'
        DOC_TYPE = 'one_to_one'
        self.pnum=self.pnum_ent.get()
        try:
            self.pnum=int(self.pnum)
        except:
            print("Please Enter Valid Number")
            self.d_text.delete('1.0','end')
            self.d_text.insert('end',"Please Enter Valid Number")
            return
        try:
            target=self.q_ent.get()
        except:
            print("Please Input Valid Question")
            self.d_text.delete('1.0','end')
            self.d_text.insert('end',"Please Input Valid Question")
            return
        
        query_mapping = {
            "query": {
                "match": {"content": target}
            },
            "size": self.pnum
        }
        self.ress = es.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=query_mapping)
        self.curPage=0
        self.refresh()
        '''
        for res in ress['hits']['hits']:
            #res = ress['hits']['hits'][0]
            self.a_text.delete('1.0','end')
            self.d_text.delete('1.0','end')
            self.a_text.insert('end',res['_score'])
            self.d_text.insert('end',res['_source']['content'])
            #print(res['_source']['content'])
        '''


def query(target):
    es = Elasticsearch()
    INDEX_NAME = 'studyabroad'
    DOC_TYPE = 'one_to_one'
    query_mapping = {
        "query": {
            "match": {"content": target}
        },
        "size": 5
    }
    ress = es.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=query_mapping)
    for res in ress['hits']['hits']:
        #res = ress['hits']['hits'][0]
        print(res['_score'])
        #print(res['_source']['content'])

if __name__ == '__main__':
    gui=GUI()