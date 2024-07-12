TOP_ENTRY := ./rtl/TageSC/Tage_SC.sv
TOP_FILES := ./rtl/Tage_SC.txt
TL ?= cpp

ifneq ($(TARGET),)
	TARGET := $(TARGET)
else
	TARGET := out/picker_out_TageSC
endif

# if EXAMPLE is set, then _EXAMPLE is set to -e
ifneq ($(EXAMPLE), false)
	_EXAMPLE := -e
endif
_EXAMPLE ?=
# if VERBOSE is set, then _VERBOSE is set to -v
ifneq ($(VERBOSE), false)
	_VERBOSE := --verbose
endif
_VERBOSE ?=
# if WAVE is set, then _WAVEFORM is set to -w
ifneq ($(WAVE), false)
	ifneq ($(WAVE), true)
		_WAVEFORM := -w $(WAVE)
	else
		_WAVEFORM := -w TageSC.fst
	endif
endif
_WAVEFORM ?=

tage_sc:
	@echo "Building tage module with parameters: "
	@echo "TL=${TL}"
	@echo "TOP_ENTRY=${TOP_ENTRY}"
	@echo "TOP_FILES=${TOP_FILES}"
	@echo "TARGET=${TARGET}"
	@echo "WAVEFORM=${_WAVEFORM}"
	@echo "VERBOSE=${_VERBOSE}"
	@echo "EXAMPLE=${_EXAMPLE}"

	@mkdir -p out
	rm -rf ${TARGET} 
	picker export ${TOP_ENTRY} --fs ${TOP_FILES} --lang ${TL} -c\
		--tdir ${TARGET} ${_WAVEFORM}${_EXAMPLE} ${_VERBOSE}
		
