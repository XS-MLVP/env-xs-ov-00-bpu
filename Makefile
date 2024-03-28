export LANG ?= python
export WAVE ?= true
export VERBOSE ?= false
export EXAMPLE ?= false
export TARGET



default:
	echo "TODO"


tage_sc:
	make -f ./mk/Tage.mk tage_sc

uftb:
	make -f ./mk/uFTB.mk uftb

ftb:
	make -f ./mk/FTB.mk ftb

filter:
	cat log|grep Cannot |awk '{print $8}'| sort| uniq|tr -d "'"

all: tage_sc uftb ftb
