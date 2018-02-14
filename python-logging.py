#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 最简单的日志记录
import logging


logging.info("打印信息")
logging.error("出现了错误")
logging.warning("警告信息")
                            # 低于warning等级的info被忽略了

print '\n\n'

logger = logging.getLogger(__name__)
logger.basicConfig(level=logging.INFO)

logger.info("打印信息")
logger.error("出现了错误")
logger.warning("警告信息")
                            # 不低于INFO的信息全部显示了


print '\n\n'

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
logging.info("打印信息")
logging.error("出现了错误")
logging.warning("警告信息")
                            # 自定制格式的信息
