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

module FoldedSRAMTemplate_25(
  input         clock,
  input         reset,
  input         io_r_req_valid,
  input  [7:0]  io_r_req_bits_setIdx,
  output        io_r_resp_data_0_valid,
  output [8:0]  io_r_resp_data_0_tag,
  output [1:0]  io_r_resp_data_0_ctr,
  output [40:0] io_r_resp_data_0_target,
  input         io_w_req_valid,
  input  [7:0]  io_w_req_bits_setIdx,
  input  [8:0]  io_w_req_bits_data_0_tag,
  input  [1:0]  io_w_req_bits_data_0_ctr,
  input  [40:0] io_w_req_bits_data_0_target
);

  wire        _array_io_r_resp_data_0_valid;
  wire [8:0]  _array_io_r_resp_data_0_tag;
  wire [1:0]  _array_io_r_resp_data_0_ctr;
  wire [40:0] _array_io_r_resp_data_0_target;
  wire        _array_io_r_resp_data_1_valid;
  wire [8:0]  _array_io_r_resp_data_1_tag;
  wire [1:0]  _array_io_r_resp_data_1_ctr;
  wire [40:0] _array_io_r_resp_data_1_target;
  reg         ridx;
  reg         holdRidx_last_r;
  reg         holdRidx_hold_data;
  wire        holdRidx = holdRidx_last_r ? ridx : holdRidx_hold_data;
  always @(posedge clock) begin
    if (io_r_req_valid)
      ridx <= io_r_req_bits_setIdx[0];
    if (holdRidx_last_r)
      holdRidx_hold_data <= ridx;
  end // always @(posedge)
  always @(posedge clock or posedge reset) begin
    if (reset)
      holdRidx_last_r <= 1'h0;
    else if (io_r_req_valid | holdRidx_last_r)
      holdRidx_last_r <= io_r_req_valid;
  end // always @(posedge, posedge)
  `ifdef ENABLE_INITIAL_REG_
    `ifdef FIRRTL_BEFORE_INITIAL
      `FIRRTL_BEFORE_INITIAL
    `endif // FIRRTL_BEFORE_INITIAL
    logic [31:0] _RANDOM[0:0];
    initial begin
      `ifdef INIT_RANDOM_PROLOG_
        `INIT_RANDOM_PROLOG_
      `endif // INIT_RANDOM_PROLOG_
      `ifdef RANDOMIZE_REG_INIT
        _RANDOM[/*Zero width*/ 1'b0] = `RANDOM;
        ridx = _RANDOM[/*Zero width*/ 1'b0][0];
        holdRidx_last_r = _RANDOM[/*Zero width*/ 1'b0][1];
        holdRidx_hold_data = _RANDOM[/*Zero width*/ 1'b0][2];
      `endif // RANDOMIZE_REG_INIT
      if (reset)
        holdRidx_last_r = 1'h0;
    end // initial
    `ifdef FIRRTL_AFTER_INITIAL
      `FIRRTL_AFTER_INITIAL
    `endif // FIRRTL_AFTER_INITIAL
  `endif // ENABLE_INITIAL_REG_
  SRAMTemplate_43 array (
    .clock                       (clock),
    .reset                       (reset),
    .io_r_req_valid              (io_r_req_valid),
    .io_r_req_bits_setIdx        (io_r_req_bits_setIdx[7:1]),
    .io_r_resp_data_0_valid      (_array_io_r_resp_data_0_valid),
    .io_r_resp_data_0_tag        (_array_io_r_resp_data_0_tag),
    .io_r_resp_data_0_ctr        (_array_io_r_resp_data_0_ctr),
    .io_r_resp_data_0_target     (_array_io_r_resp_data_0_target),
    .io_r_resp_data_1_valid      (_array_io_r_resp_data_1_valid),
    .io_r_resp_data_1_tag        (_array_io_r_resp_data_1_tag),
    .io_r_resp_data_1_ctr        (_array_io_r_resp_data_1_ctr),
    .io_r_resp_data_1_target     (_array_io_r_resp_data_1_target),
    .io_w_req_valid              (io_w_req_valid),
    .io_w_req_bits_setIdx        (io_w_req_bits_setIdx[7:1]),
    .io_w_req_bits_data_0_tag    (io_w_req_bits_data_0_tag),
    .io_w_req_bits_data_0_ctr    (io_w_req_bits_data_0_ctr),
    .io_w_req_bits_data_0_target (io_w_req_bits_data_0_target),
    .io_w_req_bits_data_1_tag    (io_w_req_bits_data_0_tag),
    .io_w_req_bits_data_1_ctr    (io_w_req_bits_data_0_ctr),
    .io_w_req_bits_data_1_target (io_w_req_bits_data_0_target),
    .io_w_req_bits_waymask       (2'h1 << io_w_req_bits_setIdx[0])
  );
  assign io_r_resp_data_0_valid =
    ~holdRidx & _array_io_r_resp_data_0_valid | holdRidx & _array_io_r_resp_data_1_valid;
  assign io_r_resp_data_0_tag =
    (holdRidx ? 9'h0 : _array_io_r_resp_data_0_tag)
    | (holdRidx ? _array_io_r_resp_data_1_tag : 9'h0);
  assign io_r_resp_data_0_ctr =
    (holdRidx ? 2'h0 : _array_io_r_resp_data_0_ctr)
    | (holdRidx ? _array_io_r_resp_data_1_ctr : 2'h0);
  assign io_r_resp_data_0_target =
    (holdRidx ? 41'h0 : _array_io_r_resp_data_0_target)
    | (holdRidx ? _array_io_r_resp_data_1_target : 41'h0);
endmodule
