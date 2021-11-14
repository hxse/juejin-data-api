# juejin-data-api
* 在项目根目录,新建配置文件,"config.json",在该位置写入token: {"token":"<your token>"}
* 参数类型
    ```
    name: str
    frequency: str
    count: int
    refresh: bool = True #是否使用缓存,如果缓存中没有数据则会默认请求新数据
    testUpdate: bool = False #是否分割成测试数据,False时,splitStart/splitEnd不生效
    splitStart: int = 0
    splitEnd: int = 0
    ```
* api举例
    * 返回10个数据
        * http://127.0.0.1:8000/ohlcv?name=SHFE.RB&frequency=60s&count=10&refresh=false&testUpdate=False&splitStart=5&splitEnd=10
    * 获取10个数据,返回其中的[5:10]个数据,用来做更新测试数据
        * testUpdate=True时splitStart/splitEnd生效
        * http://127.0.0.1:8000/ohlcv?name=SHFE.RB&frequency=60s&count=10&refresh=false&testUpdate=True&splitStart=5&splitEnd=10
