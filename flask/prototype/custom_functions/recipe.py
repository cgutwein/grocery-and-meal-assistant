import pandas as pd
import numpy as np

# def products_to_add(options, i):
#     s=options.loc[i][needed]
#     return ', '.join(list(s[s==1].index))


def return_recipes(calories_max=800,
                   calories_min=500,
                   protein_min=25,
                   meal_type='lunch',
                   cuisine='non_specified',
                   complexity='easy',
                   n_additional_ingredients=4,
                   grocery=[]):
###############
################
################
    ## For testing, remove and find better solution for loading data after testing
    data=pd.read_csv('../python/data/data.csv')
    data.drop('Unnamed: 0', axis=1, inplace=True)
    ingredients=pd.read_csv('../python/data/ingredients_short.csv')
    ingredients.drop('Unnamed: 0', axis=1, inplace=True)

    # Upload the list of non_key ingredients
    spices=list(pd.read_csv('../python/data/spices.csv')['spices'])
    spices=[x for x in spices if x in data.columns]
    garnish=['parsley', 'dried parsley', 'cilantro', 'cilantro leaves', 'dill',
             'celery leaves', 'chives', 'chocolate chips', 'sesame', 'black sesame seeds', 'sesame seeds']
    # separate ingredients from non-ingredients
    non_ingredients=['meal','title','calories','protein','carbs','fats','sodium','cuisine', 'complexity']
    non_ingredients.extend(spices)
    group_keys=['pasta', 'mold cheese', 'soft cheese', 'brined cheese', 'medium cheese', 'hard cheese', 'cottage cheese', 'dry wine',
                'liquer', 'white wine', 'red wine']
    group=dict(zip(group_keys,
                [list(ingredients[ingredients['substitute 1']==key]['stem']) for key in group_keys]))
    group_values=[y for x in group.values() for y in x]
#################
################# End of bloated data block
#################

    # extend grocery for all available substitutes
    ingredients_nongroup=[gr for gr in grocery if gr not in group_values]
    ingredients_group=list(set([ingredients[ingredients.stem==gr]['substitute 1'].values[0] for gr in grocery if gr in group_values]))

    for x in ingredients_nongroup:
        #extend to own substitutes
        idx=ingredients[ingredients['stem']==x].index
        a=[ing for ing in ingredients.loc[idx][['substitute 1', 'substitute 2', 'substitute 3']].values if type(ing)==str]
        if len(a)>0:
            grocery.extend(a)
        #check whether the ingredient in other products substitutes
        idx=ingredients[(ingredients['substitute 1']==x)|(ingredients['substitute 2']==x)|(ingredients['substitute 3']==x)].index
        if len(idx)>0:
            grocery.extend(list(ingredients.loc[idx]['stem']))

    for x in ingredients_group:
        grocery.extend(group[x])

    if meal_type in ['lunch', 'dinner']: meal_type='lunch/dinner'

    #filter basic parameters
    options=data[(data.meal==meal_type)&
                       (data.calories<calories_max)&
                       (data.calories>calories_min)&
                       (data.protein>protein_min)&
                       (data.complexity=='easy')
                      ]
    if cuisine!='non_specified':
        options=options[options.cuisine==cuisine]

    #filter based on grocery

    # drop columns with unused ingredients
    ingredients=options.drop(non_ingredients, axis=1).columns
    options.drop([x for x in ingredients if sum(options[x])==0], axis=1, inplace=True)

    #update ingredients
    ingredients=options.drop(non_ingredients, axis=1).columns

    ## products outside the groccery list

    needed=[x for x in ingredients if x not in grocery]

    # Keep only the recipes if the number of additional key ingredients doesnt exceed 3
    sums=options[needed].sum(axis=1)
    ind=[x for x in sums.index if sums.loc[x]<=n_additional_ingredients]
    options=options.loc[ind]

    recommendation=options.loc[ind][['title', 'calories', 'protein', 'carbs', 'fats']]

    recommendation['products to add']=pd.Series([', '.join(list(options.loc[i][needed][options.loc[i][needed]==1].index)) for i in ind], index=ind)

    recommendation['# of products to add']=pd.Series([len([y for y in recommendation.loc[i]['products to add'].split(",")
                                                       if y not in non_ingredients]) for i in ind], index=ind)

    return recommendation.to_html
