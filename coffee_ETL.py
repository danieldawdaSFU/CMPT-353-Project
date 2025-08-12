import pandas as pd
import sys

def coffees_num(d):
    if d == 'Less than 1':
        ret = 0
    elif d == 'More than 4':
        ret = 5
    else: 
        ret = int(d)

    return ret
    
def main():

    # read csv
    df = pd.read_csv('data/GACTT_RESULTS_ANONYMIZED_v2.csv', index_col='Submission ID')

    # rename annoying column(s)
    df = df.rename(columns={"Before today's tasting, which of the following best described what kind of coffee you like?": 'taste',
                            "What is the most you've ever paid for a cup of coffee?": "most_expensive_purchase",
                            "How many cups of coffee do you typically drink per day?": "num_cups_daily",
                            "Where do you typically drink coffee?": "coffee_location",
                            "What is your favorite coffee drink?": "fav_drink",
                            "What is your age?": "age",
                            "What roast level of coffee do you prefer?" : "pref_roast",
                            "What kind of dairy do you add? (Whole milk)": "whole_milk",
                            "What kind of dairy do you add? (Skim milk)": "skim_milk",
                            "What kind of dairy do you add? (Half and half)": "half_and_half",
                            "What kind of dairy do you add? (Coffee creamer)": "creamer", 
                            "What kind of dairy do you add? (Flavored coffee creamer)": "flav_creamer",
                            "What kind of dairy do you add? (Oat milk)": "oat_milk",
                            "What kind of dairy do you add? (Almond milk)": "almond_milk",
                            "What kind of dairy do you add? (Soy milk)": "soy_milk",
                            "What kind of dairy do you add? (Other)": "other_dairy",
                            "What kind of sugar or sweetener do you add? (Granulated Sugar)": "sugar",
                            "What kind of sugar or sweetener do you add? (Artificial Sweeteners (e.g., Splenda))": "art_sweet",
                            "What kind of sugar or sweetener do you add? (Honey)": "honey",
                            "What kind of sugar or sweetener do you add? (Maple Syrup)": "maple_syrup",
                            "What kind of sugar or sweetener do you add? (Stevia)": "stevia",
                            "What kind of sugar or sweetener do you add? (Agave Nectar)": "agave_nectar",
                            "What kind of sugar or sweetener do you add? (Brown Sugar)": "brown_sugar",
                            "What kind of sugar or sweetener do you add? (Raw Sugar (Turbinado))": "raw_sugar",
                            "Ethnicity/Race": "ethnicity",
                            "Employment Status": "employment_status"})

    # https://www.geeksforgeeks.org/pandas/using-dictionary-to-remap-values-in-pandas-dataframe-columns/
    map_columns = ['whole_milk', 'skim_milk', 'half_and_half', 'creamer', 'flav_creamer', 'oat_milk', 'almond_milk', 'soy_milk', 'other_dairy', 'sugar', 'art_sweet', 'honey', 'maple_syrup', 'stevia', 'agave_nectar', 'brown_sugar',  'raw_sugar']
    tf_dict = {True: 1, False: 0}

    # loop for easy iteration
    for col in map_columns:
        df[col] = df[col].map(tf_dict)

    # values to fillna 0
    values = {"whole_milk": 0, "skim_milk": 0, "half_and_half": 0, "creamer": 0,"flav_creamer": 0,"oat_milk": 0, "almond_milk": 0, "soy_milk": 0,"other_dairy": 0,"sugar": 0,"art_sweet": 0,"honey": 0,"maple_syrup": 0,"stevia": 0,"agave_nectar": 0,"brown_sugar": 0,"raw_sugar": 0}
    df = df.fillna(value=values)

    # change to just other
    df.loc[df['Gender'] == 'Other (please specify)', 'Gender'] = 'Other'
    df.loc[df['Gender'] == 'Prefer not to say', 'Gender'] = 'Other'
    df.loc[df['ethnicity'] == 'Other (please specify)', 'Ethnicity/Race'] = 'Other'

    # we care about how much coffee people are drinking per day
    num_drinks = df.dropna(subset=['num_cups_daily', 'coffee_location'])
    
    # we only really want people who drink coffee on the go or at cafes
    num_drinks = num_drinks[num_drinks['coffee_location'].str.contains('cafe|go')]
    
    # change how many drinks per day to numberical where 0 is 'less than 1' and 5 is 'more than 4'
    num_drinks['num_cups_daily'] = num_drinks['num_cups_daily'].apply(coffees_num)

    # create a column for identifyig drinks that contain espresso 
    # list of drinks that contain espresso
    espresso_drinks = ['Cappuccino', 'Cortado', 'Latte', 'Mocha', 'Americano', 'Espresso']
    num_drinks['is_espresso'] =  num_drinks['fav_drink'].isin(espresso_drinks)

    # group most_expensive_purchase in terms of 'high', 'medium', 'low'
    num_drinks['most_expensive_purchase_cat'] = num_drinks['most_expensive_purchase']
    
    # low category: 0
    num_drinks.loc[num_drinks['most_expensive_purchase_cat'] == 'Less than $2', 'most_expensive_purchase_cat'] = 0
    num_drinks.loc[num_drinks['most_expensive_purchase_cat'] == '$2-$4', 'most_expensive_purchase_cat'] = 0
    num_drinks.loc[num_drinks['most_expensive_purchase_cat'] == '$4-$6', 'most_expensive_purchase_cat'] = 0
    num_drinks.loc[num_drinks['most_expensive_purchase_cat'] == '$6-$8', 'most_expensive_purchase_cat'] = 0

    # high category: 1
    num_drinks.loc[num_drinks['most_expensive_purchase_cat'] == '$8-$10', 'most_expensive_purchase_cat'] = 1
    num_drinks.loc[num_drinks['most_expensive_purchase_cat'] == '$10-$15', 'most_expensive_purchase_cat'] = 1
    num_drinks.loc[num_drinks['most_expensive_purchase_cat'] == '$15-$20', 'most_expensive_purchase_cat'] = 1
    num_drinks.loc[num_drinks['most_expensive_purchase_cat'] == 'More than $20', 'most_expensive_purchase_cat'] = 1

    num_drinks = num_drinks.reset_index()

    cleaned = num_drinks[['Submission ID', 'taste', 'Gender','most_expensive_purchase_cat', 'num_cups_daily', 'coffee_location', 'fav_drink', 'age', 'is_espresso', 'pref_roast', 'whole_milk', 'skim_milk', 'half_and_half', 'creamer', 'flav_creamer', 'oat_milk', 'almond_milk', 'soy_milk', 'other_dairy', 'sugar', 'art_sweet', 'honey', 'maple_syrup', 'stevia', 'agave_nectar', 'brown_sugar',  'raw_sugar', 'ethnicity', 'employment_status']]
    cleaned.to_csv('data/coffee_cleaned.csv')


if __name__ == '__main__':
    main()