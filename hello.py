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
import numpy as np


@app.route('/')
def hello_world():    

    df = pd.read_csv('data.csv',sep="\t")

    # # Convert DataFrame to HTML table
    # df_html = df.to_html(classes='table table-bordered', index=False)

    # return render_template('index.html', df_html=df_html)
    return render_template('index.html', data=df.to_dict('records'))

@app.route('/dash')
def dash():
    df = pd.read_csv('data.csv', sep="\t")
    
    pie_chart = get_pie_chart(df)
    bar_chart = get_bar_chart(df)
    classes_bar_chart = get_spam_counts_classes(df)
    
    return render_template('dash.html', pie_chart=pie_chart, bar_chart=bar_chart,classeschart =classes_bar_chart)


def get_pie_chart(df):
    yes_rows = (df["output"] == "yes").sum()
    no_rows = (df["output"] == "no").sum()
    
    labels = ['Spam', 'Not spam']
    sizes = [yes_rows, no_rows]
    
    plt.clf()  # Clear any previous plots
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.pie(sizes, labels=labels, autopct=lambda p: f'{int(p * sum(sizes) / 100)}', shadow=True, startangle=140)
    ax.axis('equal')
    
    # Save the plot to an in-memory buffer
    img_buffer = BytesIO()
    plt.legend()
    plt.savefig(img_buffer, format='png')
    plt.close(fig)
    
    # Convert the image buffer to a base64 encoded string
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    return img_base64






def get_bar_chart(df):
    df['Date'] = pd.to_datetime(df['date'])

    counts = df.groupby(['Date', 'output']).size().unstack(fill_value=0)
    date_values = [date.strftime('%Y-%m-%d') for date in counts.index]
    SPAM = counts['yes']
    NOSPAM = counts['no']

    # Calculate the positions for bars
    bar_width = 0.35  # Width of each bar
    bar_positions = np.arange(len(date_values))  # Positions for categories

    # Create the figure and axis
    fig, ax = plt.subplots()

    # Plot the bars for each set of values
    ax.bar(bar_positions - bar_width/2, SPAM, width=bar_width, label='SPAM')
    ax.bar(bar_positions + bar_width/2, NOSPAM, width=bar_width, label='NOT SPAM')

    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.set_title('SPAM & NOT SPAM')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(date_values)
    ax.legend()

    # Save the plot to an in-memory buffer
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    plt.close(fig)
    
    # Convert the image buffer to base64 encoded string
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    return img_base64
 

def get_spam_counts_classes(df):
    df['Date'] = pd.to_datetime(df['date'])

    counts = df.groupby(['username', 'output']).size().unstack(fill_value=0)
    users_spams=counts['yes']
    users_less_than_10_spam = users_spams[users_spams < 10]
    users_more_than_10_spam = users_spams[users_spams > 10]
    users_0_spam = users_spams[users_spams ==0]
    print(users_less_than_10_spam.count())
    print(users_more_than_10_spam.count())
    print(users_0_spam.count())
    categories = ['< 10_spam', ' > 10_spam', '0 spam']
    values = [users_less_than_10_spam.count(), users_more_than_10_spam.count(), users_0_spam.count()]

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Create a bar chart
    ax.bar(categories, values,label='Count Classes')

    # Set labels and title
    ax.set_title('Spam counts classes')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Counts')
    ax.legend()

    # Save the plot to an in-memory buffer
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='png')
    plt.close(fig)
    
    # Convert the image buffer to base64 encoded string
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    return img_base64   
    
if __name__ == '__main__':
    app.run()

