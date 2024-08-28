#coding=utf-8

from config.ProjectInfo import txt_path
import ast


# -----------------------------------------------------------
#     author：wangshinan
#     description：API_将响应数据写入txt
#     param：1、text  写入的内容
#           2、txt_name 文件名
#     remarks：
# -----------------------------------------------------------

def write_txt_Response_data(text, txt_name):
    with open(txt_path + txt_name, "a+", encoding='UTF-8') as file:
        file.write(text + '\n')

# -----------------------------------------------------------
#     author：wangshinan
#     description：API_清空响应数据txt文件
#     param：1、txt_name 文件名
#     remarks：读取出格式：[{字典：第一行内容}，{字典：第二行内容}]
# -----------------------------------------------------------

def clean_txt_Response_data(txt_name):
    with open(txt_path + txt_name, "w") as file:
        file.seek(0)
        file.truncate()

# -----------------------------------------------------------
#     author：wangshinan
#     description：删除txt文件中的空白行，重新写入
#     param：1、text  写入的内容
#           2、txt_name 文件名
#     remarks：
# -----------------------------------------------------------

def delete_txt_BlankLine(text, txt_name):
    with open(txt_path + txt_name, "r") as f:
        res = f.readlines()  # res 为列表
        res = [x for x in res if x.split()]  # 将空行从 res 中去掉

    with open(txt_path + txt_name, "w") as f:
        f.write("".join(res))  # 将 res 转换为 字符串重写写入到文本


# -----------------------------------------------------------
#     author：wangshinan
#     description：API_读取响应数据txt文件(获取响应文本中的data数据——设备模板信息）
#     param：1、txt_name 文件名
#     remarks：读取出格式：[{设备模板1信息},{设备模板2信息}]
#               [{'address': '东城区得丰东巷65号', 'area': '东城区', 'city': '北京', 'classIficationId': '', 'classIficationName': '', 'copyDeviceId': 'OB47xdXY', 'copyDeviceName': '节能灯', 'country': '', 'createTime': '2019-11-11 12:59:36', 'deviceBrand': '美的', 'deviceDescription': '无', 'deviceModel': 'MD001', 'deviceName': '节能灯', 'deviceNo': '001', 'deviceProtocol': '1', 'deviceSub': '', 'deviceSubId': '', 'id': 'OB47xdXY', 'imgId': '4b629c87-28fd-4673-8fe6-60d03b287399', 'isTemplate': '1', 'location': '116.408644,39.901847', 'managerId': '', 'managerName': '', 'managerTelNo': '', 'parentDevice': '', 'parentDeviceId': '', 'province': '北京市', 'remark': '', 'state': '0', 'tagJson': '', 'tagJsonName': ''}, {'address': '东城区得丰东巷65号', 'area': '东城区', 'city': '北京', 'classIficationId': '', 'classIficationName': '', 'copyDeviceId': 'OFZdpSjL', 'copyDeviceName': '空调', 'country': '', 'createTime': '2019-11-11 12:59:29', 'deviceBrand': '美的', 'deviceDescription': '无', 'deviceModel': 'MD001', 'deviceName': '空调', 'deviceNo': '001', 'deviceProtocol': '1', 'deviceSub': '', 'deviceSubId': '', 'id': 'OFZdpSjL', 'imgId': '', 'isTemplate': '1', 'location': '116.408644,39.901847', 'managerId': '', 'managerName': '', 'managerTelNo': '', 'parentDevice': '', 'parentDeviceId': '', 'province': '北京市', 'remark': '', 'state': '0', 'tagJson': '', 'tagJsonName': ''},
#               {'address': '东城区得丰东巷65号', 'area': '东城区', 'city': '北京', 'classIficationId': '', 'classIficationName': '', 'copyDeviceId': 'C32XWruu', 'copyDeviceName': '复制模板_空调', 'country': '', 'createTime': '2019-11-11 12:59:29', 'deviceBrand': '美的', 'deviceDescription': '无', 'deviceModel': 'MD001', 'deviceName': '复制模板_空调', 'deviceNo': '001', 'deviceProtocol': '1', 'deviceSub': '', 'deviceSubId': '', 'id': 'C32XWruu', 'imgId': '', 'isTemplate': '1', 'location': '116.408644,39.901847', 'managerId': '', 'managerName': '', 'managerTelNo': '', 'parentDevice': '', 'parentDeviceId': '', 'province': '北京市', 'remark': '', 'state': '0', 'tagJson': '', 'tagJsonName': ''}] -----------------------------------------------------------
# -----------------------------------------------------------

def read_txt_Response_data(txt_name):
    list = []
    with open(txt_path + txt_name, "r", encoding='UTF-8') as file:
        Response_data = file.read().splitlines()
        for i in Response_data:
            w = ast.literal_eval(i)
            list.append(w)
    return list

