import time,os
from config import ProjectInfo
from logging import getLogger,INFO,FileHandler,StreamHandler,Formatter

def set_logging():
    if 'API' in ProjectInfo.testCase:
        log_name = '_API_TestLog'
    elif 'GUI' in ProjectInfo.testCase:
        log_name = '_GUI_TestLog'
    else:
        log_name = '_TestLog'
    t = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))+log_name

    # 创建logger对象，如果参数为空则返回root logger
    logger_name = getLogger()
    # 输出INFO及以上级别的信息
    logger_name.setLevel(level=INFO)

    fp = os.path.abspath(".") + "/outlog/"      #联调路径
    # fp = ProjectInfo.outLogPath  #单调路径
    # 获取文件处理器、流处理器
    #将日志消息发送到磁盘文件，默认情况下文件大小会无限增长
    handler = FileHandler(fp + t + ".log", encoding="utf-8")
    console = StreamHandler()


    #设置输出日志格式:Formater对象用于配置日志信息的最终顺序、结构和内容。
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 为handler指定输出格式
    handler.setFormatter(formatter)
    console.setFormatter(formatter)
    #设置日志级别
    handler.setLevel(INFO)
    console.setLevel(INFO)

    # 为logger_name添加的日志处理器
    logger_name.addHandler(handler)
    logger_name.addHandler(console)

    return logger_name

logger = set_logging()


if __name__ == "__main__":
    logger.info("out log testing!")
    logger.warning("out log testing!")
    logger.debug("out log testing!")

