import multiprocessing

from db.preDb import preDb


def get_clicltime(click_time):
    hour = int((click_time % 10000) / 100)
    minute = click_time % 100
    return hour * 60 + minute


def time_to_minute(time):
    if time == 0:
        return 0
    minute = time % 100
    hour = int((time % 10000) / 100)
    day = int(time / 10000)
    return day * 1440 + hour * 60 + minute


def format(field, index, value):
    string = ''
    if index == -1:
        string = ' ' + str(field) + ':' + str(field) + ':' + str(value)
    else:
        string = ' ' + str(field) + ':' + str(field) + \
            str(index) + ':' + str(value)
    return string


def creat_a_ffm_file(index, num, data_type, dir_path):
    file_path = dir_path + data_type + str(index) + '_' + str(index + num)
    print(file_path + ' start')
    pre_db = preDb()
    instances = []
    if data_type == 'train':
        instances = pre_db.db.train.find().limit(num).skip(index)
    else:
        instances = pre_db.db.test.find().limit(num).skip(index)

    file = open(file_path, 'w')
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
            "positionID":
            instance['positionID']
        })
        if position is None:
            line += '\n error:position is none'
            break

        app_category = pre_db.db.app_categories.find_one({
            "appID": ad["appID"]
        })
        if app_category is None:
            line += '\n error:app_category is none'
            break

# and int(instance["conversionTime"] / 10000) == int(instance["clickTime"]
# / 10000)
        if instance['label'] == 1:
            line += str(1)
        else:
            line += str(0)
        field = 10
        line += format(field, -1, get_clicltime(instance['clickTime']) / 1440)
        field += 1
        line += format(field, instance['creativeID'], 1)
        field += 1
        line += format(field, ad['adID'], 1)
        field += 1
        line += format(field, ad['camgaignID'], 1)
        field += 1
        line += format(field, ad['advertiserID'], 1)
        # field += 1
        # line += format(field, ad['appID'], 1)

        field += 1
        index = app_category['appCategory']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field += 1
        index = ad['appPlatform']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        # line += ' ' + str(17) + ':' + str(user['userID']) + ':' + str(1)
        field += 1
        line += format(field, -1, user['age'] / 80)

        field += 1
        index = user['gender']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field += 1
        index = user['education']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field += 1
        index = user['marriageStatus']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field += 1
        index = user['haveBaby']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field += 1
        index = user['hometown']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field += 1
        index = user['residence']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        field += 1
        line += format(field, position['positionID'], 1)
        field += 1
        line += format(field, position['sitesetID'], 1)
        field += 1
        line += format(field, position['positionType'], 1)

        field += 1
        index = instance['connectionType']
        value = 0 if index == 0 else 1
        line += format(field, index, value)
        field += 1
        index = instance['telecomsOperator']
        value = 0 if index == 0 else 1
        line += format(field, index, value)

        appCategory = pre_db.get_user_installedappsCategory(
            instance["userID"])
        appCategory_list = appCategory["appsCategory"]
        install_app_num = appCategory["appNum"]
        field += 1
        for i in range(len(pre_db.app_categories)):
            line += format(field,
                           pre_db.app_categories[i], appCategory_list[i])

        field += 1
        for i in range(len(pre_db.app_categories)):
            value = appCategory_list[
                i] * install_app_num / pre_db.install_app_max_num[i]
            if value > 1:
                value = 1
            line += format(field, pre_db.app_categories[i], value)

        app_actions = pre_db.get_user_app_actions(instance["userID"],
                                                  instance["clickTime"])
        app_actions_category_list = app_actions["appsCategory"]
        field += 1
        for i in range(len(pre_db.app_categories)):
            line += format(field, pre_db.app_categories[i],
                           app_actions_category_list[i])
        app_actions_category_time = app_actions[
            "app_actions_category_final_time"]
        field += 1
        for i in range(len(pre_db.app_categories)):
            line += format(
                field, pre_db.app_categories[i],
                time_to_minute(app_actions_category_time[i]) / 44640)

        line += '\n'
        file.write(line)
    file.close()
    print(file_path + ' end')


class CreateFfmFile(object):
    """docstring for CreateFfmFile"""

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def create_ffm_file(self, train_data, test_data):
        train_dir_path = self.dir_path + 'train_ffm_data/'
        test_dir_path = self.dir_path + 'test_ffm_data/'

        p = multiprocessing.Pool()
        if train_data:
            train_data_num = self.get_train_instance_len()
            train_num = int(train_data_num / 1000) + 1
            index = 0
            while index < train_data_num:
                if (index + train_num) > train_data_num:
                    p.apply_async(
                        creat_a_ffm_file,
                        args=(index, train_data_num - index, 'train',
                              train_dir_path))
                    break
                p.apply_async(
                    creat_a_ffm_file,
                    args=(index, train_num, 'train', train_dir_path))
                index += train_num
                pass
        if test_data:
            test_data_num = self.get_test_instance_len()
            p.apply_async(
                creat_a_ffm_file, args=(0, 100000, 'test', test_dir_path))
            p.apply_async(
                creat_a_ffm_file, args=(100000, 100000, 'test', test_dir_path))
            p.apply_async(
                creat_a_ffm_file,
                args=(200000, test_data_num, 'test', test_dir_path))

        p.close()
        p.join()

        return [train_dir_path, test_dir_path]

    def get_train_instance_len(self):
        pre_db = preDb()
        return pre_db.db.train.count()

    def get_test_instance_len(self):
        pre_db = preDb()
        return pre_db.db.test.count()
