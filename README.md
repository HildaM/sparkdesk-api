# sparkdesk-api 讯飞星火大模型api
> 如果该项目对你有帮助，不要忘记给我点个 star 哦！
## 使用方法
```shell
pip install sparkdesk-api==1.0.1
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
讯飞星火的API需要前往官网进行申请。
你可以先创建一个服务，然后在该服务的控制台页面左边的：“星火认知大模型”栏目，进入“合作咨询”页面进行申请。
一般使用公司邮箱申请速度快。

该模式需要 3 个参数：app_id、api_key、api_secret

具体调用方法与相关调用函数与 Web 模式一致。
