TEST_MODULE=FauFTB
TEST=uFTB_raw
TEST_FOLDER=./$(TEST)
COV_FILE_NAME=V$(TEST_MODULE)_coverage.dat

PYTHON=python3

START_CODE="from mlvp.reporter import *;\
set_meta_info('line_grate', 10);\
report = 'report/report.html';\
generate_pytest_report(report, args=['-s', '$(TEST_FOLDER)'], );\
"

run:
	@echo "Running test $(TEST)..."
	@$(PYTHON) -c $(START_CODE)
