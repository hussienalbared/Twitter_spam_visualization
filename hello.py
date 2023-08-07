# Shamelessly copied from http://flask.pocoo.org/docs/quickstart/
from flask import  render_template
import csv
from flask import Flask
import pandas as pd
app = Flask(__name__)
import sys
print(sys.executable)
import matplotlib


import matplotlib.pyplot as plt
from io import BytesIO
import base64



@app.route('/')
def hello_world():    

    df = pd.read_csv('data.csv',sep="\t")

    # # Convert DataFrame to HTML table
    df_html = df.to_html(classes='table table-bordered', index=False)

    return render_template('index.html', df_html=df_html)

@app.route('/dash')
def dash():   
     

    df = pd.read_csv('data.csv',sep="\t")
    yes_rows = (df["output"] == "yes").sum()
    no_rows = (df["output"] == "no").sum()
    labels = ['Spam', 'Not spam']
    sizes = [yes_rows, no_rows]
    plt.clf()
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))
    plt.pie(sizes, labels=labels, autopct=lambda p: f'{int(p * sum(sizes) / 100)}', shadow=True, startangle=140)
    plt.axis('equal') 
    img = BytesIO()
    plt.legend() 
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return render_template('dash.html', chart=img_base64)


@app.route('/bar')
def bar():
    
    df = pd.read_csv('data.csv',sep="\t")

    df['Date'] = pd.to_datetime(df['date'])

    counts = df.groupby(['Date', 'output']).size().unstack(fill_value=0)
    print(counts)
    # print(counts.index.values)
    date_values =  [date.strftime('%Y-%m-%d') for date in counts.index]
    # print(date_values)
    # figures = []

    # fig1, ax1 = plt.subplots()
    # fig2, ax2 = plt.subplots()
    # counts['yes'].plot(kind='bar', color='red',ax=ax1, label='Spam')
    # ax1.set_title('Bar Chart 1')
   
    # counts['no'].plot(kind='bar', color='red',ax=ax2, label='Spam')
    # ax2.set_title('Bar Chart 2')
    
    
    # figures.append(fig1)
    # figures.append(fig2)
    
    # plot_imgs = []

    # for fig in figures:
    #     img = BytesIO()
    #     fig.savefig(img, format='png')
    #     img.seek(0)
    #     plt.close(fig)
    #     plot_imgs.append(base64.b64encode(img.getvalue()).decode())
    figures = []

    # Bar Chart 1
    fig1, ax1 = plt.subplots()
    categories1 = ['A', 'B', 'C']
    values1 = counts['yes']
    ax1.bar(date_values, values1)
    ax1.set_title('Spam')
    img1 = BytesIO()
    fig1.savefig(img1, format='png')
    img1.seek(0)
    plt.close(fig1)
    figures.append(base64.b64encode(img1.getvalue()).decode())

    # Bar Chart 2
    fig2, ax2 = plt.subplots()
    
    values2 = counts['no']
    ax2.bar(date_values, values2)
    ax2.set_title('Not spam')
    img2 = BytesIO()
    fig2.savefig(img2, format='png')
    img2.seek(0)
    plt.close(fig2)
    figures.append(base64.b64encode(img2.getvalue()).decode())



    # return render_template('bar.html', img_base64=plot_imgs)
    return render_template('bar.html', figures=figures)

    
    
if __name__ == '__main__':
    app.run()

