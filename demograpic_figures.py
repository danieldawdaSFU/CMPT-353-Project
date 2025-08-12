import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns

def main():

    # read csv
    df = pd.read_csv('data/coffee_cleaned.csv', index_col='Submission ID')

    # set graph settings
    sns.set_theme(style="whitegrid")
    # sub plots -> https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    
    
    # get count from each age group
    ages = df.groupby(by='age').size().reset_index(name='count')
    axs[0,0].pie(ages['count'],labels=ages['age'], autopct='%1.1f%%', startangle=180)
    axs[0,0].set_title('Age split')

    # get count from each gender
    # change column value on value -> https://www.geeksforgeeks.org/data-analysis/how-to-replace-values-in-column-based-on-condition-in-pandas/
    gen = df
    gen = gen.groupby(by='Gender').size().reset_index(name='count')
    axs[1,0].pie(gen['count'],labels=gen['Gender'], autopct='%1.1f%%', labeldistance=1.2, startangle=180)
    axs[1,0].set_title('Gender split')

    # get count from each ethnicity
    eth = df
    eth = eth.groupby(by='ethnicity').size().reset_index(name='count')
    axs[0,1].pie(eth['count'],labels=eth['ethnicity'], autopct='%1.1f%%', labeldistance=1.2, startangle=60)
    axs[0,1].set_title('Ethnicity/Race split')
    
    # get count from each employment status
    emp = df.groupby(by='employment_status').size().reset_index(name='count')
    axs[1,1].pie(emp['count'],labels=emp['employment_status'], autopct='%1.1f%%', labeldistance=1.2, startangle=270)
    axs[1,1].set_title('Employment split')

    # save final plot
    fig.savefig('figures/demograpics.png')


if __name__ == '__main__':
    main()