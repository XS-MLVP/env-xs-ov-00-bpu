// Generated by CIRCT firtool-1.62.0
// Standard header to adapt well known macros for register randomization.
`ifndef RANDOMIZE
  `ifdef RANDOMIZE_MEM_INIT
    `define RANDOMIZE
  `endif // RANDOMIZE_MEM_INIT
`endif // not def RANDOMIZE
`ifndef RANDOMIZE
  `ifdef RANDOMIZE_REG_INIT
    `define RANDOMIZE
  `endif // RANDOMIZE_REG_INIT
`endif // not def RANDOMIZE

// RANDOM may be set to an expression that produces a 32-bit random unsigned value.
`ifndef RANDOM
  `define RANDOM $random
`endif // not def RANDOM

// Users can define INIT_RANDOM as general code that gets injected into the
// initializer block for modules with registers.
`ifndef INIT_RANDOM
  `define INIT_RANDOM
`endif // not def INIT_RANDOM

// If using random initialization, you can also define RANDOMIZE_DELAY to
// customize the delay used, otherwise 0.002 is used.
`ifndef RANDOMIZE_DELAY
  `define RANDOMIZE_DELAY 0.002
`endif // not def RANDOMIZE_DELAY

// Define INIT_RANDOM_PROLOG_ for use in our modules below.
`ifndef INIT_RANDOM_PROLOG_
  `ifdef RANDOMIZE
    `ifdef VERILATOR
      `define INIT_RANDOM_PROLOG_ `INIT_RANDOM
    `else  // VERILATOR
      `define INIT_RANDOM_PROLOG_ `INIT_RANDOM #`RANDOMIZE_DELAY begin end
    `endif // VERILATOR
  `else  // RANDOMIZE
    `define INIT_RANDOM_PROLOG_
  `endif // RANDOMIZE
`endif // not def INIT_RANDOM_PROLOG_

// Include register initializers in init blocks unless synthesis is set
`ifndef SYNTHESIS
  `ifndef ENABLE_INITIAL_REG_
    `define ENABLE_INITIAL_REG_
  `endif // not def ENABLE_INITIAL_REG_
`endif // not def SYNTHESIS

// Include rmemory initializers in init blocks unless synthesis is set
`ifndef SYNTHESIS
  `ifndef ENABLE_INITIAL_MEM_
    `define ENABLE_INITIAL_MEM_
  `endif // not def ENABLE_INITIAL_MEM_
