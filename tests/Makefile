TEST=.
TEST_FOLDER=./$(TEST)

PYTHON=python3

START_CODE="from mlvp.reporter import *;\
set_meta_info('test_case', '$(TEST)');\
report = 'report/$(TEST)/report.html';\
generate_pytest_report(report, args=['-s', '$(TEST_FOLDER)'], );\
"

run:
	@echo "Running test $(TEST)..."
	@mkdir report/$(TEST) -p
	@$(PYTHON) -c $(START_CODE)

clean:
	rm -rf report/ *.fst *.dat *.log *.hier
