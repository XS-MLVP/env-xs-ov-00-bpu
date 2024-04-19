// Generated by CIRCT firtool-1.61.0
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

module FoldedSRAMTemplate_21(	// utility/src/main/scala/utility/SRAMTemplate.scala:162:7
  input         clock,
  input         reset,
  input         io_r_req_valid,	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
  input  [6:0]  io_r_req_bits_setIdx,	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
  output [8:0]  io_r_resp_data_0_tag,	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
  output [1:0]  io_r_resp_data_0_ctr,	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
  output [38:0] io_r_resp_data_0_target,	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
  input         io_w_req_valid,	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
  input  [6:0]  io_w_req_bits_setIdx,	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
  input  [8:0]  io_w_req_bits_data_0_tag,	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
  input  [1:0]  io_w_req_bits_data_0_ctr,	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
  input  [38:0] io_w_req_bits_data_0_target	// utility/src/main/scala/utility/SRAMTemplate.scala:165:14
);

  SRAMTemplate_35 array (	// utility/src/main/scala/utility/SRAMTemplate.scala:179:21
    .clock                       (clock),
    .reset                       (reset),
    .io_r_req_valid              (io_r_req_valid),
    .io_r_req_bits_setIdx        (io_r_req_bits_setIdx),
    .io_r_resp_data_0_tag        (io_r_resp_data_0_tag),
    .io_r_resp_data_0_ctr        (io_r_resp_data_0_ctr),
    .io_r_resp_data_0_target     (io_r_resp_data_0_target),
    .io_w_req_valid              (io_w_req_valid),
    .io_w_req_bits_setIdx        (io_w_req_bits_setIdx),
    .io_w_req_bits_data_0_tag    (io_w_req_bits_data_0_tag),
    .io_w_req_bits_data_0_ctr    (io_w_req_bits_data_0_ctr),
    .io_w_req_bits_data_0_target (io_w_req_bits_data_0_target)
  );
endmodule

