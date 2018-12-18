import pymysql
import os
from definitions import *

def load_data():
    # 将CK+数据集中10000余张图片导入到MySQL数据库中
    db = pymysql.connect('localhost', 'root', '123456', 'train')
    cursor = db.cursor()
    for folder in os.listdir(CK_DIR):
        # 获取数据集文件夹中的所有主体文件夹
        dir2 = os.path.join(CK_DIR, folder)
        for folder2 in os.listdir(dir2):
            # 获取主体文件夹的所有表情序列文件夹
            if not str(folder2)[0] == '.':
                # 用.开头的为无效文件夹
                dir3 = os.path.join(dir2, folder2)
                images = os.listdir(dir3)
                # 获取该表情序列文件夹下的所有图片
                num = len(images)
                i = num - 1
                # 因为对于每个表情序列，只有其最后一张图片才有对应的标好的表情label
                # 所以这里反向遍历，先找到最后一张图片，从而找到标签后，再找其他图片
                while i != -1:
                    image = images[i]
                    # 获取一张图片
                    img_name = image[: -4]
                    # 截掉文件名中的不需要部分
                    if img_name[0] == '.':
                        # 无效图片
                        i -= 1
                        continue
                    print('NOW INSERTING', img_name)
                    subject, group, no = (j for j in img_name.split('_'))
                    img_dir = os.path.join(dir3, image)
                    # 获取图片的路径
                    if i == num - 1:
                        # 如果这是表情序列的最后一张图片，其带有表情标签，我们需要从另一个文件夹中找到它
                        label_dir = os.path.join(CK_LABEL_DIR, subject, group, subject
                                                + '_' + group + '_' + no + '_emotion.txt')
                        try:
                            with open(label_dir, 'r') as f:
                                ans = f.read().split('.')[0]
                                # 找到结果
                                sql = """
                                    INSERT INTO `groups` VALUES(%s, %s, %s, %s)
                                """ % (subject[1:], group, ans, num)
                                try:
                                    cursor.execute(sql)
                                    db.commit()
                                except Exception as e:
                                    print(e)
                                    db.rollback()
                        except:
                            # 未找到对应的标签文件
                            ans = '0'
                            # 表情记为0，即中立的编号
                            sql = """
                                INSERT INTO `groups` VALUES(%s, %s, %s, %s)
                            """ % (subject[1:], group, ans, num)
                            print(subject[1:], group, ans, num)
                            try:
                                cursor.execute(sql)
                                db.commit()
                            except Exception as e:
                                print(e)
                                db.rollback()

                    sql = """
                            INSERT INTO `imgs` VALUES(%s, %s, %s, "%s");
                            """ % (subject[1:], group, no, img_dir.replace('\\', '/'))
                    # 插入图片信息到数据库，因为数据库中会错误识别反斜杠，所以将其转换成正斜杠
                    print(subject[1:], group, no, img_dir.replace('\\', '/'))
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except Exception as e:
                        print(e)
                        db.rollback()
                    i -= 1
