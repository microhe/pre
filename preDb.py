import pymongo

class preDb(object):

    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.db = client.pre
        
        self.app_categories = []
        self.calc_app_categories()
    
    def calc_app_categories(self):
        app_categories = []
        for line in self.db.app_categories.find():
            if not line["appCategory"] in app_categories:
                app_categories.append(line["appCategory"])
        self.app_categories = app_categories.copy()
        print(self.app_categories)

    def set_user_installedappsCategory(self,user_id):
        installed_app_list = []
        for line in self.db.user_installedapps.find({"userID":user_id}):
            installed_app_list.append(line['appID'])

        app_category_id_dict = {}
        for app_id in installed_app_list:
            app_category_id = self.db.app_categories.find({"appID":app_id})[0]['appCategory']
            if app_category_id in app_category_id_dict:
                app_category_id_dict[app_category_id] += 1
            else:
                app_category_id_dict[app_category_id] = 1
            
        for category_id in self.app_categories:
            if category_id in app_category_id_dict:
                app_category_id_dict[category_id] /= len(installed_app_list)
            else:
                app_category_id_dict[category_id] = 0
    
        print(app_category_id_dict)



    def get_a_train_instance(self,index):
        
        instance = self.db.train.find().limit(1).skip(index)[0]
        print(str(instance))
        ad = self.db.ad.find({"creativeID":instance["creativeID"]})[0]
        instance["adID"] = ad["adID"]
        instance["camgaignID"] = ad["camgaignID"]
        instance["advertiserID"] = ad["advertiserID"]
        instance["appID"] = ad["appID"]
        instance["appPlatform"] = ad["appPlatform"]

        user = self.db.user.find({"userID":instance['userID']})[0]
        instance["age"] = user["age"] 
        instance["gender"] = user["gender"] 
        instance["education"] = user["education"] 
        instance["marriageStatus"] = user["marriageStatus"] 
        instance["haveBaby"] = user["haveBaby"] 
        instance["hometown"] = user["hometown"] 
        instance["residence"] = user["residence"]
        
        position = self.db.position.find({"positionID":instance['positionID']})[0]
        instance["positionID"] = position["positionID"] 
        instance["sitesetID"] = position["sitesetID"] 
        instance["positionType"] = position["positionType"]

        installed_app_list = []
        for line in self.db.user_installedapps.find({"userID":instance['userID']}):
            installed_app_list.append(line['appID'])

        for app_id in installed_app_list:
            app_category = self.db.app_categories.find({"appID":app_id})[0]['appCategory']
            app_categories_id = 'installedAppCategory_' + str(app_category)
            if app_categories_id in instance:
                instance[app_categories_id] += 1
            else:
                instance[app_categories_id] = 1
        
        for app_category in self.app_categories:
            category_id = 'installedAppCategory_' + str(app_category)
            if category_id in instance:
                instance[category_id] /= len(installed_app_list)
            else:
                instance[category_id] = 0
        
        return instance

pre_db = preDb()
pre_db.set_user_installedappsCategory(2798058)
# print(pre_db.get_a_train_instance(0)
