from prototype.models import IngrTable, Ingr, ListTable
import pickle

def ingr_search(query, series):
    query_results = series[series.str.contains(query)==True]
    items = []
    for row in query_results:
        #print(row)
        items.append(Ingr(row, '/index'))
    return (IngrTable(items, html_attrs={'align':'center', 'class': 'table table-hover'}))

def load_list(filename):
    with open(filename, 'rb') as input:
        current_list = pickle.load(input)
        return current_list

def load_list_table(filename):
    items = []
    for item in load_list(filename).groc_list:
        items.append(Ingr(item, '#'))
    return (ListTable(items, html_attrs={'align':'center', 'class': 'table table-hover'}))
