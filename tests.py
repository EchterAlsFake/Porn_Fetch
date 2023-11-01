from phub import Client

user = "layla" # random name, just ignore
pornstar = "mia"

user_object = Client().search_user(user)
pornstar_object = Client().search_pornstar(pornstar)

for user_x in pornstar_object:
    print(user_x)
