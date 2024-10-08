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

// VCS coverage exclude_file
module data_mem_16x12(	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
  input  [3:0]  R0_addr,
  input         R0_en,
  input         R0_clk,
  output [11:0] R0_data,
  input  [3:0]  R1_addr,
  input         R1_en,
  input         R1_clk,
  output [11:0] R1_data,
  input  [3:0]  W0_addr,
  input         W0_en,
  input         W0_clk,
  input  [11:0] W0_data,
  input  [1:0]  W0_mask
);

  reg [11:0] Memory[0:15];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
  always @(posedge W0_clk) begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
    if (W0_en & W0_mask[0])	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
      Memory[W0_addr][32'h0 +: 6] <= W0_data[5:0];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
    if (W0_en & W0_mask[1])	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
      Memory[W0_addr][32'h6 +: 6] <= W0_data[11:6];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
  end // always @(posedge)
  `ifdef ENABLE_INITIAL_MEM_	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
    reg [31:0] _RANDOM_MEM;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
    initial begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
      `INIT_RANDOM_PROLOG_	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
      `ifdef RANDOMIZE_MEM_INIT	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
        for (logic [4:0] i = 5'h0; i < 5'h10; i += 5'h1) begin
          _RANDOM_MEM = `RANDOM;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
          Memory[i[3:0]] = _RANDOM_MEM[11:0];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
        end	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
      `endif // RANDOMIZE_MEM_INIT
    end // initial
  `endif // ENABLE_INITIAL_MEM_
  assign R0_data = R0_en ? Memory[R0_addr] : 12'bx;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
  assign R1_data = R1_en ? Memory[R1_addr] : 12'bx;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
endmodule

