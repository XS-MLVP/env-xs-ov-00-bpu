## How to Participate in this Event

Participating in this verification event can earn you a chance to win generous prizes. [Registration Form](https://iz9a87wn37.feishu.cn/share/base/form/shrcnwpiyWaVUzyo47QdPBGy5Yd)

### Process Introduction

The process of participation is as shown below:

<img src="/.github/image/ov-pipline.svg" width="800px">

#### (0) Online Registration

There is no limit to the number of team members for this event. It can be one or more. The final prize will be distributed to the team leader according to the team's points. During the event, the team name and the name of the team leader will be made public in the group.

#### (1) Qualification Verification

In order to assess the capabilities of the participating teams, this event provides several DUTs with known bugs for the teams to perform verification tests. Teams that can find more than 80% of the bugs and can perform root cause analysis can qualify to participate. The number of bugs found will also become the corresponding team points.

#### (2) Fork Repository

Fork this repository, then set up the environment locally and participate in the testing tasks.

#### (3) Task Assignment

Tasks are described in the Issues of this repository. Team leaders sign up in the form of Issues under the Issues. The administrator will do the statistics, and then announce it in the group.

#### (4) Decompose Test Points & Write Verification Plan

Decomposing test points and verification plans are important steps in the chip verification process, which directly affect the verification results. At this stage, you need to submit the corresponding report through PR, and the organizer will review and score the report.

#### (5) Write Test Cases

Write test cases, the specific format can refer to the template in the [`tests`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fyaozhicheng%2Fworkspace%2Fenv-xs-ov-00-bpu%2Ftests%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/yaozhicheng/workspace/env-xs-ov-00-bpu/tests") directory. Test cases need to cover the corresponding test points.

#### (6) Write Test Code & Discover Bugs in Testing

During the testing process, after discovering a bug, you need to analyze the bug.

#### (7) Report Bugs through Issue and PR to Earn Points

You can submit bugs at any time through PR, but the organizer will only review bugs for a team once a day. The organizer will issue corresponding points based on the type and level of the bug.

#### (8) Write Test Report

Refer to the template [NutShell Cache](https://open-verify.cc/mlvp/docs/basic/report/) for writing.

#### (9) PPT Online Defense

Write PPT online for the defense of the entire verification task. The defense is organized centrally according to the completion situation of the team.

## Basic Tasks

### Task 1. uFTB & TFB

Source code address: [FauFTB.sv](https://github.com/XS-MLVP/env-xs-ov-00-bpu/tree/main/rtl/uFTB)
Function description document: [uFTB Branch Predictor](https://open-verify.cc/xs-bpu/en/docs/modules/01_uftb/)
Reference function point document: [uFTB Function List](https://open-verify.cc/xs-bpu/en/docs/feature/01_uftbfeature/)

Source code address: [FTB.sv](https://github.com/XS-MLVP/env-xs-ov-00-bpu/tree/main/rtl/FTB)
Function description document: [FTB Branch Predictor](https://open-verify.cc/xs-bpu/en/docs/modules/03_ftb/)
Reference function point document: [FTB Function List](https://open-verify.cc/xs-bpu/en/docs/feature/02_ftbfeature/)

1. Complete the code and document reading of the uFTB sub-predictor, understand the working principle and module functions of the uFTB. Clarify the structure of the FTB item cache used by the uFTB.
2. Based on the given reference function points, improve the function points that uFTB needs to verify, and decompose specific test points for these function points. At the same time, explain the significance of each test point to verify the function points.
3. Based on the decomposed test points, complete the test case writing for uFTB. Test cases need to cover all test points. At the same time, a detailed explanation of the test cases is required, including the purpose, input, output, expected results, and principles of the test cases.
4. Complete the code writing of the test cases for uFTB, it is recommended to complete **the writing of the reference model**. Ensure that the test cases can run through the verification environment. In the coding process, the quality of the code needs to be ensured, including the readability, maintainability, and scalability of the code.
5. Complete the running of the test cases for uFTB and generate a test report. The test report needs to include the running results of the test cases, code line coverage, function coverage, etc. The test report needs to be saved in the [`tests/report`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fyaozhicheng%2Fworkspace%2Fenv-xs-ov-00-bpu%2Ftests%2Freport%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/yaozhicheng/workspace/env-xs-ov-00-bpu/tests/report") directory, and you can open `tests/report/uFTB-yourId.html` in the browser to view the content of this test report.
6. Before the final submission, you need to check the test report to ensure that the test report meets the basic requirements for submitting PR.

### Task 2. TageSC

Source code address: [TageSC.sv](https://github.com/XS-MLVP/env-xs-ov-00-bpu/tree/main/rtl/TageSC)
Function description document: [TAGE-SC Branch Predictor](https://open-verify.cc/xs-bpu/en/docs/modules/02_tage_sc/)
Reference function point document: [TAGE-SC Function List](https://open-verify.cc/xs-bpu/en/docs/feature/03_tagescfeature/)

1. Complete the code and document reading of the TageSC sub-predictor, understand the working principles and functions of the Tage and SC single modules, and then understand the overall functions of the TageSC module. Clarify the structure of the Tage and SC table items used, and the working principle of branch folding history.
2. Based on the given reference function points, improve the function points that Tage, SC, TageSC need to verify, and decompose specific test points for these function points. At the same time, explain the significance of each test point to verify the function points.
3. Based on the decomposed test points, complete the test case writing for TageSC. Test cases need to cover all test points. At the same time, a detailed explanation of the test cases is required, including the purpose, input, output, expected results, and principles of the test cases.
4. Complete the code writing of the test cases for TageSC, it is required to complete **the writing of the reference model**. Ensure that the test cases can run through the verification environment. In the coding process, the quality of the code needs to be ensured, including the readability, maintainability, and scalability of the code.
5. Complete the running of the test cases for TageSC and generate a test report. The test report needs to include the running results of the test cases, code line coverage, function coverage, etc. The test report needs to be saved in the [`tests/report`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fyaozhicheng%2Fworkspace%2Fenv-xs-ov-00-bpu%2Ftests%2Freport%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/yaozhicheng/workspace/env-xs-ov-00-bpu/tests/report") directory, and you can open `tests/report/TageSC-yourId.html` in the browser to view the content of this test report.
6. Before the final submission, you need to check the test report to ensure that the test report meets the basic requirements for submitting PR.

### Task 3. ITTAGE

Source code address: [ITTAGE.sv](https://github.com/XS-MLVP/env-xs-ov-00-bpu/tree/main/rtl/ITTAGE)
Function description document: [ITTAGE Branch Predictor](https://open-verify.cc/xs-bpu/en/docs/modules/04_ittage/)
Reference function point document: [ITTAGE Function List](https://open-verify.cc/xs-bpu/en/docs/feature/04_ittagefeature/)

1. Complete the code and document reading of the ITTAGE sub-predictor, understand the working principles and functions of the ITTAGE. Clarify the structure of the Tage table items used by ITTAGE, understand the predictor structure of ITTAGE. Also understand the working principle of branch folding history.
2. Based on the given reference function points, improve the function points that ITTAGE needs to verify, and decompose specific test points for these function points. At the same time, explain the significance of each test point to verify the function points.
3. Based on the decomposed test points, complete the test case writing for ITTAGE. Test cases need to cover all test points. At the same time, a detailed explanation of the test cases is required, including the purpose, input, output, expected results, and principles of the test cases.
4. Complete the code writing of the test cases for ITTAGE, it is required to complete **the writing of the reference model**. Ensure that the test cases can run through the verification environment. In the coding process, the quality of the code needs to be ensured, including the readability, maintainability, and scalability of the code.
5. Complete the running of the test cases for ITTAGE and generate a test report. The test report needs to include the running results of the test cases, code line coverage, function coverage, etc. The test report needs to be saved in the [`tests/report`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fyaozhicheng%2Fworkspace%2Fenv-xs-ov-00-bpu%2Ftests%2Freport%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/yaozhicheng/workspace/env-xs-ov-00-bpu/tests/report") directory, and you can open `tests/report/ITTAGE-yourId.html` in the browser to view the content of this test report.
6. Before the final submission, you need to check the test report to ensure that the test report meets the basic requirements for submitting PR.


Translate the following markdown from Chinese to American English:

### Task 4. RAS

Source code address: [RAS.sv](https://github.com/XS-MLVP/env-xs-ov-00-bpu/tree/main/rtl/RAS)
Function description document: [RAS Branch Predictor](https://open-verify.cc/xs-bpu/en/docs/modules/05_ras/)
Reference function point document: [RAS Function List](https://open-verify.cc/xs-bpu/en/docs/feature/05_rasfeature/)

1. Complete the code and document reading of the RAS sub-predictor, understand the working principle and module function of RAS. Understand the working principle of the stack frame when the program runs, and then clarify the working principle of the RAS stack of RAS. Most clearly, the RAS predictor provides predictions for call and ret instructions.
2. Based on the given reference function points, improve the function points that RAS needs to verify, and decompose specific test points for these function points. At the same time, explain the significance of each test point to the verification function point.
3. Based on the decomposed test points, complete the test case writing for RAS. The test cases need to cover all test points. At the same time, a detailed explanation of the test cases is required, including the purpose, input, output, expected results, and principles of the test cases.
4. Complete the code writing of the RAS test cases, and require the completion of **writing the reference model**. Ensure that the test cases can pass the verification environment. During the coding process, the quality of the code needs to be ensured, including the readability, maintainability, and scalability of the code.
5. Complete the running of the RAS test cases and generate a test report. The test report needs to include the running results of the test cases, code line coverage, function coverage, and other information. The test report needs to be saved in the [`tests/report`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fyaozhicheng%2Fworkspace%2Fenv-xs-ov-00-bpu%2Ftests%2Freport%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/yaozhicheng/workspace/env-xs-ov-00-bpu/tests/report") directory, and you can open `tests/report/RAS-yourId.html` in the browser to view the content of this test report.
6. Before the final submission, you need to check the test report to ensure that the test report meets the basic requirements for submitting PR.

### Task 5. BPU Top

Source code address: [Predictor.sv & Composer.sv](https://github.com/XS-MLVP/env-xs-ov-00-bpu/tree/main/rtl/common)
Function description document: [BPU Top Module](https://open-verify.cc/xs-bpu/en/docs/modules/00_bpu_top/)
Reference function point document: [BPU Top Function List](https://open-verify.cc/xs-bpu/en/docs/feature/00_bpufeature/)

1. Complete the code and document reading of the BPU Top sub-predictor, understand the working principle and module function of BPU Top. Understand the predictor structure of BPU Top, clarify how the BPU Top predictor provides predictions for different types of branches. At the same time, understand how BPU Top interacts with the external FTQ module.
2. Based on the given reference function points, improve the function points that BPU Top needs to verify, and decompose specific test points for these function points. At the same time, explain the significance of each test point to the verification function point.
3. Based on the decomposed test points, complete the test case writing for BPU Top. The test cases need to cover all test points. At the same time, a detailed explanation of the test cases is required, including the purpose, input, output, expected results, and principles of the test cases.
4. Complete the code writing of the BPU Top test cases, and require the completion of **writing the reference model and the FTQ simulation verification environment**. Ensure that the test cases can pass the verification environment. During the coding process, the quality of the code needs to be ensured, including the readability, maintainability, and scalability of the code.
5. Complete the running of the BPU Top test cases and generate a test report. The test report needs to include the running results of the test cases, code line coverage, function coverage, and other information. The test report needs to be saved in the [`tests/report`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fyaozhicheng%2Fworkspace%2Fenv-xs-ov-00-bpu%2Ftests%2Freport%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/home/yaozhicheng/workspace/env-xs-ov-00-bpu/tests/report") directory, and you can open `tests/report/BPU-Top-yourId.html` in the browser to view the content of this test report.
6. Before the final submission, you need to check the test report to ensure that the test report meets the basic requirements for submitting PR.

## Milestones

1. Complete function point and test point decomposition: After completing the reading work of `1.`, proceed to `2.`. You can start the following work after communicating with us to confirm the completion of `2.`.
2. Complete test case communication: After completing `3.`, communicate with us to confirm that the behavior of `3.` meets expectations and the principle is correct before you can start the following work.
3. Complete the test report: After the process of `4.` and `5.`, a test report will be generated. When the report finally meets the basic requirements for PR submission after continuous iteration, and we review and pass, it is considered that the verification task is completed. During the process of completing the iteration, if you encounter bugs, you need to communicate with us, and we will give corresponding points. At the same time, if there are **questions worth asking**, you can discuss them in the discussion group.

## Basic requirements for PR submission

Coverage requirements:

1. The code line coverage needs to be greater than 95%, and explain the reasons for the uncovered code.
1. The function coverage must reach 100%
1. The coverage is obtained by running the verification environment, and the report and generation logic cannot be modified

Document requirements:

1. Reasonably decompose the function points into test points. Function points can be added by yourself, but the original function points cannot be deleted.
1. The designed test cases must cover all test points and function points
1. Please write the test document according to the template
1. After receiving multiple verification tasks, their verification reports need to be written separately

Ways to get points:

1. Reasonable test point decomposition, reasonable verification plan, standardized verification document
1. Find out the bug and analyze the cause of the bug, get points according to the bug confirmation level
1. Fix errors in the project's documents and code, and get points according to the error level
1. Submit the final verification report, get points according to the report quality, coverage
1. Final report score
