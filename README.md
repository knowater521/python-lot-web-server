## 检测CPU温度
```shell script
while true ; do vcgencmd measure_temp ; sleep 1 ; done
```


* 预设7个埋点，加上初始位置共8个点位
---

设备初始位置 - cp1 >cp2>cp3>cp4>cp5>cp6>cp7 
* 程序启动，向右行驶5秒，离开干簧管传感器，向左行驶15秒，期间抵达传感器位置时自动停止电机转动，15秒后开始注册光电传感器
* 后台暴露端口：
    * 左右移动
        * 向左 http://192.168.1.13/left
        * 向右 http://192.168.1.13/right
        * 急停 http://192.168.1.13/stop
        * 当抵达最后一个产品位置时，请求相同方向当接口时程序不会启动电机，并忽略本次请求
    * 移动到指定位置：
        *http://address/specified/{Location number}
        * 编号必须限制在1 - 7之间，其他数值程序将做忽略处理
        * 抵达指定位置后再做相同请求程序忽略执行该操作
    * 强制指定当前位置：
        * http://address/set/location/{Location number}
        * 用于存在误差时，将设备推到指定位置后手动设置当前位置，而不需要初始化位置
        * 编号必须限制在1 - 7之间，其他数值程序将做忽略处理
    * 设备初始化：
        * http://192.168.1.13/init
    * 设备关机
        * http://192.168.1.13/shutdown
        * 设备恢复到初始位置后关机
    * 当前位置
        * http://192.168.1.13/current/position
    
* 开机启动：
    * 文件路径：/home/pi/pythonproject/web-server/appRelay.py 
    * 程序启动命令：sudo python appRelay.py 
    * sudo nohup python /home/pi/pythonproject/web-server/appRelay.py &
    * ps aux | grep appRelay.py
    * kell 746
    
    
    

         
        
>0
>>1
>>>2
>>>>3
>>>>>4
>>>>>>5
>>>>>>>6
>>>>>>>>7
* 程序终止：卸载光电传感器，设备向左行驶到初始位置，若超时1分钟未抵达则强制终止程序
---
//TODO 设备急停物理按钮功能
