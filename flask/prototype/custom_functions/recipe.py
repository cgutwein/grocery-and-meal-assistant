import pandas as pd
import numpy as np
from prototype.models import RecListTable, RecListTableItem
from sklearn.metrics.pairwise import cosine_similarity
import ast

global_data = pd.read_csv('../python/data/data.csv')
global_data.drop('index', axis=1, inplace=True)

#################
################# End of bloated data block
#################

# extend grocery for all available substitutes
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


def score_preference(i, user_score, temp_data):
    weighted_score=np.mean([cosine_similarity(np.asarray(temp_data.loc[i]).reshape(1, -1),
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
                   grocery=[],
                   user_score={},
                   sort_field = 'title',
                   userspecs='n'):
###############
################
################

    ## desserts and drinks wouldnt have the calories limit, but would be sorted by their nutrition values
    calories_split={'breakfast': 0.2, 'lunch/dinner': 0.3, 'lunch': 0.3, 'dinner': 0.3, 'snack': 0.1}

    if meal_type in calories_split.keys():
        calories_meal = calories*calories_split[meal_type]
        calories_max = calories_meal*1.2
        calories_min = calories_meal*0.8
        if meal_type=='breakfast':
            calories_min = calories_meal*0.7

    ## reducing nutritional values to per meal values
        protein_meal = protein*calories_split[meal_type]
        protein_min = protein_meal*0.85
        if meal_type=='breakfast':
            calories_min = calories_meal*0.7

        carb_meal = carb*calories_split[meal_type]
        fat_meal = fat*calories_split[meal_type]

    cuisine = ast.literal_eval(cuisine)
    ## For testing, remove and find better solution for loading data after testing
    data=global_data

    ingredients=pd.read_csv('../python/data/ingredients_short.csv')
    ingredients.drop('Unnamed: 0', axis=1, inplace=True)

    # Upload the list of non_key ingredients
    spices=list(pd.read_csv('../python/data/spices.csv')['spices'])
    spices=[x for x in spices if x in data.columns]
    garnish=['parsley', 'dried parsley', 'cilantro', 'cilantro leaves', 'dill',
             'celery leaves', 'chives', 'chocolate chips', 'sesame', 'black sesame seeds', 'sesame seeds']
    # separate ingredients from non-ingredients
    non_ingredients=['meal','title','calories','protein','carbs','fats','sodium','cuisine', 'complexity', 'recipe_text', 'ingredient_txt', 'image', 'image_link', 'breakfast', 'lunch', 'dinner', 'drink', 'snack']
  
    non_ingredients.extend(spices)
    group_keys=['pasta', 'mold cheese', 'soft cheese', 'brined cheese', 'medium cheese', 'hard cheese', 'cottage cheese', 'dry wine',
                'liquer', 'white wine', 'red wine']
    group=dict(zip(group_keys,
                [list(ingredients[ingredients['substitute 1']==key]['stem']) for key in group_keys]))
    group_values=[y for x in group.values() for y in x]
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

    if meal_type in calories_split.keys():
        options=data[(data.meal==meal_type)&
                       (data.calories<calories_max)&
                       (data.calories>calories_min)&
                       (data.protein>protein_min)&
                       (data.complexity<=complexity)
                      ]

    else:
        options=data[(data.meal==meal_type)&
                       (data.complexity<=complexity)]
    if 'all' not in cuisine:
        options=options[options.cuisine.isin(cuisine)]

    print("shape", options.shape)

    #filter based on userspecs
    if userspecs=='vg':
        meat_ingr=list(ingredients[ingredients['food type'].isin(['meat', 'poultry'])]['stem'])
        to_remove=[i for i in options.index if np.sum(options.loc[i][meat_ingr])>0]
        options.drop(to_remove, inplace=True)
    elif userspecs=='ve':
        meat_ingr=list(ingredients[ingredients['food type'].isin(['meat', 'poultry', 'fish', 'dairy', 'egg', 'seafood'])]['stem'])        
        to_remove=[i for i in options.index if np.sum(options.loc[i][meat_ingr])>0]
        options.drop(to_remove, inplace=True)
     
    #filter based on grocery

    # drop columns with unused ingredients
    ingr=[x for x in options.columns if x not in non_ingredients]
    zero_column=[x for x in ingr if sum(options[x])==0]
    #print("zero_column", len(zero_column))

    options.drop(zero_column, axis=1, inplace=True)

    #print("shape 1", options.shape)

    #update ingredients
    ingr=[x for x in options.columns if x not in non_ingredients]

    ## products outside the groccery list

    needed=[x for x in ingr if x not in grocery]

    # Keep only the recipes if the number of additional key ingredients doesnt exceed n
    sums=options[needed].sum(axis=1)
    ind=[i for i in sums.index if sums.loc[i]<=n_additional_ingredients]
    options=options.loc[ind]
    recommendation=options.loc[ind][['title', 'calories', 'protein', 'carbs', 'fats', 'image_link', 'recipe_text', 'ingredient_txt']]

    recommendation['products to add']=pd.Series([', '.join(list(options.loc[i][needed][options.loc[i][needed]==1].index)) for i in ind], index=ind)

    recommendation['# of products to add']=pd.Series([len([y for y in recommendation.loc[i]['products to add'].split(",")
                                                       if y not in non_ingredients]) for i in ind], index=ind)
    if meal_type in calories_split.keys():
        recommendation['nutrition penalty']=pd.Series([score_nutrition(recommendation.loc[i], protein_meal, fat_meal, carb_meal) for i in recommendation.index], index=recommendation.index)
    else:
        recommendation['nutrition penalty']=pd.Series([(recommendation.loc[i]['carbs']+recommendation.loc[i]['fats']) for i in recommendation.index], index=recommendation.index)
    # Creation of temp_dataset for the user_score calculation
    
    if sort_field=='user score':
        
        user_score=dict(zip([int(x) for x in user_score.keys()], [int(y) for y in user_score.values()]))
        temp_data=data[data.meal==meal_type]
        temp_data=temp_data.drop(non_ingredients, axis=1)

    # Filter the user_score dict to have only the items of the appropriate meal type
        keys=list(filter(lambda x: data.loc[x].meal==meal_type, user_score.keys()))
        temp_user_score=dict(zip(keys, [user_score[key] for key in keys]))

        if len(temp_user_score.keys())==0:
            recommendation['user score']=pd.Series([0]*recommendation.shape[0], index=recommendation.index)
        else:
            recommendation['user score']=pd.Series([score_preference(i, temp_user_score, temp_data) for i in recommendation.index], index=recommendation.index)
    else:      
        recommendation['user score']=pd.Series([0]*recommendation.shape[0], index=recommendation.index)

   # Create the output dataset
    rec_list = []
    n = len(recommendation)
    sort_order={'title':True, 'calories':True, 'fats':True, 'carbs':True, 'protein': False, 'products to add': True, 'nutrition penalty': True, 'user score': False}
    rec_sorted = recommendation.sort_values(by=[sort_field], ascending=sort_order[sort_field])
    print("rec_sorted", len(rec_sorted['image_link']))
    for i in range(n):
        rec_list.append(RecListTableItem(rec_sorted.iloc[i]['title'],rec_sorted.iloc[i]['calories'],rec_sorted.iloc[i]['fats'],rec_sorted.iloc[i]['carbs'],rec_sorted.iloc[i]['protein'],rec_sorted.iloc[i]['products to add'], rec_sorted.iloc[i]['nutrition penalty'], rec_sorted.iloc[i]['user score']))
    return (rec_sorted) #(RecListTable(rec_list, html_attrs={'align':'center', 'class':'table table-hover'}))
