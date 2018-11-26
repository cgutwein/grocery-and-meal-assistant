import pandas as pd
import numpy as np
from prototype.models import RecListTable, RecListTableItem
from sklearn.metrics.pairwise import cosine_similarity
import ast

global_data = pd.read_csv('../python/data/data.csv')
# def products_to_add(options, i):
#     s=options.loc[i][needed]
#     return ', '.join(list(s[s==1].index))

def score_nutrition(x, u_protein, u_fat, u_carb):
    # less protein - penalized, coefficient 2
    # more carbs than recommended - penalized, coefficient 2
    # more fat than recommended - penalized, coefficient 1

    penalty=-2*(min(0, u_protein-x['protein']))+\
    2*(max(0, u_carb-x['carbs']))+max(0, u_fat-x['fats'])

    return (penalty)

def score_preference(i, user_score):
    temp_data=data.drop(non_ingredients, axis=1)
    weighted_score=np.mean([cosine_similarity(np.asarray(temp_data.loc[i].reshape(1, -1)),
                                              np.asarray(temp_data.loc[key]).reshape(1, -1))*user_score[key]
                            for key in user_score.keys()])
    return (weighted_score)

def return_recipes(calories=2500,
                   protein=150,
                   fat=70,
                   carb=150,
                   meal_type='lunch',
                   cuisine='non_specified',
                   complexity=1,
                   n_additional_ingredients=4,
                   grocery=[]):
###############
################
################
    complexity_dict = {0:'easy', 1:'medium', 2:'hard'}
    complexity = complexity_dict[complexity]
    calories_max = calories / 3
    calories_min = calories / 10

    ## reducing nutritional values to per meal values
    protein_max = protein / 3
    protein_min = protein / 10
    protein_meal = protein/4
    carb_meal = carb/4
    fat_meal = fat/4

    cuisine = ast.literal_eval(cuisine)
    ## For testing, remove and find better solution for loading data after testing
    data=global_data
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
                       (data.complexity==complexity)
                      ]
    if 'all' not in cuisine:
        options=options[options.cuisine.isin(cuisine)]

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

    recommendation['nutrition penalty']=pd.Series([score_nutrition(recommendation.loc[i], protein_meal, fat_meal, carb_meal) for i in recommendation.index], index=recommendation.index)
    #
    # recommendation['user score']=pd.Series([score_preference(i, user_score) for i in recommendation.index], index=recommendation.index)
    rec_list = []
    n = len(recommendation)


    for i in range(n):
        rec_list.append(RecListTableItem(recommendation.iloc[i]['title'],recommendation.iloc[i]['calories'],recommendation.iloc[i]['fats'],recommendation.iloc[i]['carbs'],recommendation.iloc[i]['protein'],recommendation.iloc[i]['products to add'], recommendation.iloc[i]['nutrition penalty']))
    return (RecListTable(rec_list, html_attrs={'align':'center', 'class':'table table-striped'}))
