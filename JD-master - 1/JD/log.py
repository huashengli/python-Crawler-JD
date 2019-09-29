import logging
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s [%(filename)s:%(lineo)d]'
                            '：%(message)s'
                            '- %(asctime)s',date='[%d/%b/%Y %H:%M:%s]',
                    )

logger=logging.getLogger(__name__)
if __name__=='__main__':
    logger.info("log") #括号里显示的想要看到的变量值
