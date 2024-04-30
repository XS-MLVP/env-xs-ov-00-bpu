# BPU验证环境

本环境提供BPU验证所需的所有依赖，以及工具包。本验证环境需要在linux系统下运行，包含以下组件

1. 生成待验证的 Python DUT 模块
2. 对DUT进行验证的示例项目
3. 生成验证报告的组件

待验证项目：

- 待验证模块：[XiangShan ea2f767](https://github.com/OpenXiangShan/XiangShan/tree/ea2f767c24941b08d375b2b9529cd11b5850960a)


## 安装依赖

除去基本的gcc/python3开发环境外，本验仓库还依赖如下两个项目，请先行安装，**并安装对应项目的依赖**。

1. [Picker](https://github.com/XS-MLVP/picker)
2. [MLVP](https://github.com/XS-MLVP/mlvp)

再通过以下命令安装其他依赖：
```bash
apt install lcov # genhtml
pip install pytest-sugar pytest-rerunfailures pytest-xdist pytest-assume pytest-html # pytest

```

## 生成待验证模块

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

**支持的模块名称有：uftb、tage_sc、ftb、ras、ittage。也可以通过如下命令，一次性生成所有DUT模块。**

```bash
make all TL=python
```

## BPU外围环境

BPU是CPU中的一个模块，单独无法运行，为了对BPU中的子模块进行验证，本环境提供了其所需的外围环境来驱动BPU中的各个模块。

### 分支 Trace 工具：BRTParser

BRTParser 使我们专门为 BPU 验证所设计的能够自动抓取、解析程序指令流中的分支信息的工具，它基于香山前端的开发工具 `OracleBP`。 BRTParser 内部集成了 NEMU 模拟器，可以直接运行程序，并在其中抓取分支信息。BRTParser 会将抓取到的分支信息解析成一种通用的格式，方便后续的验证工作。

具体请参见 `utils` 目录下的 `BRTParser`。

### FTQ 运行环境

由于单独的子预测器模块并无法运行真实的程序，更无法验证其在实际程序中的预测准确率与功能正确性。因此，我们提供了一个简易的 FTQ 环境，该环境使用了 BRTParser 生成的分支信息来生成程序指令执行流。FTQ 将会解析预测器的预测结果，并与实际的分支信息进行比对，从而验证预测器的准确性。另外，FTQ 还会向 BPU 发出重定向信息与更新信息，使得预测器可以在 FTQ 的环境中不间断运行。

为了使一个子预测器能够正常工作，我们还模拟了 BPU 顶层模块，为子预测器提供时序控制等功能。对于非 FTB 类型的子预测器，我们还提供了一个简易的 FTB 实现，用于向子预测器结果中添加 FTB 基础预测结果信息。

目前，我们使用 FTQ 环境驱动了 uFTB 子预测器，并编写了时序精确的 uFTB 参考模型。FTQ 环境的具体实现和使用方法都可以在这个测试用例中获取，详见 `test_src/uFTB-with-ftq`。

## 验证示例

本仓库基于uFTB模块提供了验证示例，其中包含了：如何编写测试用例、发送激励、定义功能覆盖率、生成测试报告等。

### 编写TestCase



#### 创建测试函数

本验证环境基于Pytest进行搭建，因此如何编写test请参考[对应文档](https://open-verify.cc/mlvp/docs/quick-start/frameworks/pytest/)。

在本示例中，编写了如下test：

```bash

```

#### 发送激励



#### 运行测试



#### 生成测试报告


