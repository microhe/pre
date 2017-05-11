import multiprocessing

from db.preDb import preDb


def get_clicltime(click_time):
    hour = int((click_time % 10000) / 100)
    minute = click_time % 100
    return hour * 60 + minute


def format(field, index, value):
    string = ''
    if index == -1:
        string = ' ' + str(field) + ':' + str(field) + ':' + str(value)
    else:
        string = ' ' + str(field) + ':' + str(field) + \
            str(index) + ':' + str(value)
    return string


def creat_ffm_file(index, num):
    file_name = 'train_' + str(index) + '_' + str(index + num)
    print(file_name + ' start')
    file = open('~/train_ffm_data/' + file_name, 'w')
    pre_db = preDb()
    instances = pre_db.db.train.find().limit(num).skip(index)
    for instance in instances:
        line = ''
        ad = pre_db.db.ad.find_one({"creativeID": instance["creativeID"]})
        if ad is None:
            line += '\n error:ad is none'
            break

        user = pre_db.db.user.find_one({"userID": instance['userID']})
        if user is None:
            line += '\n error:user is none'
            break

        position = pre_db.db.position.find_one({
            "positionID": instance['positionID']
        })
        if position is None:
            line += '\n error:position is none'
            break

        app_category = pre_db.db.app_categories.find_one(
            {"appID": ad["appID"]})
        if app_category is None:
            line += '\n error:app_category is none'
            break

        if instance['label'] == 1 and instance["conversionTime"] / 10000 == instance["clickTime"] / 10000:
            line += str(1)
        else:
            line += str(0)

        line += format(30, -1, get_clicltime(instance['clickTime'] / 1440))
        line += format(10, instance['creativeID'], 1)
        line += format(11, ad['adID'], 1)
        line += format(12, ad['camgaignID'], 1)
        line += format(13, ad['advertiserID'], 1)
        line += format(14, ad['appID'], 1)

        field = 15
        index = app_category['appCategory']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field = 16
        index = ad['appPlatform']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        line += ' ' + str(17) + ':' + str(user['userID']) + ':' + str(1)
        line += format(18, -1, user['age'] / 80)

        field = 19
        index = user['gender']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field = 20
        index = user['education']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field = 21
        index = user['marriageStatus']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field = 22
        index = user['haveBaby']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field = 23
        index = user['hometown']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field = 24
        index = user['residence']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        line += format(25, position['positionID'], 1)
        line += format(26, position['sitesetID'], 1)
        line += format(27, position['positionType'], 1)

        field = 28
        index = instance['connectionType']
        value = 0 if index == 0 else 1
        line += format(field, index, value)
        field = 29
        index = instance['telecomsOperator']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        appCategory_list = pre_db.get_user_installedappsCategory(instance[
            "userID"])
        for i in range(len(pre_db.app_categories)):
            line += format(50, pre_db.app_categories[i], appCategory_list[i])

        line += '\n'
        file.write(line)
    file.close()
    print(file_name + ' end')



def get_train_instance_len():
    pre_db = preDb()
    return pre_db.db.train.count()



if __name__ == '__main__':
    # data_num = get_train_instance_len()
    data_num = 1000
    num = int(data_num / 20)

    p = multiprocessing.Pool()
    for i in range(20):
        p.apply_async(creat_ffm_file, args=(i * num, num))

    p.close()
    p.join()