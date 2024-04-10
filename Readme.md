# 香山微架构开放验证第一期：昆明湖BPU模块UT验证实战

本仓库为“香山微架构开放验证第一期：昆明湖BPU模块UT验证实战”的验证环境。该验证环境需要在linux系统下运行，它包含了如何生成带验证的Python DUT模块、验证示例、验证报告生成等模块。（待验证模块对应的香山仓库为：[github.com/OpenXiangShan/XiangShan](https://github.com/OpenXiangShan/XiangShan)，commit为：XXXX）

**本验证活动官方为：[www.openverify.cc](https://openverify.cc)**

**gitlink活动地址为：gitlink.com/xxx/xxx**


## 0x0、安装依赖

除去基本的gcc/python3开发环境外，本验仓库还依赖RTL仿真器 Verilator（4.218 ）、Picker工具、MLVP库。具体安装方法请参考以下链接。

1. [Verilator](https://www.veripool.org/projects/verilator/wiki/Installing)
2. [Picker](https://github.com/XS-MLVP/picker)
3. [mlvp](https://github.com/XS-MLVP/mlvp)

通过以下命令安装python依赖：
```bash
pip3 install XXXX XXXX XXXX
```

## 0x1、生成待验证模块

下载仓库

```bash
git clone https://github.com/XS-MLVP/env-xs-ov-00-bpu.git
cd env-xs-ov-00-bpu.git
```

### 生成 uFTB

```bash
make uftb TL=python
```

上述命令会在当前目录中生成out目录，其中 picker_out_uFTB 目录下的 UT_FauFTB 即为待验证的Python Module。可以在python环境中直接导入。因为待验证的python DUT与python版本相关，所以无法提供通用版本的python-dut，需要自行编译。

```bash
out
`-- picker_out_uFTB
    `-- UT_FauFTB
        |-- _UT_FauFTB.so
        |-- __init__.py
        |-- libDPIFauFTB.a
        |-- libUTFauFTB.so
        |-- libUT_FauFTB.py
        |-- uFTB.fst.hier
        `-- xspcomm
            |-- __init__.py
            |-- __pycache__
            |   |-- __init__.cpython-38.pyc
            |   `-- pyxspcomm.cpython-38.pyc
            |-- _pyxspcomm.so -> _pyxspcomm.so.0.0.1
            |-- _pyxspcomm.so.0.0.1
            |-- info.py
            `-- pyxspcomm.py

4 directories, 13 files
```

当导入模块UT_FauFTB后，可以在Python环境中进行简单测试。

```python
from UT_FauFTB import *

if __name__ == "__main__":
    # Create DUT
    uftb = DUTFauFTB()
    # Init DUT with clock pin name
    uftb.init_clock("clock")

    # Your testcases here
    # ...

    # Destroy DUT
    utb.finalize()
```

其他待验证模块，例如 TAGE-SC，FTB也可以通过类似命令生成。

### Tage SC

```bash
make tage_sc TL=python
```

### FTB

```bash
make ftb TL=python
```

**支持的模块名称有：uftb、tage_sc、ftb、ras。也可以通过如下命令，一次性生成所有DUT模块。**

```bash
make all TL=python
```

## 0x2、BPU外围环境

BPU是CPU中的一个模块，单独无法运行，为了对BPU中的子模块进行验证，本环境提供了其所需的外围环境来驱动BPU中的各个模块。

### Fake-FTQ

TBD

### 分支Trace

TBD


## 0x3、验证示例

本仓库基于uFTB模块提供了验证示例，其中包含了：如何编写测试用例、发送激励、定义功能覆盖率、生成测试报告等。

### 编写TestCase

TBD

#### 创建测试函数

本验证环境基于Pytest进行搭建，因此如何编写test请参考文档：XXXXX。在本示例中，编写了如下test：

```bash
xxxx/test_xxx.py
```

#### 发送激励

TDB

#### 运行测试

TBD

#### 生成测试报告

在运行

## 0x4、如何参与本活动

参与本验证活动，取得名次能够获得丰厚大奖，获得地址为：XXXX。

### 流程介绍

参与验证的流程如下图所示：

【图】

#### （0）报名

TBD

#### （1）资格认证

TBD

#### （2）fork 本仓库

TBD

#### （3）领取任务

TBD

#### （4）分解测试点

TBD

#### （5）编写测试用例

TBD

#### （6）编写测试代码&测试发现bug

TBD

#### （7）通过Issue和PR汇报bug获得积分

TBD

#### （8）编写测试文档

TBD

#### （9）提交测试文档获得最终积分

TBD
