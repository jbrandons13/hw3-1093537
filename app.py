from flask import Flask, render_template, request, url_for
import pandas as pd
import logomaker as lm
from matplotlib.figure import Figure
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.form['text']
    # Process the text as desired (e.g., print it or store it in a database)
    input = text.split('\r\n')

    tranform_input = ['' for _ in range(16)]
    for each in input:
        counter = 0
        for letter in each:
            tranform_input[counter] += letter
            counter += 1
    input = [item for item in tranform_input if item != '']

    amino_acids = list('ACDEFGHIKLMNPQRSTVWY')

    # Initialize a dictionary with all amino acids set to zero
    base_dict = {aa: 0 for aa in amino_acids}

    # Create a list of 20 such dictionaries
    data = [base_dict.copy() for _ in range(20)]
            
    count = 0
    for each in input:
        for letter in each:
            data[count][letter] += 1
        count += 1
    
    newlist = []
    for each in data:

        total_count = sum(each.values())
        # Calculate relative frequencies
        f = {amino_acid: (count / total_count if count != 0 else 0) for amino_acid, count in each.items()}
        newlist.append(f)

    filtered_list = [d for d in newlist if any(value != 0 for value in d.values())]
    output = base_dict
    for each in output:
        output[each] = []
        
    for each in filtered_list:
        for letter, count in each.items():
            output[letter].append(count)
            
    nt_df = pd.DataFrame(output)

    colors = {
    'A': '#1f77b4', 
    'C': '#ff7f0e', 
    'D': '#2ca02c', 
    'E': '#d62728', 
    'F': '#9467bd', 
    'G': '#8c564b', 
    'H': '#e377c2', 
    'I': '#7f7f7f', 
    'K': '#bcbd22', 
    'L': '#17becf', 
    'M': '#9edae5', 
    'N': '#aec7e8', 
    'P': '#ffbb78', 
    'Q': '#98df8a', 
    'R': '#ff9896', 
    'S': '#c5b0d5', 
    'T': '#c49c94', 
    'V': '#f7b6d2', 
    'W': '#c7c7c7', 
    'Y': '#dbdb8d'
    }
    
    # Create a sequence logo.
    fig = Figure()
    ax = fig.subplots()
    lm.Logo(nt_df, ax=ax, color_scheme=colors)
    formats = ['png','jpg','svg']
    img_filenames = {}
    for img_format in formats:
        img_filename = f"logo.{img_format}"
        fig.savefig(os.path.join('static',img_filename), format=img_format)
        img_filenames[img_format] = url_for('static', filename=img_filename)
    
    return render_template('result.html', img_filenames = img_filenames)



    # # Convert logo to PNG image
    # img_filename = 'logo.png'
    # fig.savefig(os.path.join('static', img_filename))

    # # Redirect to results page
    # return render_template('result.html', img_filename=url_for('static', filename=img_filename))

if __name__ == '__main__':
    app.run()