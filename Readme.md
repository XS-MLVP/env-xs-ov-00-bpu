# XiangShan Open Verify Class-00-BPU

This is the first class of XiangShan Open Verify. In this class, we will verify the BPU of XiangShan.  
The repository is used to build the verification environment and testcases for the BPU.

## Environment

Install the following tools before running the testcases.

1. [Verilator](https://www.veripool.org/projects/verilator/wiki/Installing)
2. [Picker](https://github.com/XS-MLVP/picker)

## Build

### uFTB

```bash
make uftb LANG=python
```

Then you will see the following files in the `out` directory. The whole directory is the python module of uFTB of XiangShan.  

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
The `UT_FauFTB` is the python module of uFTB of XiangShan which can be imported in the testcases. For example, you can import the module by the following code when your python file is in the `picker_out_uFTB` directory.

```python
from UT_FauFTB import *

if __name__ == "__main__":
    uFTB = DUTFauFTB()
    dut.init_clock("clk")

    # Your testcases here

    uFTB.finalize()
```

The other modules such as Tage_SC are similar to uFTB. You can import them in the same way.

### Tage SC

```bash
make tage_sc LANG=python
```

### FTB

```bash
make ftb LANG=python
```