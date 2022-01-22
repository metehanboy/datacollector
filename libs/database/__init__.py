class db_helper:

    def tip_belirle(self,tipsiz):
        if 'str' in str(type(tipsiz)).lower():
            return '\'' + str(tipsiz).replace("'", "''") + '\''
        elif 'timestamp' in str(type(tipsiz)):
            return '\'' + tipsiz.strftime("%Y-%m-%d %H:%M:%S") + '\''
        elif 'datetime' in str(type(tipsiz)):
            return '\'' + tipsiz.strftime("%Y-%m-%d %H:%M:%S") + '\''
        elif str(tipsiz) == 'None':
            return 'NULL'
        elif tipsiz != tipsiz:
            return 'NULL'
        else:
            return str(tipsiz)


    def chunker(self,lst,n=200):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]