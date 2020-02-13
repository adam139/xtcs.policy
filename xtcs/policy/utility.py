
def mergeDic(*diclist):
    result = {}
    for wedic in diclist:
        result.update(wedic)
    return result
 
def fetch_url_parameters(qstr):      
                
    if bool(qstr):
        qlist = qstr.split('&')
        diclist = map(lambda x:{x.split('=')[0]:x.split('=')[1]},qlist)
        qpt = mergeDic(*diclist)
        return qpt
    return {}
     