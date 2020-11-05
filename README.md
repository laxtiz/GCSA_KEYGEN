# 某个航线绘制程序的注册机

某程序以 GCSA_V1R0_{DATE} 命名，使用期为两个月，在此之后需要注册。

主程序使用Python 实现，并以PyInstaller 打包发布。

## 注册验证机制
**序列号明文**为本机C盘序列号。
**注册码明文**为序列号明文加上一段特殊字符串。
验证时，只要序列号和特殊字符串都在注册码内即可。
> 特殊字符串为：Buy272737

### 序列号明文
打开命令提示符，输入`vol C:`, 可查询本机C盘序列号
> 驱动器 C 中的卷没有标签。  
> 卷的序列号是 E442-438A

将四字节数据 0xE442438A 转为整数 `-465419638`，即为序列号明文。

### 注册码明文
连接**序列号明文**和**特殊字符串**，得到`-465419638buy272737`，即为**注册码明文**

### 加密机制
将明文字符串`plain_text`以*utf8*解码，获得字节数组`data`。
将`data`以*DES*加密，获得加密后的字节数组`result`。
将`result`通过*base64*编码，获得加密结果`cipher_text`。

解密机制以同样方式逆序即可。
> DES加密算法使用的**KEY**和**IV**均为：11272737

## Python 实现注册机
使用本程序需Python 运行环境

### 准备
1. 创建virtualenv 虚拟环境
    - for Linux:
        ```sh
        python -m venv venv
        source ./venv/bin/activate
        ```

    - for Windows:
        ```powershell
        py -m venv venv
        .\venv\Scripts\activate
        ```

2. 安装需求库
    ```sh
    python -m pip install --upgrade pip wheel setuptools
    python -m pip install -r requirements.txt
    ```

### 测试
测试案例使用Python 标准库 unittest
```sh
python -m unittest -v
```

### 运行
无参数运行返回本机序列号及注册码
> python keygen.py  
> 序列号：qoTGxmXtDFbR5AkUZ5ZL0Q==  
> 注册码：qoTGxmXtDFZPyRIBHmCyim/6UV/ypqcP

将序列号作为参数传递，返回对应的注册码
> pyhton keygen.py QBxOPKM8eFHhI4wO/tf2lQ==  
> 序列号：QBxOPKM8eFHhI4wO/tf2lQ==  
> 注册码：QBxOPKM8eFFXoB1YUvqsQquNWkRcgiGg