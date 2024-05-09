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

module WrBypass(	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
  input        clock,	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
  input        reset,	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
  input        io_wen,	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:34:14]
  input  [8:0] io_write_idx,	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:34:14]
  input  [2:0] io_write_data_0,	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:34:14]
  output       io_hit,	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:34:14]
  output       io_hit_data_0_valid,	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:34:14]
  output [2:0] io_hit_data_0_bits	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:34:14]
);

  wire       _idx_tag_cam_io_r_resp_0_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27]
  wire       _idx_tag_cam_io_r_resp_0_1;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27]
  wire       _idx_tag_cam_io_r_resp_0_2;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27]
  wire       _idx_tag_cam_io_r_resp_0_3;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27]
  wire       _idx_tag_cam_io_r_resp_0_4;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27]
  wire       _idx_tag_cam_io_r_resp_0_5;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27]
  wire       _idx_tag_cam_io_r_resp_0_6;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27]
  wire       _idx_tag_cam_io_r_resp_0_7;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27]
  reg        valids_0_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23]
  reg        valids_1_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23]
  reg        valids_2_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23]
  reg        valids_3_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23]
  reg        valids_4_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23]
  reg        valids_5_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23]
  reg        valids_6_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23]
  reg        valids_7_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23]
  reg        ever_written_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29]
  reg        ever_written_1;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29]
  reg        ever_written_2;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29]
  reg        ever_written_3;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29]
  reg        ever_written_4;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29]
  reg        ever_written_5;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29]
  reg        ever_written_6;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29]
  reg        ever_written_7;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29]
  wire       hits_oh_0 = _idx_tag_cam_io_r_resp_0_0 & ever_written_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27, :57:29, :61:83]
  wire       hits_oh_1 = _idx_tag_cam_io_r_resp_0_1 & ever_written_1;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27, :57:29, :61:83]
  wire       hits_oh_2 = _idx_tag_cam_io_r_resp_0_2 & ever_written_2;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27, :57:29, :61:83]
  wire       hits_oh_3 = _idx_tag_cam_io_r_resp_0_3 & ever_written_3;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27, :57:29, :61:83]
  wire       hits_oh_4 = _idx_tag_cam_io_r_resp_0_4 & ever_written_4;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27, :57:29, :61:83]
  wire       hits_oh_5 = _idx_tag_cam_io_r_resp_0_5 & ever_written_5;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27, :57:29, :61:83]
  wire       hits_oh_6 = _idx_tag_cam_io_r_resp_0_6 & ever_written_6;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27, :57:29, :61:83]
  wire       hits_oh_7 = _idx_tag_cam_io_r_resp_0_7 & ever_written_7;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27, :57:29, :61:83]
  wire [2:0] _hit_idx_T_2 =
    {hits_oh_7, hits_oh_6, hits_oh_5} | {hits_oh_3, hits_oh_2, hits_oh_1};	// @[src/main/scala/chisel3/util/OneHot.scala:30:18, :31:18, :32:28, src/main/scala/xiangshan/frontend/WrBypass.scala:61:83]
  wire [2:0] hit_idx =
    {|{hits_oh_7, hits_oh_6, hits_oh_5, hits_oh_4},
     |(_hit_idx_T_2[2:1]),
     _hit_idx_T_2[2] | _hit_idx_T_2[0]};	// @[src/main/scala/chisel3/util/OneHot.scala:30:18, :31:18, :32:{10,14,28}, src/main/scala/xiangshan/frontend/WrBypass.scala:61:83]
  wire       hit =
    hits_oh_0 | hits_oh_1 | hits_oh_2 | hits_oh_3 | hits_oh_4 | hits_oh_5 | hits_oh_6
    | hits_oh_7;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:61:83, :63:29]
  reg  [6:0] state_reg;	// @[rocket-chip/src/main/scala/util/Replacement.scala:168:72]
  wire [2:0] enq_idx =
    {state_reg[6],
     state_reg[6]
       ? {state_reg[5], state_reg[5] ? state_reg[4] : state_reg[3]}
       : {state_reg[2], state_reg[2] ? state_reg[1] : state_reg[0]}};	// @[rocket-chip/src/main/scala/util/Replacement.scala:168:72, :243:38, :245:38, :249:12, :250:16, rocket-chip/src/main/scala/util/package.scala:155:13]
  wire [2:0] state_reg_touch_way_sized = hit ? hit_idx : enq_idx;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:63:29, :87:37]
  wire       _GEN = enq_idx == 3'h0;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/xiangshan/frontend/WrBypass.scala:95:30, :98:31]
  wire       _GEN_0 = enq_idx == 3'h1;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/xiangshan/frontend/WrBypass.scala:95:30, :98:31]
  wire       _GEN_1 = enq_idx == 3'h2;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/xiangshan/frontend/WrBypass.scala:95:30, :98:31]
  wire       _GEN_2 = enq_idx == 3'h3;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/xiangshan/frontend/WrBypass.scala:95:30, :98:31]
  wire       _GEN_3 = enq_idx == 3'h4;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/xiangshan/frontend/WrBypass.scala:95:30, :98:31]
  wire       _GEN_4 = enq_idx == 3'h5;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/xiangshan/frontend/WrBypass.scala:95:30, :98:31]
  wire       _GEN_5 = enq_idx == 3'h6;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/xiangshan/frontend/WrBypass.scala:95:30, :98:31]
  always @(posedge clock or posedge reset) begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
    if (reset) begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
      valids_0_0 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
      valids_1_0 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
      valids_2_0 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
      valids_3_0 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
      valids_4_0 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
      valids_5_0 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
      valids_6_0 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
      valids_7_0 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
      ever_written_0 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
      ever_written_1 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
      ever_written_2 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
      ever_written_3 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
      ever_written_4 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
      ever_written_5 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
      ever_written_6 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
      ever_written_7 <= 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
      state_reg <= 7'h0;	// @[rocket-chip/src/main/scala/util/Replacement.scala:168:72]
    end
    else begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
      if (io_wen) begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:34:14]
        if (hit) begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:63:29]
          valids_0_0 <= hit_idx == 3'h0 | valids_0_0;	// @[src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :95:30]
          valids_1_0 <= hit_idx == 3'h1 | valids_1_0;	// @[src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :95:30]
          valids_2_0 <= hit_idx == 3'h2 | valids_2_0;	// @[src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :95:30]
          valids_3_0 <= hit_idx == 3'h3 | valids_3_0;	// @[src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :95:30]
          valids_4_0 <= hit_idx == 3'h4 | valids_4_0;	// @[src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :95:30]
          valids_5_0 <= hit_idx == 3'h5 | valids_5_0;	// @[src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :95:30]
          valids_6_0 <= hit_idx == 3'h6 | valids_6_0;	// @[src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :95:30]
          valids_7_0 <= (&hit_idx) | valids_7_0;	// @[src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :95:30]
        end
        else begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:63:29]
          valids_0_0 <= _GEN | ~_GEN & valids_0_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :98:31, :99:28, :101:30]
          valids_1_0 <= _GEN_0 | ~_GEN_0 & valids_1_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :98:31, :99:28, :101:30]
          valids_2_0 <= _GEN_1 | ~_GEN_1 & valids_2_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :98:31, :99:28, :101:30]
          valids_3_0 <= _GEN_2 | ~_GEN_2 & valids_3_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :98:31, :99:28, :101:30]
          valids_4_0 <= _GEN_3 | ~_GEN_3 & valids_4_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :98:31, :99:28, :101:30]
          valids_5_0 <= _GEN_4 | ~_GEN_4 & valids_5_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :98:31, :99:28, :101:30]
          valids_6_0 <= _GEN_5 | ~_GEN_5 & valids_6_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :98:31, :99:28, :101:30]
          valids_7_0 <= (&enq_idx) | ~(&enq_idx) & valids_7_0;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/xiangshan/frontend/WrBypass.scala:56:23, :98:31, :99:28, :101:30]
        end
        state_reg <=
          {~(state_reg_touch_way_sized[2]),
           state_reg_touch_way_sized[2]
             ? {~(state_reg_touch_way_sized[1]),
                state_reg_touch_way_sized[1]
                  ? ~(state_reg_touch_way_sized[0])
                  : state_reg[4],
                state_reg_touch_way_sized[1]
                  ? state_reg[3]
                  : ~(state_reg_touch_way_sized[0])}
             : state_reg[5:3],
           state_reg_touch_way_sized[2]
             ? state_reg[2:0]
             : {~(state_reg_touch_way_sized[1]),
                state_reg_touch_way_sized[1]
                  ? ~(state_reg_touch_way_sized[0])
                  : state_reg[1],
                state_reg_touch_way_sized[1]
                  ? state_reg[0]
                  : ~(state_reg_touch_way_sized[0])}};	// @[rocket-chip/src/main/scala/util/Replacement.scala:168:72, :196:{33,43}, :198:38, :202:12, :203:16, :206:16, :218:7, :245:38, rocket-chip/src/main/scala/util/package.scala:155:13, src/main/scala/xiangshan/frontend/WrBypass.scala:87:37]
      end
      ever_written_0 <= io_wen & ~hit & _GEN | ever_written_0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29, :63:29, :92:19, :93:18, :98:31]
      ever_written_1 <= io_wen & ~hit & _GEN_0 | ever_written_1;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29, :63:29, :92:19, :93:18, :98:31]
      ever_written_2 <= io_wen & ~hit & _GEN_1 | ever_written_2;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29, :63:29, :92:19, :93:18, :98:31]
      ever_written_3 <= io_wen & ~hit & _GEN_2 | ever_written_3;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29, :63:29, :92:19, :93:18, :98:31]
      ever_written_4 <= io_wen & ~hit & _GEN_3 | ever_written_4;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29, :63:29, :92:19, :93:18, :98:31]
      ever_written_5 <= io_wen & ~hit & _GEN_4 | ever_written_5;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29, :63:29, :92:19, :93:18, :98:31]
      ever_written_6 <= io_wen & ~hit & _GEN_5 | ever_written_6;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:57:29, :63:29, :92:19, :93:18, :98:31]
      ever_written_7 <= io_wen & ~hit & (&enq_idx) | ever_written_7;	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/xiangshan/frontend/WrBypass.scala:57:29, :63:29, :92:19, :93:18, :98:31]
    end
  end // always @(posedge, posedge)
  `ifdef ENABLE_INITIAL_REG_	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
    `ifdef FIRRTL_BEFORE_INITIAL	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
      `FIRRTL_BEFORE_INITIAL	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
    `endif // FIRRTL_BEFORE_INITIAL
    logic [31:0] _RANDOM[0:0];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
    initial begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
      `ifdef INIT_RANDOM_PROLOG_	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
        `INIT_RANDOM_PROLOG_	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
      `endif // INIT_RANDOM_PROLOG_
      `ifdef RANDOMIZE_REG_INIT	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
        _RANDOM[/*Zero width*/ 1'b0] = `RANDOM;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
        valids_0_0 = _RANDOM[/*Zero width*/ 1'b0][0];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_1_0 = _RANDOM[/*Zero width*/ 1'b0][1];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_2_0 = _RANDOM[/*Zero width*/ 1'b0][2];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_3_0 = _RANDOM[/*Zero width*/ 1'b0][3];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_4_0 = _RANDOM[/*Zero width*/ 1'b0][4];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_5_0 = _RANDOM[/*Zero width*/ 1'b0][5];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_6_0 = _RANDOM[/*Zero width*/ 1'b0][6];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_7_0 = _RANDOM[/*Zero width*/ 1'b0][7];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        ever_written_0 = _RANDOM[/*Zero width*/ 1'b0][8];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23, :57:29]
        ever_written_1 = _RANDOM[/*Zero width*/ 1'b0][9];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23, :57:29]
        ever_written_2 = _RANDOM[/*Zero width*/ 1'b0][10];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23, :57:29]
        ever_written_3 = _RANDOM[/*Zero width*/ 1'b0][11];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23, :57:29]
        ever_written_4 = _RANDOM[/*Zero width*/ 1'b0][12];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23, :57:29]
        ever_written_5 = _RANDOM[/*Zero width*/ 1'b0][13];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23, :57:29]
        ever_written_6 = _RANDOM[/*Zero width*/ 1'b0][14];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23, :57:29]
        ever_written_7 = _RANDOM[/*Zero width*/ 1'b0][15];	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23, :57:29]
        state_reg = _RANDOM[/*Zero width*/ 1'b0][22:16];	// @[rocket-chip/src/main/scala/util/Replacement.scala:168:72, src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
      `endif // RANDOMIZE_REG_INIT
      if (reset) begin	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
        valids_0_0 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_1_0 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_2_0 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_3_0 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_4_0 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_5_0 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_6_0 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        valids_7_0 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23]
        ever_written_0 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
        ever_written_1 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
        ever_written_2 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
        ever_written_3 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
        ever_written_4 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
        ever_written_5 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
        ever_written_6 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
        ever_written_7 = 1'h0;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :57:29]
        state_reg = 7'h0;	// @[rocket-chip/src/main/scala/util/Replacement.scala:168:72]
      end
    end // initial
    `ifdef FIRRTL_AFTER_INITIAL	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
      `FIRRTL_AFTER_INITIAL	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
    `endif // FIRRTL_AFTER_INITIAL
  `endif // ENABLE_INITIAL_REG_
  CAMTemplate idx_tag_cam (	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:53:27]
    .clock              (clock),
    .io_r_req_0_idx     (io_write_idx),
    .io_r_resp_0_0      (_idx_tag_cam_io_r_resp_0_0),
    .io_r_resp_0_1      (_idx_tag_cam_io_r_resp_0_1),
    .io_r_resp_0_2      (_idx_tag_cam_io_r_resp_0_2),
    .io_r_resp_0_3      (_idx_tag_cam_io_r_resp_0_3),
    .io_r_resp_0_4      (_idx_tag_cam_io_r_resp_0_4),
    .io_r_resp_0_5      (_idx_tag_cam_io_r_resp_0_5),
    .io_r_resp_0_6      (_idx_tag_cam_io_r_resp_0_6),
    .io_r_resp_0_7      (_idx_tag_cam_io_r_resp_0_7),
    .io_w_valid         (io_wen & ~hit),	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:63:29, :107:{23,26}]
    .io_w_bits_data_idx (io_write_idx),
    .io_w_bits_index    (enq_idx)	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12]
  );
  data_mem_0_8x3 data_mem_0_ext (	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:54:21]
    .R0_addr (hit_idx),	// @[src/main/scala/chisel3/util/OneHot.scala:32:10]
    .R0_en   (1'h1),	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7]
    .R0_clk  (clock),
    .R0_data (io_hit_data_0_bits),
    .W0_addr (hit ? hit_idx : enq_idx),	// @[rocket-chip/src/main/scala/util/Replacement.scala:249:12, src/main/scala/chisel3/util/OneHot.scala:32:10, src/main/scala/xiangshan/frontend/WrBypass.scala:63:29, :83:29]
    .W0_en   (io_wen),
    .W0_clk  (clock),
    .W0_data (io_write_data_0)
  );
  assign io_hit = hit;	// @[src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :63:29]
  assign io_hit_data_0_valid =
    hits_oh_0 & valids_0_0 | hits_oh_1 & valids_1_0 | hits_oh_2 & valids_2_0 | hits_oh_3
    & valids_3_0 | hits_oh_4 & valids_4_0 | hits_oh_5 & valids_5_0 | hits_oh_6
    & valids_6_0 | hits_oh_7 & valids_7_0;	// @[src/main/scala/chisel3/util/Mux.scala:30:73, src/main/scala/xiangshan/frontend/WrBypass.scala:26:7, :56:23, :61:83]
endmodule

