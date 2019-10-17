## 检测CPU温度
```shell script
while true ; do vcgencmd measure_temp ; sleep 1 ; done
```


* 预设7个埋点，加上初始位置共8个点位
* 磁--0----1-------2-------3-------4-------5-------6-------7-------磁
---

设备初始位置 - cp1 >cp2>cp3>cp4>cp5>cp6>cp7 
* 程序启动，向右行驶5秒，离开磁体，再向左行驶直到接近磁体，再向右行驶到0号光电传感器挡板
* 想回到0号初始位置需要调用接口：http://192.168.1.13/init，和程序启动动作一样
* 后台暴露端口：
    * 左右移动
        * 向左 http://192.168.1.13/left
        * 向右 http://192.168.1.13/right
        * 急停 http://192.168.1.13/stop
        * 当抵达第一个或最后一个产品位置时（1/7），请求相同方向当接口时程序不会启动电机，并忽略本次请求
        * 急停按键用于解除继电器被占用状态或强制关闭继电器，按此按钮下一次运行方向必须是之前到相同方向，否则位置会-1，如果位置不一致调用强制指定位置接口：http://address/set/location/{Location number}
    * 移动到指定位置：
        * http://address/specified/{Location number}
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
