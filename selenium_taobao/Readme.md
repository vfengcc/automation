python + selenium 模拟淘宝登录 并抓取指定关键词商品

环境： python 3.7 + selenium 3.141.0 + chromedriver.exe

主要实现：

    - 1. 实现cookie存储，启动后加载cookie并做校验。
    
    - 2. 实现滑动条类验证码，js打开新tab页，多tab页切换。
    
    - 3. 可以设定最大爬取的页数，可以设置多个关键词进行抓取。 

总结： 本实例内看起来比较繁琐，但是更贴近人为操作习惯，中间加有随机sleep时间间隔。

附： 
	- ChromeDriver下载链接：
		- 官网地址：https://sites.google.com/a/chromium.org/chromedriver/downloads
		- 淘宝镜像：http://npm.taobao.org/mirrors/chromedriver/