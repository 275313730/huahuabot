# coding: UTF-8

from os import mkdir, path, walk

import PIL.Image as Image
import demjson3
import requests
from lxml import etree


def get_pic(pic_url, pic_path):
    response = s.get(pic_url)
    with open(pic_path, 'wb') as fp:
        fp.write(response.content)


def download_pics():
    if not path.exists('./pic'):
        mkdir('./pic')

    avatar_url = 'https://ssr.res.netease.com/pc/zt/20191112204330/data/shishen_avatar/'
    card_url = 'https://ssr.res.netease.com/pc/zt/20191112204330/data/card/'
    dir_dict = {}

    resp_html = s.get('https://ssr.163.com/cardmaker/').text
    js_url = etree.HTML(resp_html).xpath('/html/body/script[5]/@src')[0]

    response = s.get(js_url)
    start_subscript = response.text.find('),d=[') + 4
    end_subscript = response.text.find(';function u(e')
    data = response.text[start_subscript:end_subscript]
    data_json = demjson3.decode(data)  # 使用demjson库解析不正常json数据
    for v in data_json:
        card_id = str(v['id'])
        card_name = v['name']
        card_role = int(v['role'])  # 没有办法，role有int有string，得多处理一步
        card_type = v['type']

        # 为了炭治郎，我还得特意处理斜杠，平安京数值怪天天恶心我就算了，写个代码还恶心我。
        card_name = card_name.replace('/', '-')

        print('正在爬取: {}-{}'.format(card_id, card_name))

        # 如果是式神，创建文件夹存放此式神头像和所有卡牌
        if card_type == '式神':
            if not path.exists('./pic/' + card_name):
                mkdir('./pic/' + card_name)

            dir_dict[card_role] = card_name
            pic_path = './pic/{}/avatar.png'.format(dir_dict[card_role])
            get_pic(avatar_url + card_id + '.png', pic_path)

        pic_path = './pic/{}/{}.png'.format(dir_dict[card_role], card_name)
        get_pic(card_url + card_id + '.png', pic_path)


def combine_pics():
    for root, dirs, files in walk("./pic"):
        for _dir in dirs:
            COL = 4  # 指定拼接图片的列数
            ROW = 2  # 指定拼接图片的行数
            UNIT_HEIGHT_SIZE = 546  # 图片高度
            UNIT_WIDTH_SIZE = 307  # 图片宽度
            PATH = "./pic/" + _dir + "/"  # 需要拼接的图片所在的路径
            NAME = "combine"  # 拼接出的图片保存的名字
            SAVE_QUALITY = 100  # 保存的图片的质量 可选0-100

            # 进行图片的复制拼接
            def concat_images(image_names, name, _path):
                image_files = []
                for index in range(COL * ROW):
                    image_files.append(Image.open(_path + image_names[index]))  # 读取所有用于拼接的图片
                target = Image.new('RGBA', (UNIT_WIDTH_SIZE * COL, UNIT_HEIGHT_SIZE * ROW))  # 创建成品图的画布
                # 第一个参数RGB表示创建RGB彩色图，第二个参数传入元组指定图片大小，第三个参数可指定颜色，默认为黑色
                for row in range(ROW):
                    for col in range(COL):
                        # 对图片进行逐行拼接
                        # paste方法第一个参数指定需要拼接的图片，第二个参数为二元元组（指定复制位置的左上角坐标）
                        # 或四元元组（指定复制位置的左上角和右下角坐标）
                        target.paste(image_files[COL * row + col],
                                     (0 + UNIT_WIDTH_SIZE * col, 0 + UNIT_HEIGHT_SIZE * row))
                target.save(f"{_path}{name}.png", quality=SAVE_QUALITY)  # 成品图保存

            # 获取需要拼接图片的名称
            def get_image_names(role_name, _path):
                image_names = list(walk(_path))[0][2]  # 获取目标文件夹下的所有文件的文件名
                image_names.remove("avatar.png")
                image_names.remove(f"{role_name}.png")
                if 'combine.png' in image_names:
                    image_names.remove('combine.png')
                # 先用list将iterator转成list，再[0]取出里面的三元元组元素，再[2]取出元组中的由文件夹名组成的列表
                # 从所有文件中随机抽取需要数量的文件，可设置是否能重复抽取
                # random库中的choices函数用于可放回抽取，第一个参数指定用于抽取的对象，k参数指定抽取数量
                # sample函数用于不放回抽取，参数同上
                print(image_names)
                return image_names

            concat_images(get_image_names(_dir, PATH), NAME, PATH)


s = requests.session()
# download_pics()
combine_pics()