`endif // not def SYNTHESIS

module SRAMTemplate_14(	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
  input         clock,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
  input         reset,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
  output        io_r_req_ready,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_r_req_valid,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input  [7:0]  io_r_req_bits_setIdx,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_0,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_1,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_2,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_3,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_4,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_5,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_6,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_7,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_8,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_9,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_10,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_11,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_12,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_13,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_14,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  output        io_r_resp_data_15,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_valid,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input  [7:0]  io_w_req_bits_setIdx,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_0,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_1,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_2,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_3,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_4,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_5,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_6,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_7,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_8,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_9,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_10,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_11,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_12,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_13,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_14,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         io_w_req_bits_data_15,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input  [15:0] io_w_req_bits_waymask,	// @[utility/src/main/scala/utility/SRAMTemplate.scala:144:14]
  input         extra_reset	// @[utility/src/main/scala/utility/SRAMTemplate.scala:148:44]
);

  wire [7:0]  setIdx;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:174:19]
  wire        realRen;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:172:38]
  wire        wen;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:171:52]
  wire [15:0] _array_RW0_rdata;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:154:26]
  reg         _resetState;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:158:30]
  reg  [7:0]  _resetSet;	// @[src/main/scala/chisel3/util/Counter.scala:61:40]
  assign wen = io_w_req_valid | _resetState;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:158:30, :171:52]
  assign realRen = io_r_req_valid & ~wen;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:171:52, :172:{38,41}]
  assign setIdx = _resetState ? _resetSet : io_w_req_bits_setIdx;	// @[src/main/scala/chisel3/util/Counter.scala:61:40, utility/src/main/scala/utility/SRAMTemplate.scala:158:30, :174:19]
  reg         rdata_last_r;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22]
  reg         rdata_hold_data_0;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_1;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_2;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_3;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_4;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_5;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_6;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_7;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_8;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_9;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_10;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_11;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_12;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_13;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_14;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  reg         rdata_hold_data_15;	// @[utility/src/main/scala/utility/Hold.scala:24:82]
  always @(posedge clock or posedge reset) begin	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
    if (reset) begin	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
      _resetState <= 1'h1;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :158:30]
      _resetSet <= 8'h0;	// @[src/main/scala/chisel3/util/Counter.scala:61:40]
      rdata_last_r <= 1'h0;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
    end
    else begin	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
      _resetState <= extra_reset | ~(_resetState & (&_resetSet)) & _resetState;	// @[src/main/scala/chisel3/util/Counter.scala:61:40, :73:24, :117:24, :118:{16,23}, utility/src/main/scala/utility/SRAMTemplate.scala:158:30, :160:{24,38}, :162:30, :163:21]
      if (_resetState)	// @[utility/src/main/scala/utility/SRAMTemplate.scala:158:30]
        _resetSet <= 8'(_resetSet + 8'h1);	// @[src/main/scala/chisel3/util/Counter.scala:61:40, :77:24]
      if (realRen | rdata_last_r)	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:{22,40}, utility/src/main/scala/utility/SRAMTemplate.scala:172:38]
        rdata_last_r <= realRen;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/SRAMTemplate.scala:172:38]
    end
  end // always @(posedge, posedge)
  always @(posedge clock) begin	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
    if (rdata_last_r) begin	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22]
      rdata_hold_data_0 <= _array_RW0_rdata[0];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_1 <= _array_RW0_rdata[1];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_2 <= _array_RW0_rdata[2];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_3 <= _array_RW0_rdata[3];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_4 <= _array_RW0_rdata[4];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_5 <= _array_RW0_rdata[5];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_6 <= _array_RW0_rdata[6];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_7 <= _array_RW0_rdata[7];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_8 <= _array_RW0_rdata[8];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_9 <= _array_RW0_rdata[9];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_10 <= _array_RW0_rdata[10];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_11 <= _array_RW0_rdata[11];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_12 <= _array_RW0_rdata[12];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_13 <= _array_RW0_rdata[13];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_14 <= _array_RW0_rdata[14];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
      rdata_hold_data_15 <= _array_RW0_rdata[15];	// @[utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :192:69]
    end
  end // always @(posedge)
  `ifdef ENABLE_INITIAL_REG_	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
    `ifdef FIRRTL_BEFORE_INITIAL	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
      `FIRRTL_BEFORE_INITIAL	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
    `endif // FIRRTL_BEFORE_INITIAL
    logic [31:0] _RANDOM[0:33];	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
    initial begin	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
      `ifdef INIT_RANDOM_PROLOG_	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        `INIT_RANDOM_PROLOG_	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
      `endif // INIT_RANDOM_PROLOG_
      `ifdef RANDOMIZE_REG_INIT	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        for (logic [5:0] i = 6'h0; i < 6'h22; i += 6'h1) begin
          _RANDOM[i] = `RANDOM;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        end	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        _resetState = _RANDOM[6'h0][0];	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :158:30]
        _resetSet = _RANDOM[6'h0][8:1];	// @[src/main/scala/chisel3/util/Counter.scala:61:40, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :158:30]
        rdata_last_r = _RANDOM[6'h21][10];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_0 = _RANDOM[6'h21][11];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_1 = _RANDOM[6'h21][12];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_2 = _RANDOM[6'h21][13];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_3 = _RANDOM[6'h21][14];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_4 = _RANDOM[6'h21][15];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_5 = _RANDOM[6'h21][16];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_6 = _RANDOM[6'h21][17];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_7 = _RANDOM[6'h21][18];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_8 = _RANDOM[6'h21][19];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_9 = _RANDOM[6'h21][20];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_10 = _RANDOM[6'h21][21];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_11 = _RANDOM[6'h21][22];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_12 = _RANDOM[6'h21][23];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_13 = _RANDOM[6'h21][24];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_14 = _RANDOM[6'h21][25];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        rdata_hold_data_15 = _RANDOM[6'h21][26];	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
      `endif // RANDOMIZE_REG_INIT
      if (reset) begin	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
        _resetState = 1'h1;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :158:30]
        _resetSet = 8'h0;	// @[src/main/scala/chisel3/util/Counter.scala:61:40]
        rdata_last_r = 1'h0;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
      end
    end // initial
    `ifdef FIRRTL_AFTER_INITIAL	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
      `FIRRTL_AFTER_INITIAL	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7]
    `endif // FIRRTL_AFTER_INITIAL
  `endif // ENABLE_INITIAL_REG_
  array_4 array (	// @[utility/src/main/scala/utility/SRAMTemplate.scala:154:26]
    .RW0_addr  (wen ? setIdx : io_r_req_bits_setIdx),	// @[utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :171:52, :174:19]
    .RW0_en    (realRen | wen),	// @[utility/src/main/scala/utility/SRAMTemplate.scala:154:26, :171:52, :172:38]
    .RW0_clk   (clock),
    .RW0_wmode (wen),	// @[utility/src/main/scala/utility/SRAMTemplate.scala:171:52]
    .RW0_wdata
      ({~_resetState & io_w_req_bits_data_15,
        ~_resetState & io_w_req_bits_data_14,
        ~_resetState & io_w_req_bits_data_13,
        ~_resetState & io_w_req_bits_data_12,
        ~_resetState & io_w_req_bits_data_11,
        ~_resetState & io_w_req_bits_data_10,
        ~_resetState & io_w_req_bits_data_9,
        ~_resetState & io_w_req_bits_data_8,
        ~_resetState & io_w_req_bits_data_7,
        ~_resetState & io_w_req_bits_data_6,
        ~_resetState & io_w_req_bits_data_5,
        ~_resetState & io_w_req_bits_data_4,
        ~_resetState & io_w_req_bits_data_3,
        ~_resetState & io_w_req_bits_data_2,
        ~_resetState & io_w_req_bits_data_1,
        ~_resetState & io_w_req_bits_data_0}),	// @[utility/src/main/scala/utility/SRAMTemplate.scala:158:30, :175:18, :176:13]
    .RW0_rdata (_array_RW0_rdata),
    .RW0_wmask (_resetState ? 16'hFFFF : io_w_req_bits_waymask)	// @[utility/src/main/scala/utility/SRAMTemplate.scala:158:30, :180:{22,39}]
  );
  assign io_r_req_ready = ~_resetState & ~wen;	// @[utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :158:30, :171:52, :172:41, :222:{21,33}]
  assign io_r_resp_data_0 = rdata_last_r ? _array_RW0_rdata[0] : rdata_hold_data_0;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_1 = rdata_last_r ? _array_RW0_rdata[1] : rdata_hold_data_1;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_2 = rdata_last_r ? _array_RW0_rdata[2] : rdata_hold_data_2;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_3 = rdata_last_r ? _array_RW0_rdata[3] : rdata_hold_data_3;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_4 = rdata_last_r ? _array_RW0_rdata[4] : rdata_hold_data_4;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_5 = rdata_last_r ? _array_RW0_rdata[5] : rdata_hold_data_5;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_6 = rdata_last_r ? _array_RW0_rdata[6] : rdata_hold_data_6;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_7 = rdata_last_r ? _array_RW0_rdata[7] : rdata_hold_data_7;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_8 = rdata_last_r ? _array_RW0_rdata[8] : rdata_hold_data_8;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_9 = rdata_last_r ? _array_RW0_rdata[9] : rdata_hold_data_9;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_10 = rdata_last_r ? _array_RW0_rdata[10] : rdata_hold_data_10;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_11 = rdata_last_r ? _array_RW0_rdata[11] : rdata_hold_data_11;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_12 = rdata_last_r ? _array_RW0_rdata[12] : rdata_hold_data_12;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_13 = rdata_last_r ? _array_RW0_rdata[13] : rdata_hold_data_13;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_14 = rdata_last_r ? _array_RW0_rdata[14] : rdata_hold_data_14;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
  assign io_r_resp_data_15 = rdata_last_r ? _array_RW0_rdata[15] : rdata_hold_data_15;	// @[utility/src/main/scala/utility/ClockGatedReg.scala:25:22, utility/src/main/scala/utility/Hold.scala:24:82, :25:8, utility/src/main/scala/utility/SRAMTemplate.scala:138:7, :154:26, :192:69]
endmodule

