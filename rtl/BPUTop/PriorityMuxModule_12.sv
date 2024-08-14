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

module PriorityMuxModule_12(
  input  s2_AFHOB_sel,
  input  s2_AFHOB_src_afhob_5_bits_0,
  input  s2_AFHOB_src_afhob_5_bits_1,
  input  s2_AFHOB_src_afhob_5_bits_2,
  input  s2_AFHOB_src_afhob_5_bits_3,
  input  s2_AFHOB_src_afhob_4_bits_0,
  input  s2_AFHOB_src_afhob_4_bits_1,
  input  s2_AFHOB_src_afhob_4_bits_2,
  input  s2_AFHOB_src_afhob_4_bits_3,
  input  s2_AFHOB_src_afhob_3_bits_0,
  input  s2_AFHOB_src_afhob_3_bits_1,
  input  s2_AFHOB_src_afhob_3_bits_2,
  input  s2_AFHOB_src_afhob_3_bits_3,
  input  s2_AFHOB_src_afhob_2_bits_0,
  input  s2_AFHOB_src_afhob_2_bits_1,
  input  s2_AFHOB_src_afhob_2_bits_2,
  input  s2_AFHOB_src_afhob_2_bits_3,
  input  s2_AFHOB_src_afhob_1_bits_0,
  input  s2_AFHOB_src_afhob_1_bits_1,
  input  s2_AFHOB_src_afhob_1_bits_2,
  input  s2_AFHOB_src_afhob_1_bits_3,
  input  s2_AFHOB_src_afhob_0_bits_0,
  input  s2_AFHOB_src_afhob_0_bits_1,
  input  s2_AFHOB_src_afhob_0_bits_2,
  input  s2_AFHOB_src_afhob_0_bits_3,
  input  s1_AFHOB_sel,
  input  s1_AFHOB_src_afhob_5_bits_0,
  input  s1_AFHOB_src_afhob_5_bits_1,
  input  s1_AFHOB_src_afhob_5_bits_2,
  input  s1_AFHOB_src_afhob_5_bits_3,
  input  s1_AFHOB_src_afhob_4_bits_0,
  input  s1_AFHOB_src_afhob_4_bits_1,
  input  s1_AFHOB_src_afhob_4_bits_2,
  input  s1_AFHOB_src_afhob_4_bits_3,
  input  s1_AFHOB_src_afhob_3_bits_0,
  input  s1_AFHOB_src_afhob_3_bits_1,
  input  s1_AFHOB_src_afhob_3_bits_2,
  input  s1_AFHOB_src_afhob_3_bits_3,
  input  s1_AFHOB_src_afhob_2_bits_0,
  input  s1_AFHOB_src_afhob_2_bits_1,
  input  s1_AFHOB_src_afhob_2_bits_2,
  input  s1_AFHOB_src_afhob_2_bits_3,
  input  s1_AFHOB_src_afhob_1_bits_0,
  input  s1_AFHOB_src_afhob_1_bits_1,
  input  s1_AFHOB_src_afhob_1_bits_2,
  input  s1_AFHOB_src_afhob_1_bits_3,
  input  s1_AFHOB_src_afhob_0_bits_0,
  input  s1_AFHOB_src_afhob_0_bits_1,
  input  s1_AFHOB_src_afhob_0_bits_2,
  input  s1_AFHOB_src_afhob_0_bits_3,
  input  s3_AFHOB_sel,
  input  s3_AFHOB_src_afhob_5_bits_0,
  input  s3_AFHOB_src_afhob_5_bits_1,
  input  s3_AFHOB_src_afhob_5_bits_2,
  input  s3_AFHOB_src_afhob_5_bits_3,
  input  s3_AFHOB_src_afhob_4_bits_0,
  input  s3_AFHOB_src_afhob_4_bits_1,
  input  s3_AFHOB_src_afhob_4_bits_2,
  input  s3_AFHOB_src_afhob_4_bits_3,
  input  s3_AFHOB_src_afhob_3_bits_0,
  input  s3_AFHOB_src_afhob_3_bits_1,
  input  s3_AFHOB_src_afhob_3_bits_2,
  input  s3_AFHOB_src_afhob_3_bits_3,
  input  s3_AFHOB_src_afhob_2_bits_0,
  input  s3_AFHOB_src_afhob_2_bits_1,
  input  s3_AFHOB_src_afhob_2_bits_2,
  input  s3_AFHOB_src_afhob_2_bits_3,
  input  s3_AFHOB_src_afhob_1_bits_0,
  input  s3_AFHOB_src_afhob_1_bits_1,
  input  s3_AFHOB_src_afhob_1_bits_2,
  input  s3_AFHOB_src_afhob_1_bits_3,
  input  s3_AFHOB_src_afhob_0_bits_0,
  input  s3_AFHOB_src_afhob_0_bits_1,
  input  s3_AFHOB_src_afhob_0_bits_2,
  input  s3_AFHOB_src_afhob_0_bits_3,
  input  redirect_AFHOB_sel,
  input  redirect_AFHOB_src_afhob_5_bits_0,
  input  redirect_AFHOB_src_afhob_5_bits_1,
  input  redirect_AFHOB_src_afhob_5_bits_2,
  input  redirect_AFHOB_src_afhob_5_bits_3,
  input  redirect_AFHOB_src_afhob_4_bits_0,
  input  redirect_AFHOB_src_afhob_4_bits_1,
  input  redirect_AFHOB_src_afhob_4_bits_2,
  input  redirect_AFHOB_src_afhob_4_bits_3,
  input  redirect_AFHOB_src_afhob_3_bits_0,
  input  redirect_AFHOB_src_afhob_3_bits_1,
  input  redirect_AFHOB_src_afhob_3_bits_2,
  input  redirect_AFHOB_src_afhob_3_bits_3,
  input  redirect_AFHOB_src_afhob_2_bits_0,
  input  redirect_AFHOB_src_afhob_2_bits_1,
  input  redirect_AFHOB_src_afhob_2_bits_2,
  input  redirect_AFHOB_src_afhob_2_bits_3,
  input  redirect_AFHOB_src_afhob_1_bits_0,
  input  redirect_AFHOB_src_afhob_1_bits_1,
  input  redirect_AFHOB_src_afhob_1_bits_2,
  input  redirect_AFHOB_src_afhob_1_bits_3,
  input  redirect_AFHOB_src_afhob_0_bits_0,
  input  redirect_AFHOB_src_afhob_0_bits_1,
  input  redirect_AFHOB_src_afhob_0_bits_2,
  input  redirect_AFHOB_src_afhob_0_bits_3,
  input  stallAFHOB_src_afhob_5_bits_0,
  input  stallAFHOB_src_afhob_5_bits_1,
  input  stallAFHOB_src_afhob_5_bits_2,
  input  stallAFHOB_src_afhob_5_bits_3,
  input  stallAFHOB_src_afhob_4_bits_0,
  input  stallAFHOB_src_afhob_4_bits_1,
  input  stallAFHOB_src_afhob_4_bits_2,
  input  stallAFHOB_src_afhob_4_bits_3,
  input  stallAFHOB_src_afhob_3_bits_0,
  input  stallAFHOB_src_afhob_3_bits_1,
  input  stallAFHOB_src_afhob_3_bits_2,
  input  stallAFHOB_src_afhob_3_bits_3,
  input  stallAFHOB_src_afhob_2_bits_0,
  input  stallAFHOB_src_afhob_2_bits_1,
  input  stallAFHOB_src_afhob_2_bits_2,
  input  stallAFHOB_src_afhob_2_bits_3,
  input  stallAFHOB_src_afhob_1_bits_0,
  input  stallAFHOB_src_afhob_1_bits_1,
  input  stallAFHOB_src_afhob_1_bits_2,
  input  stallAFHOB_src_afhob_1_bits_3,
  input  stallAFHOB_src_afhob_0_bits_0,
  input  stallAFHOB_src_afhob_0_bits_1,
  input  stallAFHOB_src_afhob_0_bits_2,
  input  stallAFHOB_src_afhob_0_bits_3,
  output out_res_afhob_5_bits_0,
  output out_res_afhob_5_bits_1,
  output out_res_afhob_5_bits_2,
  output out_res_afhob_5_bits_3,
  output out_res_afhob_4_bits_0,
  output out_res_afhob_4_bits_1,
  output out_res_afhob_4_bits_2,
  output out_res_afhob_4_bits_3,
  output out_res_afhob_3_bits_0,
  output out_res_afhob_3_bits_1,
  output out_res_afhob_3_bits_2,
  output out_res_afhob_3_bits_3,
  output out_res_afhob_2_bits_0,
  output out_res_afhob_2_bits_1,
  output out_res_afhob_2_bits_2,
  output out_res_afhob_2_bits_3,
  output out_res_afhob_1_bits_0,
  output out_res_afhob_1_bits_1,
  output out_res_afhob_1_bits_2,
  output out_res_afhob_1_bits_3,
  output out_res_afhob_0_bits_0,
  output out_res_afhob_0_bits_1,
  output out_res_afhob_0_bits_2,
  output out_res_afhob_0_bits_3
);

  assign out_res_afhob_5_bits_0 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_5_bits_0
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_5_bits_0
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_5_bits_0
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_5_bits_0
                  : stallAFHOB_src_afhob_5_bits_0;
  assign out_res_afhob_5_bits_1 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_5_bits_1
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_5_bits_1
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_5_bits_1
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_5_bits_1
                  : stallAFHOB_src_afhob_5_bits_1;
  assign out_res_afhob_5_bits_2 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_5_bits_2
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_5_bits_2
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_5_bits_2
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_5_bits_2
                  : stallAFHOB_src_afhob_5_bits_2;
  assign out_res_afhob_5_bits_3 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_5_bits_3
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_5_bits_3
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_5_bits_3
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_5_bits_3
                  : stallAFHOB_src_afhob_5_bits_3;
  assign out_res_afhob_4_bits_0 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_4_bits_0
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_4_bits_0
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_4_bits_0
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_4_bits_0
                  : stallAFHOB_src_afhob_4_bits_0;
  assign out_res_afhob_4_bits_1 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_4_bits_1
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_4_bits_1
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_4_bits_1
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_4_bits_1
                  : stallAFHOB_src_afhob_4_bits_1;
  assign out_res_afhob_4_bits_2 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_4_bits_2
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_4_bits_2
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_4_bits_2
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_4_bits_2
                  : stallAFHOB_src_afhob_4_bits_2;
  assign out_res_afhob_4_bits_3 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_4_bits_3
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_4_bits_3
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_4_bits_3
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_4_bits_3
                  : stallAFHOB_src_afhob_4_bits_3;
  assign out_res_afhob_3_bits_0 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_3_bits_0
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_3_bits_0
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_3_bits_0
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_3_bits_0
                  : stallAFHOB_src_afhob_3_bits_0;
  assign out_res_afhob_3_bits_1 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_3_bits_1
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_3_bits_1
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_3_bits_1
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_3_bits_1
                  : stallAFHOB_src_afhob_3_bits_1;
  assign out_res_afhob_3_bits_2 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_3_bits_2
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_3_bits_2
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_3_bits_2
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_3_bits_2
                  : stallAFHOB_src_afhob_3_bits_2;
  assign out_res_afhob_3_bits_3 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_3_bits_3
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_3_bits_3
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_3_bits_3
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_3_bits_3
                  : stallAFHOB_src_afhob_3_bits_3;
  assign out_res_afhob_2_bits_0 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_2_bits_0
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_2_bits_0
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_2_bits_0
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_2_bits_0
                  : stallAFHOB_src_afhob_2_bits_0;
  assign out_res_afhob_2_bits_1 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_2_bits_1
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_2_bits_1
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_2_bits_1
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_2_bits_1
                  : stallAFHOB_src_afhob_2_bits_1;
  assign out_res_afhob_2_bits_2 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_2_bits_2
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_2_bits_2
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_2_bits_2
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_2_bits_2
                  : stallAFHOB_src_afhob_2_bits_2;
  assign out_res_afhob_2_bits_3 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_2_bits_3
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_2_bits_3
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_2_bits_3
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_2_bits_3
                  : stallAFHOB_src_afhob_2_bits_3;
  assign out_res_afhob_1_bits_0 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_1_bits_0
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_1_bits_0
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_1_bits_0
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_1_bits_0
                  : stallAFHOB_src_afhob_1_bits_0;
  assign out_res_afhob_1_bits_1 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_1_bits_1
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_1_bits_1
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_1_bits_1
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_1_bits_1
                  : stallAFHOB_src_afhob_1_bits_1;
  assign out_res_afhob_1_bits_2 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_1_bits_2
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_1_bits_2
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_1_bits_2
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_1_bits_2
                  : stallAFHOB_src_afhob_1_bits_2;
  assign out_res_afhob_1_bits_3 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_1_bits_3
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_1_bits_3
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_1_bits_3
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_1_bits_3
                  : stallAFHOB_src_afhob_1_bits_3;
  assign out_res_afhob_0_bits_0 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_0_bits_0
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_0_bits_0
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_0_bits_0
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_0_bits_0
                  : stallAFHOB_src_afhob_0_bits_0;
  assign out_res_afhob_0_bits_1 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_0_bits_1
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_0_bits_1
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_0_bits_1
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_0_bits_1
                  : stallAFHOB_src_afhob_0_bits_1;
  assign out_res_afhob_0_bits_2 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_0_bits_2
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_0_bits_2
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_0_bits_2
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_0_bits_2
                  : stallAFHOB_src_afhob_0_bits_2;
  assign out_res_afhob_0_bits_3 =
    s2_AFHOB_sel
      ? s2_AFHOB_src_afhob_0_bits_3
      : s1_AFHOB_sel
          ? s1_AFHOB_src_afhob_0_bits_3
          : s3_AFHOB_sel
              ? s3_AFHOB_src_afhob_0_bits_3
              : redirect_AFHOB_sel
                  ? redirect_AFHOB_src_afhob_0_bits_3
                  : stallAFHOB_src_afhob_0_bits_3;
endmodule

