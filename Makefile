export TL ?= python
export WAVE ?= true
export VERBOSE ?= false
export EXAMPLE ?= false
export TARGET



default:
	echo "TODO"

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
