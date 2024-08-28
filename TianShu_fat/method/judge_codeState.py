# -----------------------------------------------------------
#     author：wangshinan
#     description：判断响应结果code情况
#     param：responseText 响应结果
#     remarks：
# -----------------------------------------------------------

from method.out_log import logger

def judge_codeState(responseText):
    if '"code":4000' in responseText:
        logger.info("\033[1;35m'未登陆\033[0m")
    elif "err=4001" in responseText:
        logger.info("\033[1;35m'用户名不存在\033[0m")
    elif "err=4002" in responseText:
        logger.info("\033[1;35m'密码错误\033[0m")
    elif "err=4003" in responseText:
        logger.info("\033[1;35m'账号过期\033[0m")
    elif "err=4004" in responseText:
        logger.info("\033[1;35m'账号锁定\033[0m")
    elif "err=4005" in responseText:
        logger.info("\033[1;35m'账号禁用\033[0m")
    elif "err=4006" in responseText:
        logger.info("\033[1;35m'密码过期\033[0m")
    if '"code":-1' in responseText:
        logger.info("\033[1;35m'未知结果\033[0m")
    elif '"code":200' in responseText:
        logger.info("\033[1;35m'成功\033[0m")
    elif '"code":201' in responseText:
        logger.info("\033[1;35m'警告\033[0m")
    elif '"code":500' in responseText:
        logger.info("\033[1;35m'服务器出错\033[0m")
    elif '"code":1000' in responseText:
        logger.info("\033[1;35m'失败\033[0m")
    elif '"code":1010' in responseText:
        logger.info("\033[1;35m'参数错误\033[0m")
    elif '"code":1011' in responseText:
        logger.info("\033[1;35m'必要参数为空\033[0m")
    elif '"code":1100' in responseText:
        logger.info("\033[1;35m'csrf防护未通过\033[0m")
    elif '"code":4010' in responseText:
        logger.info("\033[1;35m'暂无权限\033[0m")
    elif '"code":4030' in responseText:
        logger.info("\033[1;35m'验证码过期\033[0m")
    elif '"code":4031' in responseText:
        logger.info("\033[1;35m'验证码错误\033[0m")
    elif '"code":4040' in responseText:
        logger.info("\033[1;35m'session过期\033[0m")
    elif '"code":4041' in responseText:
        logger.info("\033[1;35m'session失效\033[0m")
    elif '"code":4100' in responseText:
        logger.info("\033[1;35m'OAUTH认证出错\033[0m")
    elif '"code":4110' in responseText:
        logger.info("\033[1;35m'无效的ACCESS_TOKEN\033[0m")
    elif '"code":4111' in responseText:
        logger.info("\033[1;35m'无效的REFRESH_TOKEN\033[0m")
    else:
        pass
