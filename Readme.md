# The first phase of Open Verification for the Kunminghu microarchitecture of Xiangshan: Kunminghu's BPU Module UT Verification in Action.

[中文文档](/Readme_cn.md)

This project aims to explore open-sourced subdivision verification of the high-performance open-source RISC-V OpenXiangshan processor's microarchitecture. It introduces new tools and methods based on Python, enabling all students interested in chip design and verification to quickly grasp and study the XiangShan microarchitecture. This phase provides a detailed introduction to the principles and implementation of the branch prediction module of the XiangShan Kunminghu architecture, along with the corresponding open-source verification environment. Participants in this phase can earn points and rewards by submitting bugs, writing verification reports, and more.

**The Open-Verify Porject Official Website：[www.open-verify.cc](https://open-verify.cc)**

**Gitlink Event：[https://www.gitlink.org.cn/glcc/2023/subjects/detail/473](https://www.gitlink.org.cn/glcc/2023/subjects/detail/473)**


## Introduction

This project utilizes open-source tools for the open verification of open-source chips. The focus of the current phase is the BPU module within the XiangShan Kunminghu microarchitecture.

## Kunminghu microarchitecture

The Kunming Lake architecture is the third-generation high-performance microarchitecture of the XiangShan open-source processor. For the architecture diagram, please refer to the [Kunminghu architecture diagram](https://github.com/OpenXiangShan/XiangShan/raw/kunminghu/images/xs-arch-nanhu.svg).

## Chip verification

Chip validation is a crucial aspect of chip design work. Skipping or insufficient validation can result in chip fabrication failures or products not meeting standards, leading to significant losses. Chip design companies treat chip design as proprietary business secrets, and chip validation typically requires access to the chip design source code. Therefore, chip validation work can only be conducted internally within the company. However, with the open-source nature of the Shanhai high-performance RISC-V chip, concerns about "leaking proprietary secrets" do not arise. Consequently, chip validation work can be distributed in a manner similar to software subcontracting or crowdsourcing, allowing interested individuals to participate remotely.

## Related documents

1. [Basic Learning Materials](https://open-verify.cc/mlvp/docs/): Learn about chip validation and how to use Python for validation.

1. [Introduction to Shanhai BPU](https://open-verify.cc/xs-bpu/docs/): Learn about branch prediction and the basic predictors used in the Shanhai processor.

1. [How to Participate in This Activity](/doc/join_cn.md): Learn how to participate in this activity and the rules.

1. [Building Verification Environment](/doc/env_cn.md): Learn how to set up the basic verification environment, how to validate, and submit validation results.

## Repository Directory
The structure of this repository directory and corresponding explanations are as follows:

```bash
.
├── LICENSE          
├── Makefile         
├── Readme.md        
├── Readme_cn.md     
├── doc              
├── image            
├── mk               # Sub makefiles
├── out              # DUT output
└── src              # DUT source code
```

**Note: Since this project requires submitting results via PR, please make sure to organize the data according to the directory requirements mentioned above.**

## Discussion group

To prevent spam advertisements in the group, please run the following Python code to get the group number.

QQ group
```python
import base64
base64.b64decode('Your_Base64_Data_Here').decode()
```

Wechat group
```python
import base64
from io import BytesIO
from PIL import Image
base64_image_data = \
"Your_Base64_Image_Data_Here_0"\
"Your_Base64_Image_Data_Here_1"
image_data = base64.b64decode(base64_image_data)
image = Image.open(BytesIO(image_data))
image.show()
```
