# -*- coding: utf-8 -*-
import json

res = '{"code":2000,"data":{"reservationItemVOS":[{"status":1,"reservationTime":1712798825860,"reservationId":19657314832,"itemPicUrl":"https://resource.moutai519.com.cn/mt-resource/static-union/170436846886fe18.png","itemName":"53%vol 500ml贵州茅台酒（甲辰龙年）","itemId":"10941","price":"2499","count":1,"sessionName":"","reserveStartTime":1712797200000,"shopId":"111110105010","orderEndTimeCountDown":73336765,"sessionType":1},{"status":1,"reservationTime":1712710853955,"reservationId":19646114304,"itemPicUrl":"https://resource.moutai519.com.cn/mt-resource/static-union/170436845942c00f.png","itemName":"53%vol 375ml×2贵州茅台酒（甲辰龙年）","itemId":"10942","price":"3599","count":1,"sessionName":"","reserveStartTime":1712710800000,"shopId":"211110105023","sessionType":1},{"status":1,"reservationTime":1712710842634,"reservationId":19645922451,"itemPicUrl":"https://resource.moutai519.com.cn/mt-resource/static-union/170436846886fe18.png","itemName":"53%vol 500ml贵州茅台酒（甲辰龙年）","itemId":"10941","price":"2499","count":1,"sessionName":"","reserveStartTime":1712710800000,"shopId":"110105061013","sessionType":1},{"status":1,"reservationTime":1712625675933,"reservationId":19635117925,"itemPicUrl":"https://resource.moutai519.com.cn/mt-resource/static-union/170436846886fe18.png","itemName":"53%vol 500ml贵州茅台酒（甲辰龙年）","itemId":"10941","price":"2499","count":1,"sessionName":"","reserveStartTime":1712624400000,"shopId":"111110105010","sessionType":1},{"status":1,"reservationTime":1712538029129,"reservationId":19615027771,"itemPicUrl":"https://resource.moutai519.com.cn/mt-resource/static-union/170436846886fe18.png","itemName":"53%vol 500ml贵州茅台酒（甲辰龙年）","itemId":"10941","price":"2499","count":1,"sessionName":"","reserveStartTime":1712538000000,"shopId":"211110105016","sessionType":1},{"status":1,"reservationTime":1712454321557,"reservationId":19609950466,"itemPicUrl":"https://resource.moutai519.com.cn/mt-resource/static-union/170436846886fe18.png","itemName":"53%vol 500ml贵州茅台酒（甲辰龙年）","itemId":"10941","price":"2499","count":1,"sessionName":"","reserveStartTime":1712451600000,"shopId":"211110101003","sessionType":1}],"hasMore":true,"validTime":1712842663224,"showAfterTime":1712678400000,"notOrderCount":0,"tips":"前往查看"}}'.encode('utf-8')
resJson = json.loads(res)
print(resJson)
lastResult = resJson["data"]["reservationItemVOS"][0]
print(lastResult)
itemName = lastResult["itemName"]
status = lastResult["status"]
if status == 2:
    print(f"{itemName} 申购成功")
else:
    print(f"{itemName} 申购失败")
