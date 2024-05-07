# 香山微架构开放验证第一期：昆明湖BPU模块UT验证实战

**[English Readme](/Readme.md)**


本项目的目标是对高性能开源RISC-V香山处理器的微架构进行开放式分包验证的探索。它提供了基于Python的新工具、新方法，让所有对芯片设计与验证感兴趣的同学能够快速了解香山微架构，学习香山微架构。本期活动对香山昆明湖架构的分支预测模块的原理以及实现进行了详细介绍，并提供了对应的开源验证环境。参本次活动的同学，通过提交Bug、编写验证报告等获取积分与奖励。


**开源开放验证官网：[open-verify.cc](https://open-verify.cc)**


## 简介

本项目是基于开源工具对开源芯片进行的开源开放验证。本期验证的对象是香山昆明湖微架构中的BPU模块。

### 昆明湖微架构

昆明湖架构是香山开源处理器的第三代高性能微架构，架构图请参考：[昆明湖架构图](https://github.com/OpenXiangShan/XiangShan/raw/kunminghu/images/xs-arch-nanhu.svg)。

### 芯片验证

芯片验证是芯片设计工作中的重点，跳过验证或者验证的不够，会导致流片失败或者芯片产品不达标，带来巨大损失。芯片设计公司把芯片设计当成核心商业机密，而芯片验证通常需要基于芯片设计源代码，因此芯片验证工作只能在公司内部进行。开源香山高性能risc-v芯片不存在“商业机密泄露”等问题，因此可以把芯片验证工作以类似软件分包、众包的方式进行分发，让感兴趣的人远程参与。

## 学习材料

1. **[基础学习材料](https://open-verify.cc/mlvp/docs/)**，学习什么是芯片验证，如何使用Python进行验证。
1. **[香山BPU介绍](https://open-verify.cc/xs-bpu/docs/)**，学习什么是分支预测，香山处理器中采用了哪些基础预测器。
1. **[如何参与本活动](/doc/join_cn.md)**，介绍如何参与本活动，有哪些活动规则。
1. **[构建验证环境](/doc/env_cn.md)**，介绍基本验证环境搭建，如何进行验证和提交验证结果。


## 本仓库目录

本仓库目录结构和对应说明如下：

```bash
.
├── doc              # 仓库文档
├── image            # 文档图片
├── LICENSE          # 开源协议
├── Makefile         # Makefile
├── mk               # 子 Makefile
├── Readme_cn.md     # 中文 Readme
├── Readme.md        # 英文 Readme
├── tests            # 测试用例    <- 在此目录添加测试用例
│   ├── Makefile        # 测试用例 Makefile
│   ├── conftest.py     # 测试用例配置
│   ├── README.md       # 测试用例说明
│   ├── uFTB_raw        # 测试用例1：uFTB_raw
│   └── uftb-with-ftq   # 测试用例2：uftb-with-ftq
└── utils            # 实用工具
    ├── BRTParser       # 分支预测结果解析工具
    └── ready-to-run    # 可供在模拟器中执行的程序
```

**注：由于本项目是以PR的方式提交结果，所以请务必按照上述目录要求进行数据组织**

## 报名链接

请访问以下链接报名参与本活动：

[报名问卷](https://iz9a87wn37.feishu.cn/share/base/form/shrcnwpiyWaVUzyo47QdPBGy5Yd)

## 加入讨QQ论群: 600480230

<image src="/.github/image/600480230.jpg" alter="600480230" width=500px />
