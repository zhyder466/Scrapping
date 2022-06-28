from bs4 import BeautifulSoup
import requests
from tkinter import messagebox
from csv import writer
import tkinter as tk
import pandas as pd
from tkinter import *
import matplotlib.pyplot as plt

a = tk.Tk()
a.title('Data Scraper')
a.geometry('700x780')
img = PhotoImage(file='back.png')
lab = Label(a,image=img)
lab.place(x=0,y=0)
a.config(bg='#34495E')
t = tk.StringVar()
a.resizable(False,False)

def scrapeDataFromSite():
    url = t.get()
    if url == 'https://www.bbc.com/urdu':
        page2 = requests.get(url)
        soup2 = BeautifulSoup(page2.text,'lxml')
        refLinks = soup2.find_all('a','bbc-puhg0e e1ibkbh73')

        storyCount = 0
        b = True
        links = []
        with open('stories.csv','w',newline='',encoding='utf8') as f:
            thewriter = writer(f)
            header=['Headlines','Stories','Category']
            thewriter.writerow(header)
            for z in refLinks:
                label = tk.Label(text='Successfully Scraped!', font=('Arial 16 bold'), bg='#34495E', fg='white')
                label.place(x=600, y=68)
                c=1
                while(b):
                    page = requests.get('https://www.bbc.com'+z['href']+'?page='+str(c))
                    soup = BeautifulSoup(page.text,'lxml')

                    link_soup = soup.select('.bbc-uk8dsi.emimjbx0')

                    for i in link_soup:
                        links.append(i['href'])
                    for l in links:
                        req = requests.get(l)
                        soup1 = BeautifulSoup(req.text,'lxml')
                        try:
                            blog = soup1.select('.e1j2237y4.bbc-1n11bte.essoxwk0')[0]
                            title = blog.select('.bbc-1pfktyq.essoxwk0')[0].text
                            body_soup = blog.select('.bbc-4wucq3.essoxwk0')
                        except ConnectionError:
                            continue
                        except Exception:
                            continue
                        body_text = []
                        for p in body_soup:
                            body_text.append(p.text)
                        body_text = ' '.join(body_text)
                        info = [title,body_text,z.text]
                        thewriter.writerow(info)
                        storyCount+=1
                        print(storyCount)
                        if storyCount == 100:
                            b= False
                            break
                    c+=1
                b= True
                storyCount=0
    else:
        r = tk.Tk()
        r.withdraw()
        messagebox.showerror("ERROR",'PLEASE ENTER BBC URDU WEBSITE LINK ONLY!')
        r.mainloop()


file = pd.read_excel('C:\\Users\\Zeeshan\\Documents\\Scraped.xlsx')
headlines = file['Headlines'].values
stories = file['Stories'].values
category = file['Category'].values
data = []
h = str(headlines).split()
s = str(stories).split()
c = str(category).split()
for i in h:
    data.append(i)
for i in c:
    data.append(i)
for i in s:
    data.append(i)

def getMaxLengthStory():
    max = 0
    longStory = ''
    for i in stories.tolist():
        if len(i)>max:
            max = len(i)
            longStory = i
    frm = tk.Tk()
    frm.geometry("600x500")
    frm.resizable(False, False)
    frm.title('Longest Story')
    T = tk.Text(frm, height=60, width=60,font=('Arial 16 bold'))
    l = tk.Label(frm, text="LONGEST STORY IN DATASET")
    l.config(font=('Arial 18 bold'))
    l.pack()
    T.pack()
    T.insert(tk.END, longStory)
    tk.mainloop()

def getMinLengthStory():
    min = len(stories.tolist()[0])
    minStory = ''
    for i in stories:
        if len(i)<min:
            min = len(i)
            minStory = i
    frame = tk.Tk()
    frame.geometry("600x500")
    frame.title('Shortest Story')
    frame.resizable(False, False)
    T = tk.Text(frame, height=60, width=60,font=('Arial 16 bold'))
    l = tk.Label(frame, text="SHORTEST STORY IN DATASET")
    l.config(font=('Arial 18 bold'))
    l.pack()
    T.pack()
    T.insert(tk.END,minStory)
    tk.mainloop()

def getUniqueWords():
    words = []
    for i in data:
        if i not in words:
            words.append(i)
    frame = tk.Tk()
    frame.geometry("400x100")
    frame.resizable(False, False)
    frame.title('Total Unique Words')
    T = tk.Text(frame, height=5, width=20,font=('Arial 20 bold'))
    l = tk.Label(frame, text="TOTAL UNIQUE WORDS IN DATASET")
    l.config(font=('Arial 14 bold'))
    l.pack()
    T.pack()
    T.insert(tk.END, str(len(words)))
    tk.mainloop()

