![fastapi - 0.68.1](https://img.shields.io/static/v1?label=fastapi&message=0.68.1&color=success&logo=fastapi)


### 个人学习使用，写的烂勿喷

功能：

- [x] 基础API功能(私库&中转库)
- [x] 循环4小时检索一次入库状态，超过给定时间自动删除记录(私库&中转库)
- [x] 每4小时存档json文件一次，同步到Github仓库(私库)
- [x] 内置入库识别，动态源的uid粉丝少于1万不再入库(私库)，动态源的uid粉丝少于2000不再入库(中转库)
- [x] 内置共享数据接口访问次数限制，每2秒150000次请求限制(中转库)
- [x] 多后端组网同步(中转库到私库交换数据)
- [x] 定时监控后端运行状况(外接脚本仓库没有) 

**为避免数据滥用，特使用junmo.ink网址代替IP在这里展示用法，并给所有接口加上了关键词和关键字校验，实际必须使用群公告里的IP不能用带junmo.ink的链接否则会重定向获取不到数据，关键词和端口号在群公告自取**

### 共享的私人数据规则是1万粉以上的每小时最新的150或50条数据(实际日常平均更新的只有50条左右，节日期间150条左右，自己选用)

### 截至12.06 18:00，上面私人库内保存2977条抽奖动态数据(都大于等于1万粉)，下面中转库内保存1962条抽奖动态数据(都大于等于2000粉)(11.14 00：30清空过数据库，所以没攒多少)。

**一个月大概万粉以上的有3000动态，2000粉以上的因为有删过库，未能统计准确**

共享数据2000粉丝过滤(实际日常平均更新的只有100条左右，节日期间更新量暴增，没有统计平均的意义) 

上传数据接口链接：http://junmo.ink:端口号/lottery/set_lottery_info/关键词  

共享数据接口链接：http://junmo.ink:端口号/lottery/get_lottery_info/关键词  

私人数据1万粉丝过滤：(实际日常平均更新的只有50条左右，节日期间150条左右，自己选用，只保存一个月)

返回50条数据接口链接：http://junmo.ink:端口号/lottery/get_info_screen_50/关键词 

返回150条数据接口链接：http://junmo.ink:端口号/lottery/get_info_screen_150/关键词  

数据通过中转服务器连接我的服务器，请勿滥用接口

使用该链接请对应脚本my_config.js内替换填写

```
        APIs: ["http://junmo.ink:端口号/lottery/get_lottery_info/关键词"],


        set_lottery_info_url: "http://junmo.ink:端口号/lottery/set_lottery_info/关键词",

```

### 私人数据和中转共享数据区别

私人数据是从我库内取的动态，共计150条或50条。

共享数据则是直接从中转服务器中取数据，共计150条。

前者包含我个人爬虫的数据，后者不包含我个人爬虫的数据，只是中转服务器中缓存的大家共享的数据。

前者也包含大家共享的数据，中转服务器会把所有收集到的数据再传到我服务器上，筛过再入库。

**简单的说，前者每日更新数据少，入库粉丝要求高，后者每日更新数据多，入库粉丝要求低。**

当然也可以混着用，接口来源可以不单一 (单号使用推荐，多号使用不推荐)

请对应脚本my_config.js内替换填写(150+50条)

```
        APIs: [
        "http://junmo.ink:端口号/lottery/get_lottery_info/关键词",
        "http://junmo.ink:端口号/lottery/get_info_screen_50/关键词"
        ],
```


### 新号推荐接口

只能运行一次！！！这个接口会返回所有历史数据！！！替代上面的共享数据接口链接后运行一次即可！！！

新号推荐接口链接：http://junmo.ink:端口号/lottery/get_all_lottery_info/关键字

使用该链接请对应脚本my_config.js内填写

```
        APIs: [
        "http://junmo.ink:端口号/lottery/get_all_lottery_info/关键字"
        ],
```

不要作死一直使用这个接口，不然你转几天都转不完的，只供新号使用一次补全之前的动态！！！新号跑完记得更换接口！！！

使用有风险，后果自负！！！

### API高级配置

两个API，一个链接私库，一个链接中转库，两个库的区别在上面有说明，这里只展示用法，和上面接口需要替换的东西一样

接口限制最大获取数量150(不含150，别填150)条最新数据，可自定义获取数量

接口提供是否为官方动态的自定义规则，

```
http://junmo.ink:端口号/lottery/get_private_info/关键字?official=是官方写true不是官方写false&limit=数量自填0~149之间的数

http://junmo.ink:端口号/lottery/get_transit_info/关键字?official=是官方写true不是官方写false&limit=数量自填0~149之间的数
```


# 免责声明

* 代码仅供学习，请下载后24小时内删除。
* 不可用于商业以及非法目的，使用本代码与相关接口产生的一切后果, 作者不承担任何责任。
* 使用方法自行摸索或群内提问，仓库不提供额外的解答服务。


## Special statement:

Any unlocking and decryption analysis scripts involved in the Script project released by this warehouse are only used for testing, learning and research, and are forbidden to be used for commercial purposes. Their legality, accuracy, completeness and effectiveness cannot be guaranteed. Please make your own judgment based on the situation. .

All resource files in this project are forbidden to be reproduced or published in any form by any official account or self-media.

This warehouse is not responsible for any script problems, including but not limited to any loss or damage caused by any script errors.

Any user who indirectly uses the script, including but not limited to establishing a VPS or disseminating it when certain actions violate national/regional laws or related regulations, this warehouse is not responsible for any privacy leakage or other consequences caused by this.

Do not use any content of the Script project for commercial or illegal purposes, otherwise you will be responsible for the consequences.

If any unit or individual believes that the script of the project may be suspected of infringing on their rights, they should promptly notify and provide proof of identity and ownership. We will delete the relevant script after receiving the certification document.

Anyone who views this item in any way or directly or indirectly uses any script of the Script item should read this statement carefully. This warehouse reserves the right to change or supplement this disclaimer at any time. Once you have used and copied any relevant scripts or rules of the Script project, you are deemed to have accepted this disclaimer.



