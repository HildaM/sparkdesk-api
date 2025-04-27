# sparkdesk-api 讯飞星火大模型api
> 如果该项目对你有帮助，不要忘记给我点个 star，或者 [赞助](https://github.com/HildaM/sparkdesk-api#-%E8%B5%9E%E5%8A%A9) 我一杯蜜雪冰城喔~
## 使用方法
```shell
pip install sparkdesk-api==1.6.1
```
或者
```shell
pip install sparkdesk-api==1.6.1 -i https://pypi.org/simple
```

### 1. Web模式
Web模式下，需要前往讯飞星火大模型web端通过 F12 抓取 3 个参数：cookie、fd、GtToken
- [获取参数的方法](https://github.com/HildaM/sparkdesk-api/tree/main/docs)

#### 命令行操作
```shell
python sparkdesk_web_cli.py
```

#### api调用
- chat()：一次询问
- chat_stream()：连续询问，相当于命令行模式
```python
from sparkdesk_web.core import SparkWeb

sparkWeb = SparkWeb(
     cookie=cookie,
     fd=fd,
     GtToken=GtToken
 )

 # single chat
 print(sparkWeb.chat("repeat: hello world"))
 # continue chat
 sparkWeb.chat_stream()
```

### 2. API模式
支持v4.0、v3.5、v3.0、v2.0、v1.0 四个版本 以及 [助手API](https://xinghuo.xfyun.cn/botcenter/createbot)，默认接口版本为3.5
- 默认api接口版本为3.5，配置其他版本需要指定Version参数（3.1或者2.1或者1.1）

讯飞星火的API需要前往官网进行申请。
你可以先创建一个服务，然后在该服务的控制台页面左边的：“星火认知大模型”栏目，进入“合作咨询”页面进行申请。
一般使用公司邮箱申请速度快。

该模式需要 3 个参数：app_id、api_key、api_secret
```python
from sparkdesk_api.core import SparkAPI
# 默认api接口版本为3.1，配置其他版本需要指定Version参数（2.1或者1.1）
sparkAPI = SparkAPI(
    app_id=app_id,
    api_secret=api_secret,
    api_key=api_key,
    # version=2.1,
    # assistant_id="xyzspsb4i5s7_v1"
)
sparkAPI.chat_stream()
```

具体调用方法与相关调用函数与 Web 模式一致。

# 🙏 赞助
如果项目对您有帮助，可以赞助我一杯蜜雪冰城哦~
<div>
  <img src="docs/赞助.jpg" style="width: 300px;">
</div>

# 🤝贡献

## 🎉鸣谢

感谢以下开发者对该项目做出的贡献：

<a href="https://github.com/HildaM/sparkdesk-api/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HildaM/sparkdesk-api" />
</a>