def topTenWordsByFrequency():
    d = {}
    l = {}
    s =''
    for i in data:
        if not i in d:
            d[i] = 1
        else:
            d[i] = (d.get(i)+1)
    c=0
    while c<10:
        max = 0
        word = ''
        for i in d:
            if d[i]>max:
                max = d[i]
                word = i
        l[word] = d[word]
        s+=(word+' : '+str(d[word])+'\n')
        d[word] = -1
        c+=1
    frame = tk.Tk()
    frame.geometry("400x350")
    frame.resizable(False,False)
    frame.title('Shortest Story')
    T = tk.Text(frame, height=20, width=20,font=('Arial 18 bold'))
    l = tk.Label(frame, text="TOP 10 WORDS BY FREQUENCY")
    l.config(font=('Arial 18 bold'))
    l.pack()
    T.pack()
    T.insert(tk.END, s)
    tk.mainloop()

def countStoriesForEachCategory():
    categs = {}
    str1 = ''
    for i in category:
        if i not in categs:
            categs[i]=1
        else:
            categs[i] = (categs.get(i)+1)
    for j in categs:
        str1+= j+" : "+str(categs.get(j))+'\n'
    frame = tk.Tk()
    frame.geometry("470x350")
    frame.resizable(False, False)
    frame.title('Shortest Story')
    T = tk.Text(frame, height=20, width=20, font=('Arial 18 bold'))
    l = tk.Label(frame, text="TOTAL STORIES FOR EACH CATEGORY")
    l.config(font=('Arial 18 bold'))
    l.pack()
    T.pack()
    T.insert(tk.END, str1)
    tk.mainloop()

def plotBarGraph():
    categs = {}
    for i in category:
        if i not in categs:
            categs[i] = 1
        else:
            categs[i] = (categs.get(i) + 1)
    cat = []
    total = []
    for j in categs:
        cat.append(j[::-1])
        total.append(categs[j])
    f = plt.figure(figsize=(7,5))
    pos = [1,2,3,4,5,6,7]
    plt.bar(pos,total,color='blue',width=0.5)
    plt.xticks(pos,cat)
    plt.show()

#Main GUI Interface
label = tk.Label(text='ENTER WEBSITE LINK: ',font=('Arial 16 bold'),bg='black',fg='white')
label.place(x=5,y=20)
button = tk.Button(text='SCRAPE NOW',bg='#27AE60',fg='white',command=scrapeDataFromSite,font=('Arial 16 bold'))
button.place(x=430,y=75)
label1 = tk.Label(text='SHORTEST STORY IN DATASET:',font=('Arial 16 bold'),bg='black',fg='white')
label1.place(x=5,y=200)
button1 = tk.Button(text='Click here to print',bg='#27AE60',fg='white',command=getMinLengthStory,font=('Arial 16 bold'))
button1.place(x=430,y=192)
label2 = tk.Label(text='LONGEST STORY IN DATASET:',font=('Arial 16 bold'),bg='black',fg='white')
label2.place(x=5,y=300)
button2 = tk.Button(text='Click here to print',bg='#27AE60',fg='white',command=getMaxLengthStory,font=('Arial 16 bold'))
button2.place(x=430,y=292)
text = tk.Entry(textvariable=t,font=('Arial 16 bold'),width=35,relief='groove',borderwidth=2,fg='#34495E')
text.place(x=260,y=20)
label3 = tk.Label(text='TOP TEN WORDS BY FREQUENCY:',font=('Arial 16 bold'),bg='black',fg='white')
label3.place(x=5,y=400)
button3 = tk.Button(text='Click here to print',bg='#27AE60',fg='white',command=topTenWordsByFrequency,font=('Arial 16 bold'))
button3.place(x=430,y=392)
label4 = tk.Label(text='TOTAL UNIQUE WORDS IN DATASET:',font=('Arial 16 bold'),bg='black',fg='white')
label4.place(x=5,y=500)
button4 = tk.Button(text='Click here to print',bg='#27AE60',fg='white',command=getUniqueWords,font=('Arial 16 bold'))
button4.place(x=430,y=492)
label5 = tk.Label(text='TOTAL STORIES FOR EACH CATEGORY:',font=('Arial 16 bold'),bg='black',fg='white')
label5.place(x=5,y=600)
button5 = tk.Button(text='Click here to print',bg='#27AE60',fg='white',command=countStoriesForEachCategory,font=('Arial 16 bold'))
button5.place(x=430,y=592)
label6 = tk.Label(text='PLOT BAR GRAPH FOR DATASET:',font=('Arial 16 bold'),bg='black',fg='white')
label6.place(x=5,y=700)
button6 = tk.Button(text='Click here to print',bg='#27AE60',fg='white',command=plotBarGraph,font=('Arial 16 bold'))
button6.place(x=430,y=692)
a.mainloop()