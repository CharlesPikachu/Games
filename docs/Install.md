# 安装CPGames


#### 环境配置

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+


#### Whl文件安装(推荐)

在终端运行如下命令即可(请保证python在环境变量中):

```sh
wget https://github.com/CharlesPikachu/Games/releases/download/v0.1.2/cpgames-0.1.2-py3-none-any.whl
pip install cpgames-0.1.2-py3-none-any.whl
```


#### PIP安装(推荐)

在终端运行如下命令即可(请保证python在环境变量中):

```sh
pip install cpgames --upgrade
```


#### 源代码安装

**1.在线安装**

运行如下命令即可在线安装:

```sh
pip install git+https://github.com/CharlesPikachu/Games.git@master
```

**2.离线安装**

利用如下命令下载Games源代码到本地:

```sh
git clone https://github.com/CharlesPikachu/Games.git
```

接着, 切到Games目录下:

```sh
cd Games
```

最后运行如下命令进行安装:

```sh
python setup.py install
```