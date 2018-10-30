from prototype.models import IngrTable, Ingr

def ingr_search(query, series):
    query_results = series[series.str.contains(query)==True]
    items = []
    for row in query_results:
        #print(row)
        items.append(Ingr(row, '/index'))
    return (IngrTable(items, html_attrs={'align':'center', 'class': 'table table-hover'}))
