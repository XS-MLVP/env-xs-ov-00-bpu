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

module Folded1WDataModuleTemplate(	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
  input        clock,	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
  input        reset,	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
  input        io_ren_0,	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:209:14]
  input  [7:0] io_raddr_0,	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:209:14]
  output       io_rdata_0,	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:209:14]
  input        io_wen,	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:209:14]
  input  [7:0] io_waddr,	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:209:14]
  input        io_wdata,	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:209:14]
  input        io_resetEn	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:209:14]
);

  wire [15:0] _data_ext_R0_data;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:224:17]
  reg         doing_reset;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:226:28]
  reg  [3:0]  resetRow;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:230:25]
  reg  [7:0]  raddr_0;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:236:69]
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
     {_data_ext_R0_data[0]}};	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:224:17, :243:23]
  always @(posedge clock or posedge reset) begin	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
    if (reset) begin	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
      doing_reset <= 1'h1;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7, :226:28]
      resetRow <= 4'h0;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:230:25]
    end
    else begin	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
      doing_reset <= resetRow != 4'hF & (io_resetEn | doing_reset);	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:226:28, :228:{36,50}, :230:25, :232:{18,35,49}]
      if (doing_reset)	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:226:28]
        resetRow <= 4'(resetRow + 4'h1);	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:230:25, :231:45]
    end
  end // always @(posedge, posedge)
  always @(posedge clock) begin	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
    if (io_ren_0)	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:209:14]
      raddr_0 <= io_raddr_0;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:236:69]
  end // always @(posedge)
  `ifdef ENABLE_INITIAL_REG_	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
    `ifdef FIRRTL_BEFORE_INITIAL	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
      `FIRRTL_BEFORE_INITIAL	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
    `endif // FIRRTL_BEFORE_INITIAL
    logic [31:0] _RANDOM[0:0];	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
    initial begin	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
      `ifdef INIT_RANDOM_PROLOG_	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
        `INIT_RANDOM_PROLOG_	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
      `endif // INIT_RANDOM_PROLOG_
      `ifdef RANDOMIZE_REG_INIT	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
        _RANDOM[/*Zero width*/ 1'b0] = `RANDOM;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
        doing_reset = _RANDOM[/*Zero width*/ 1'b0][0];	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7, :226:28]
        resetRow = _RANDOM[/*Zero width*/ 1'b0][4:1];	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7, :226:28, :230:25]
        raddr_0 = _RANDOM[/*Zero width*/ 1'b0][12:5];	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7, :226:28, :236:69]
      `endif // RANDOMIZE_REG_INIT
      if (reset) begin	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
        doing_reset = 1'h1;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7, :226:28]
        resetRow = 4'h0;	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:230:25]
      end
    end // initial
    `ifdef FIRRTL_AFTER_INITIAL	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
      `FIRRTL_AFTER_INITIAL	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
    `endif // FIRRTL_AFTER_INITIAL
  `endif // ENABLE_INITIAL_REG_
  data_16x16 data_ext (	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:224:17]
    .R0_addr (raddr_0[7:4]),	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:236:69, :241:25]
    .R0_en   (1'h1),	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7]
    .R0_clk  (clock),
    .R0_data (_data_ext_R0_data),
    .W0_addr (io_waddr[7:4]),	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:246:24]
    .W0_en   (~doing_reset & io_wen),	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:224:17, :226:28, :243:23, :250:21, :252:22]
    .W0_clk  (clock),
    .W0_data ({16{io_wdata}}),	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:224:17]
    .W1_addr (resetRow),	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:230:25]
    .W1_en   (doing_reset),	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:226:28]
    .W1_clk  (clock),
    .W1_data (16'h0)	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:224:17]
  );
  assign io_rdata_0 = ~doing_reset & _GEN[raddr_0[3:0]];	// @[utility/src/main/scala/utility/DataModuleTemplate.scala:207:7, :226:28, :236:69, :242:23, :243:23]
endmodule

