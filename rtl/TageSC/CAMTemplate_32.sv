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

module CAMTemplate_32(	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
  input         clock,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
  input  [10:0] io_r_req_0_idx,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  output        io_r_resp_0_0,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  output        io_r_resp_0_1,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  output        io_r_resp_0_2,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  output        io_r_resp_0_3,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  output        io_r_resp_0_4,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  output        io_r_resp_0_5,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  output        io_r_resp_0_6,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  output        io_r_resp_0_7,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  input         io_w_valid,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  input  [10:0] io_w_bits_data_idx,	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
  input  [2:0]  io_w_bits_index	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:149:14]
);

  reg [10:0] array_0;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
  reg [10:0] array_1;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
  reg [10:0] array_2;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
  reg [10:0] array_3;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
  reg [10:0] array_4;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
  reg [10:0] array_5;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
  reg [10:0] array_6;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
  reg [10:0] array_7;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
  always @(posedge clock) begin	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
    if (io_w_valid & io_w_bits_index == 3'h0)	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18, :170:21, :171:28]
      array_0 <= io_w_bits_data_idx;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
    if (io_w_valid & io_w_bits_index == 3'h1)	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18, :170:21, :171:28]
      array_1 <= io_w_bits_data_idx;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
    if (io_w_valid & io_w_bits_index == 3'h2)	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18, :170:21, :171:28]
      array_2 <= io_w_bits_data_idx;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
    if (io_w_valid & io_w_bits_index == 3'h3)	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18, :170:21, :171:28]
      array_3 <= io_w_bits_data_idx;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
    if (io_w_valid & io_w_bits_index == 3'h4)	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18, :170:21, :171:28]
      array_4 <= io_w_bits_data_idx;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
    if (io_w_valid & io_w_bits_index == 3'h5)	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18, :170:21, :171:28]
      array_5 <= io_w_bits_data_idx;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
    if (io_w_valid & io_w_bits_index == 3'h6)	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18, :170:21, :171:28]
      array_6 <= io_w_bits_data_idx;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
    if (io_w_valid & (&io_w_bits_index))	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18, :170:21, :171:28]
      array_7 <= io_w_bits_data_idx;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:164:18]
  end // always @(posedge)
  `ifdef ENABLE_INITIAL_REG_	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
    `ifdef FIRRTL_BEFORE_INITIAL	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
      `FIRRTL_BEFORE_INITIAL	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
    `endif // FIRRTL_BEFORE_INITIAL
    logic [31:0] _RANDOM[0:2];	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
    initial begin	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
      `ifdef INIT_RANDOM_PROLOG_	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
        `INIT_RANDOM_PROLOG_	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
      `endif // INIT_RANDOM_PROLOG_
      `ifdef RANDOMIZE_REG_INIT	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
        for (logic [1:0] i = 2'h0; i < 2'h3; i += 2'h1) begin
          _RANDOM[i] = `RANDOM;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
        end	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
        array_0 = _RANDOM[2'h0][10:0];	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18]
        array_1 = _RANDOM[2'h0][21:11];	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18]
        array_2 = {_RANDOM[2'h0][31:22], _RANDOM[2'h1][0]};	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18]
        array_3 = _RANDOM[2'h1][11:1];	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18]
        array_4 = _RANDOM[2'h1][22:12];	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18]
        array_5 = {_RANDOM[2'h1][31:23], _RANDOM[2'h2][1:0]};	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18]
        array_6 = _RANDOM[2'h2][12:2];	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18]
        array_7 = _RANDOM[2'h2][23:13];	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18]
      `endif // RANDOMIZE_REG_INIT
    end // initial
    `ifdef FIRRTL_AFTER_INITIAL	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
      `FIRRTL_AFTER_INITIAL	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7]
    `endif // FIRRTL_AFTER_INITIAL
  `endif // ENABLE_INITIAL_REG_
  assign io_r_resp_0_0 = io_r_req_0_idx == array_0;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18, :167:39]
  assign io_r_resp_0_1 = io_r_req_0_idx == array_1;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18, :167:39]
  assign io_r_resp_0_2 = io_r_req_0_idx == array_2;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18, :167:39]
  assign io_r_resp_0_3 = io_r_req_0_idx == array_3;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18, :167:39]
  assign io_r_resp_0_4 = io_r_req_0_idx == array_4;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18, :167:39]
  assign io_r_resp_0_5 = io_r_req_0_idx == array_5;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18, :167:39]
  assign io_r_resp_0_6 = io_r_req_0_idx == array_6;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18, :167:39]
  assign io_r_resp_0_7 = io_r_req_0_idx == array_7;	// @[src/main/scala/xiangshan/cache/mmu/MMUBundle.scala:148:7, :164:18, :167:39]
endmodule

