import altair as alt
import pandas as pd
import json

def createChart(data, zipcode):
    color_expression    = "highlight._vgsid_==datum._vgsid_"
    color_condition     = alt.ConditionalPredicateValueDef(color_expression, "Teal")
    highlight_selection = alt.selection_single(name="highlight", empty="all", on="mouseover")
    #rating_selection    = alt.selection_single(name="rating", empty="all", encodings=['y'])
    data = data[data['zipcode']==zipcode].nlargest(20, 'num')
    try:
        maxCount            = int(data['num'].max())
    except ValueError:
        maxCount = 10
        data = pd.DataFrame([{"name":"undefine", "num":0}])

    return alt.Chart(data)\
              .mark_bar(stroke="Black")\
              .encode(
                  alt.X("num:Q", axis=alt.Axis(title="Restaurants"),
                    scale=alt.Scale(domain=(0,maxCount))),
                  alt.Y('name:O', axis=alt.Axis(title="cuisine"),
                    sort=alt.SortField(field="num", op="argmax")),
                  alt.ColorValue("LightGrey", condition=color_condition),
              ).properties(
                selection = highlight_selection,
              )


def loadData():
    import urllib.request, json
    with urllib.request.urlopen("https://raw.githubusercontent.com/yixuantang/Visualization_JS/master/Homework3/Data/nyc_restaurants_by_cuisine.json") as url:
        cuisines = json.loads(url.read().decode())

    tmp_list = []
    tmp_dict = {}
    for one in cuisines:
        tmp_dict['name'] = one['cuisine']
        for zipcode,num in one['perZip'].items():
            tmp_dict['zipcode'] = zipcode
            tmp_dict['num'] = num
            tmp_list.append(tmp_dict.copy())

    df = pd.DataFrame(tmp_list)
    return df

