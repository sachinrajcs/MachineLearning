import zomatopy as zt
import json
import pandas as pd
from send_mail import send_mail
import pandas as pd


def resturant_dict(location,cuisine):
    config={ "user_key":"277e7408d760dec40abe91c1e9686569"}
    zomato = zt.initialize_app(config)
    location_detail=zomato.get_location(location, 1)
    d1 = json.loads(location_detail)
    lat=d1["location_suggestions"][0]["latitude"]
    lon=d1["location_suggestions"][0]["longitude"]
    cuisines_dict={'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85,'american':1,'mexican':73}
    results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)),limit=100)
    d = json.loads(results)
    return(d)  

def resturants(resturant_list,top_5_10,price_preference):
    filtered_resturants = {'Resturant_Name':[],'Location_Address':[],'User_Rating':[],'Average_Cost':[]}
    for resturant in resturant_list:
        if(price_preference=="low"):
            if(resturant['restaurant']['average_cost_for_two']<300):
                filtered_resturants['Resturant_Name'].append(resturant['restaurant']['name'])
                filtered_resturants['Location_Address'].append(resturant['restaurant']['location']['address'])
                filtered_resturants['User_Rating'].append(resturant['restaurant']['user_rating']['aggregate_rating'])
                filtered_resturants['Average_Cost'].append(resturant['restaurant']['average_cost_for_two'])
        elif(price_preference=="mid"):
            if(300>=resturant['restaurant']['average_cost_for_two']<=700):
                filtered_resturants['Resturant_Name'].append(resturant['restaurant']['name'])
                filtered_resturants['Location_Address'].append(resturant['restaurant']['location']['address'])
                filtered_resturants['User_Rating'].append(resturant['restaurant']['user_rating']['aggregate_rating'])
                filtered_resturants['Average_Cost'].append(resturant['restaurant']['average_cost_for_two'])
        elif(price_preference=="high"):
            if(resturant['restaurant']['average_cost_for_two']>700):
                filtered_resturants['Resturant_Name'].append(resturant['restaurant']['name'])
                filtered_resturants['Location_Address'].append(resturant['restaurant']['location']['address'])
                filtered_resturants['User_Rating'].append(resturant['restaurant']['user_rating']['aggregate_rating'])
                filtered_resturants['Average_Cost'].append(resturant['restaurant']['average_cost_for_two'])
    
    df = pd.DataFrame(filtered_resturants).sort_values(by='User_Rating',ascending=False).head(top_5_10)
    df.reset_index(inplace=True)
    df.drop('index',axis=1,inplace=True)
    df['bot_response'] = df.Resturant_Name+' in '+df.Location_Address+' has been rated '+df.User_Rating 
    return(df)