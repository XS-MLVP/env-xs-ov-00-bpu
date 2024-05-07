# uFTB-raw

## 介绍

本测试用例提供了基于模拟随机数据的香山处理器 uFTB 分支预测器的仿真验证环境，用于验证 uFTB 的缓存功能和预测功能。

为此，我们为 uFTB 提供了简易的 uFTB Wrapper，以向 uFTB 提供时序控制和输入输出处理。具体而言，我们提供了三种操作：

1. 生成数据队列：由于uFTB实际上可以被是为FTB表项的一个缓存，所以我们将传递的信息封装为 FTBEntry，以便于 uFTB 的使用。而 FTBEntry 本身是一组受约束的数据，因此只要随机数据符合结果即可。
2. 读取操作：uFTB 会根据传递的信息，从自身缓存的 FTB 表项中读取预测结果。因为我们的测试用例是随机生成的，所以我们不需要真实的预测结果，只需要保证 uFTB 的读取操作正确即可。
3. 更新操作：uFTB 会根据传递的信息，更新自身缓存的 FTB 表项。只要更新生效，即可认为 uFTB 的更新操作正确。

对读取和更新操作，我们将对Pin接口的操作封装为 `get_pred` 和 `set_update` 方法，以便于 uFTB 的使用。
同时对原始的 uFTB 模型进行了封装，由于存在很多重复的接口，我们使用 python 的元编程机制，将重复的接口合并，以减少对pin接口操作时的代码量。


## 快速使用

### 环境配置

**1. 安装 mlvp**

具体步骤参见 https://github.com/XS-MLVP/mlvp

**2. 编译 DUT**

在本仓库根目录下执行

```shell
make uftb TL=python
```

即可生成 DUT 编译结果，编译结果无需移动，程序会自动检索对应目录。

### 仿真验证

在 `tests` 目录下执行

```shell
make TEST=uFTB-raw run
```

即可开始仿真验证。

程序运行结束后，会生成对应的波形文件及覆盖率报告。波形文件位于 `tests/report/uFTB-raw` 目录下，覆盖率报告位于 `tests/report/uFTB-raw.html`。


## 使用说明

### 目录结构

```bash
uFTB-raw                    # 测试用例名称
|-- FTBEntry.py             # 针对 FTB 表项的封装
|-- FauFTB.py               # 针对 uFTB 的二次封装，将重复信号合并，并恢复信号结构体层次
|-- README.md               
`-- test_raw.py             # 测试入口，用于驱动随机数据生成、uFTB 操作
```
