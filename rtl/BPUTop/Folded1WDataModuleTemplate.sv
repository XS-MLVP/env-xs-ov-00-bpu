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

module Folded1WDataModuleTemplate(
  input        clock,
  input        reset,
  input        io_ren_0,
  input  [7:0] io_raddr_0,
  output       io_rdata_0,
  input        io_wen,
  input  [7:0] io_waddr,
  input        io_wdata,
  input        io_resetEn
);

  wire [15:0] _data_ext_R0_data;
  reg         doing_reset;
  reg  [3:0]  resetRow;
  reg  [7:0]  raddr_0;
  wire [15:0] _GEN =
    {{_data_ext_R0_data[15]},
     {_data_ext_R0_data[14]},
     {_data_ext_R0_data[13]},
     {_data_ext_R0_data[12]},
     {_data_ext_R0_data[11]},
     {_data_ext_R0_data[10]},
     {_data_ext_R0_data[9]},
     {_data_ext_R0_data[8]},
     {_data_ext_R0_data[7]},
     {_data_ext_R0_data[6]},
     {_data_ext_R0_data[5]},
     {_data_ext_R0_data[4]},
     {_data_ext_R0_data[3]},
     {_data_ext_R0_data[2]},
     {_data_ext_R0_data[1]},
     {_data_ext_R0_data[0]}};
  always @(posedge clock or posedge reset) begin
    if (reset) begin
      doing_reset <= 1'h1;
      resetRow <= 4'h0;
    end
    else begin
      doing_reset <= resetRow != 4'hF & (io_resetEn | doing_reset);
      if (doing_reset)
        resetRow <= 4'(resetRow + 4'h1);
    end
  end // always @(posedge, posedge)
  always @(posedge clock) begin
    if (io_ren_0)
      raddr_0 <= io_raddr_0;
  end // always @(posedge)
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
        doing_reset = _RANDOM[/*Zero width*/ 1'b0][0];
        resetRow = _RANDOM[/*Zero width*/ 1'b0][4:1];
        raddr_0 = _RANDOM[/*Zero width*/ 1'b0][12:5];
      `endif // RANDOMIZE_REG_INIT
      if (reset) begin
        doing_reset = 1'h1;
        resetRow = 4'h0;
      end
    end // initial
    `ifdef FIRRTL_AFTER_INITIAL
      `FIRRTL_AFTER_INITIAL
    `endif // FIRRTL_AFTER_INITIAL
  `endif // ENABLE_INITIAL_REG_
  data_16x16 data_ext (
    .R0_addr (raddr_0[7:4]),
    .R0_en   (1'h1),
    .R0_clk  (clock),
    .R0_data (_data_ext_R0_data),
    .W0_addr (io_waddr[7:4]),
    .W0_en   (~doing_reset & io_wen),
    .W0_clk  (clock),
    .W0_data ({16{io_wdata}}),
    .W1_addr (resetRow),
    .W1_en   (doing_reset),
    .W1_clk  (clock),
    .W1_data (16'h0)
  );
  assign io_rdata_0 = ~doing_reset & _GEN[raddr_0[3:0]];
endmodule

