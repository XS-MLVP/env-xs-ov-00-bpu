export TL ?= python
export WAVE ?= true
export VERBOSE ?= false
export EXAMPLE ?= false
export TARGET



default:
	@echo "Usage"
	@echo "  test:     run tests, use TEST=test_name specify test folder in tests, default test all tests"
	@echo "  uftb:     build uFTB DUT module"
	@echo "  tage_sc:  build TAGE_SC DUT module"
	@echo "  ftb:      build FTB DUT module"
	@echo "  ras:      build RAS DUT module"
	@echo "  ittage:   build ITTAGE DUT module"
	@echo "  all:      build all DUTs"
	@echo "Make examples:"
	@echo "  make test TEST=uFTB-raw"
	@echo "  make uftb"

test:
	make -f tests/Makefile

uftb:
	make -f ./mk/uFTB.mk uftb

tage_sc:
	make -f ./mk/Tage.mk tage_sc

ftb:
	make -f ./mk/FTB.mk ftb

ras:
	make -f ./mk/RAS.mk ras

ittage:
	make -f ./mk/ITTAGE.mk ittage

filter:
	cat log|grep Cannot |awk '{print $8}'| sort| uniq|tr -d "'"

all: uftb tage_sc ftb ras ittage
