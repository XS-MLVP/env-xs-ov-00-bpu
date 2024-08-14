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

module WrBypass_33(
  input        clock,
  input        reset,
  input        io_wen,
  input  [7:0] io_write_idx,
  input  [5:0] io_write_data_0,
  input  [5:0] io_write_data_1,
  input        io_write_way_mask_0,
  input        io_write_way_mask_1,
  output       io_hit,
  output       io_hit_data_0_valid,
  output [5:0] io_hit_data_0_bits,
  output       io_hit_data_1_valid,
  output [5:0] io_hit_data_1_bits
);

  wire [11:0] _data_mem_ext_R0_data;
  wire [11:0] _data_mem_ext_R1_data;
  wire        _idx_tag_cam_io_r_resp_0_0;
  wire        _idx_tag_cam_io_r_resp_0_1;
  wire        _idx_tag_cam_io_r_resp_0_2;
  wire        _idx_tag_cam_io_r_resp_0_3;
  wire        _idx_tag_cam_io_r_resp_0_4;
  wire        _idx_tag_cam_io_r_resp_0_5;
  wire        _idx_tag_cam_io_r_resp_0_6;
  wire        _idx_tag_cam_io_r_resp_0_7;
  wire        _idx_tag_cam_io_r_resp_0_8;
  wire        _idx_tag_cam_io_r_resp_0_9;
  wire        _idx_tag_cam_io_r_resp_0_10;
  wire        _idx_tag_cam_io_r_resp_0_11;
  wire        _idx_tag_cam_io_r_resp_0_12;
  wire        _idx_tag_cam_io_r_resp_0_13;
  wire        _idx_tag_cam_io_r_resp_0_14;
  wire        _idx_tag_cam_io_r_resp_0_15;
  reg         valids_0_0;
  reg         valids_0_1;
  reg         valids_1_0;
  reg         valids_1_1;
  reg         valids_2_0;
  reg         valids_2_1;
  reg         valids_3_0;
  reg         valids_3_1;
  reg         valids_4_0;
  reg         valids_4_1;
  reg         valids_5_0;
  reg         valids_5_1;
  reg         valids_6_0;
  reg         valids_6_1;
  reg         valids_7_0;
  reg         valids_7_1;
  reg         valids_8_0;
  reg         valids_8_1;
  reg         valids_9_0;
  reg         valids_9_1;
  reg         valids_10_0;
  reg         valids_10_1;
  reg         valids_11_0;
  reg         valids_11_1;
  reg         valids_12_0;
  reg         valids_12_1;
  reg         valids_13_0;
  reg         valids_13_1;
  reg         valids_14_0;
  reg         valids_14_1;
  reg         valids_15_0;
  reg         valids_15_1;
  reg         ever_written_0;
  reg         ever_written_1;
  reg         ever_written_2;
  reg         ever_written_3;
  reg         ever_written_4;
  reg         ever_written_5;
  reg         ever_written_6;
  reg         ever_written_7;
  reg         ever_written_8;
  reg         ever_written_9;
  reg         ever_written_10;
  reg         ever_written_11;
  reg         ever_written_12;
  reg         ever_written_13;
  reg         ever_written_14;
  reg         ever_written_15;
  wire        hits_oh_0 = _idx_tag_cam_io_r_resp_0_0 & ever_written_0;
  wire        hits_oh_1 = _idx_tag_cam_io_r_resp_0_1 & ever_written_1;
  wire        hits_oh_2 = _idx_tag_cam_io_r_resp_0_2 & ever_written_2;
  wire        hits_oh_3 = _idx_tag_cam_io_r_resp_0_3 & ever_written_3;
  wire        hits_oh_4 = _idx_tag_cam_io_r_resp_0_4 & ever_written_4;
  wire        hits_oh_5 = _idx_tag_cam_io_r_resp_0_5 & ever_written_5;
  wire        hits_oh_6 = _idx_tag_cam_io_r_resp_0_6 & ever_written_6;
  wire        hits_oh_7 = _idx_tag_cam_io_r_resp_0_7 & ever_written_7;
  wire        hits_oh_8 = _idx_tag_cam_io_r_resp_0_8 & ever_written_8;
  wire        hits_oh_9 = _idx_tag_cam_io_r_resp_0_9 & ever_written_9;
  wire        hits_oh_10 = _idx_tag_cam_io_r_resp_0_10 & ever_written_10;
  wire        hits_oh_11 = _idx_tag_cam_io_r_resp_0_11 & ever_written_11;
  wire        hits_oh_12 = _idx_tag_cam_io_r_resp_0_12 & ever_written_12;
  wire        hits_oh_13 = _idx_tag_cam_io_r_resp_0_13 & ever_written_13;
  wire        hits_oh_14 = _idx_tag_cam_io_r_resp_0_14 & ever_written_14;
  wire        hits_oh_15 = _idx_tag_cam_io_r_resp_0_15 & ever_written_15;
  wire [6:0]  _hit_idx_T_2 =
    {hits_oh_15, hits_oh_14, hits_oh_13, hits_oh_12, hits_oh_11, hits_oh_10, hits_oh_9}
    | {hits_oh_7, hits_oh_6, hits_oh_5, hits_oh_4, hits_oh_3, hits_oh_2, hits_oh_1};
  wire [2:0]  _hit_idx_T_4 = _hit_idx_T_2[6:4] | _hit_idx_T_2[2:0];
  wire [3:0]  hit_idx =
    {|{hits_oh_15,
       hits_oh_14,
       hits_oh_13,
       hits_oh_12,
       hits_oh_11,
       hits_oh_10,
       hits_oh_9,
       hits_oh_8},
     |(_hit_idx_T_2[6:3]),
     |(_hit_idx_T_4[2:1]),
     _hit_idx_T_4[2] | _hit_idx_T_4[0]};
  wire        hit =
    hits_oh_0 | hits_oh_1 | hits_oh_2 | hits_oh_3 | hits_oh_4 | hits_oh_5 | hits_oh_6
    | hits_oh_7 | hits_oh_8 | hits_oh_9 | hits_oh_10 | hits_oh_11 | hits_oh_12
    | hits_oh_13 | hits_oh_14 | hits_oh_15;
  reg  [14:0] state_reg;
  wire [3:0]  enq_idx =
    {state_reg[14],
     state_reg[14]
       ? {state_reg[13],
          state_reg[13]
            ? {state_reg[12], state_reg[12] ? state_reg[11] : state_reg[10]}
            : {state_reg[9], state_reg[9] ? state_reg[8] : state_reg[7]}}
       : {state_reg[6],
          state_reg[6]
            ? {state_reg[5], state_reg[5] ? state_reg[4] : state_reg[3]}
            : {state_reg[2], state_reg[2] ? state_reg[1] : state_reg[0]}}};
  wire        _GEN = hit_idx == 4'h0;
  wire        _GEN_0 = hit_idx == 4'h1;
  wire        _GEN_1 = hit_idx == 4'h2;
  wire        _GEN_2 = hit_idx == 4'h3;
  wire        _GEN_3 = hit_idx == 4'h4;
  wire        _GEN_4 = hit_idx == 4'h5;
  wire        _GEN_5 = hit_idx == 4'h6;
  wire        _GEN_6 = hit_idx == 4'h7;
  wire        _GEN_7 = hit_idx == 4'h8;
  wire        _GEN_8 = hit_idx == 4'h9;
  wire        _GEN_9 = hit_idx == 4'hA;
  wire        _GEN_10 = hit_idx == 4'hB;
  wire        _GEN_11 = hit_idx == 4'hC;
  wire        _GEN_12 = hit_idx == 4'hD;
  wire        _GEN_13 = hit_idx == 4'hE;
  wire [3:0]  state_reg_touch_way_sized = hit ? hit_idx : enq_idx;
  wire        _GEN_14 = enq_idx == 4'h0;
  wire        _GEN_15 = enq_idx == 4'h1;
  wire        _GEN_16 = enq_idx == 4'h2;
  wire        _GEN_17 = enq_idx == 4'h3;
  wire        _GEN_18 = enq_idx == 4'h4;
  wire        _GEN_19 = enq_idx == 4'h5;
  wire        _GEN_20 = enq_idx == 4'h6;
  wire        _GEN_21 = enq_idx == 4'h7;
  wire        _GEN_22 = enq_idx == 4'h8;
  wire        _GEN_23 = enq_idx == 4'h9;
  wire        _GEN_24 = enq_idx == 4'hA;
  wire        _GEN_25 = enq_idx == 4'hB;
  wire        _GEN_26 = enq_idx == 4'hC;
  wire        _GEN_27 = enq_idx == 4'hD;
  wire        _GEN_28 = enq_idx == 4'hE;
  always @(posedge clock or posedge reset) begin
    if (reset) begin
      valids_0_0 <= 1'h0;
      valids_0_1 <= 1'h0;
      valids_1_0 <= 1'h0;
      valids_1_1 <= 1'h0;
      valids_2_0 <= 1'h0;
      valids_2_1 <= 1'h0;
      valids_3_0 <= 1'h0;
      valids_3_1 <= 1'h0;
      valids_4_0 <= 1'h0;
      valids_4_1 <= 1'h0;
      valids_5_0 <= 1'h0;
      valids_5_1 <= 1'h0;
      valids_6_0 <= 1'h0;
      valids_6_1 <= 1'h0;
      valids_7_0 <= 1'h0;
      valids_7_1 <= 1'h0;
      valids_8_0 <= 1'h0;
      valids_8_1 <= 1'h0;
      valids_9_0 <= 1'h0;
      valids_9_1 <= 1'h0;
      valids_10_0 <= 1'h0;
      valids_10_1 <= 1'h0;
      valids_11_0 <= 1'h0;
      valids_11_1 <= 1'h0;
      valids_12_0 <= 1'h0;
      valids_12_1 <= 1'h0;
      valids_13_0 <= 1'h0;
      valids_13_1 <= 1'h0;
      valids_14_0 <= 1'h0;
      valids_14_1 <= 1'h0;
      valids_15_0 <= 1'h0;
      valids_15_1 <= 1'h0;
      ever_written_0 <= 1'h0;
      ever_written_1 <= 1'h0;
      ever_written_2 <= 1'h0;
      ever_written_3 <= 1'h0;
      ever_written_4 <= 1'h0;
      ever_written_5 <= 1'h0;
      ever_written_6 <= 1'h0;
      ever_written_7 <= 1'h0;
      ever_written_8 <= 1'h0;
      ever_written_9 <= 1'h0;
      ever_written_10 <= 1'h0;
      ever_written_11 <= 1'h0;
      ever_written_12 <= 1'h0;
      ever_written_13 <= 1'h0;
      ever_written_14 <= 1'h0;
      ever_written_15 <= 1'h0;
      state_reg <= 15'h0;
    end
    else begin
      if (io_wen) begin
        if (hit) begin
          valids_0_0 <= io_write_way_mask_0 & _GEN | valids_0_0;
          valids_0_1 <= io_write_way_mask_1 & _GEN | valids_0_1;
          valids_1_0 <= io_write_way_mask_0 & _GEN_0 | valids_1_0;
          valids_1_1 <= io_write_way_mask_1 & _GEN_0 | valids_1_1;
          valids_2_0 <= io_write_way_mask_0 & _GEN_1 | valids_2_0;
          valids_2_1 <= io_write_way_mask_1 & _GEN_1 | valids_2_1;
          valids_3_0 <= io_write_way_mask_0 & _GEN_2 | valids_3_0;
          valids_3_1 <= io_write_way_mask_1 & _GEN_2 | valids_3_1;
          valids_4_0 <= io_write_way_mask_0 & _GEN_3 | valids_4_0;
          valids_4_1 <= io_write_way_mask_1 & _GEN_3 | valids_4_1;
          valids_5_0 <= io_write_way_mask_0 & _GEN_4 | valids_5_0;
          valids_5_1 <= io_write_way_mask_1 & _GEN_4 | valids_5_1;
          valids_6_0 <= io_write_way_mask_0 & _GEN_5 | valids_6_0;
          valids_6_1 <= io_write_way_mask_1 & _GEN_5 | valids_6_1;
          valids_7_0 <= io_write_way_mask_0 & _GEN_6 | valids_7_0;
          valids_7_1 <= io_write_way_mask_1 & _GEN_6 | valids_7_1;
          valids_8_0 <= io_write_way_mask_0 & _GEN_7 | valids_8_0;
          valids_8_1 <= io_write_way_mask_1 & _GEN_7 | valids_8_1;
          valids_9_0 <= io_write_way_mask_0 & _GEN_8 | valids_9_0;
          valids_9_1 <= io_write_way_mask_1 & _GEN_8 | valids_9_1;
          valids_10_0 <= io_write_way_mask_0 & _GEN_9 | valids_10_0;
          valids_10_1 <= io_write_way_mask_1 & _GEN_9 | valids_10_1;
          valids_11_0 <= io_write_way_mask_0 & _GEN_10 | valids_11_0;
          valids_11_1 <= io_write_way_mask_1 & _GEN_10 | valids_11_1;
          valids_12_0 <= io_write_way_mask_0 & _GEN_11 | valids_12_0;
          valids_12_1 <= io_write_way_mask_1 & _GEN_11 | valids_12_1;
          valids_13_0 <= io_write_way_mask_0 & _GEN_12 | valids_13_0;
          valids_13_1 <= io_write_way_mask_1 & _GEN_12 | valids_13_1;
          valids_14_0 <= io_write_way_mask_0 & _GEN_13 | valids_14_0;
          valids_14_1 <= io_write_way_mask_1 & _GEN_13 | valids_14_1;
          valids_15_0 <= io_write_way_mask_0 & (&hit_idx) | valids_15_0;
          valids_15_1 <= io_write_way_mask_1 & (&hit_idx) | valids_15_1;
        end
        else begin
          valids_0_0 <= io_write_way_mask_0 & _GEN_14 | ~_GEN_14 & valids_0_0;
          valids_0_1 <= io_write_way_mask_1 & _GEN_14 | ~_GEN_14 & valids_0_1;
          valids_1_0 <= io_write_way_mask_0 & _GEN_15 | ~_GEN_15 & valids_1_0;
          valids_1_1 <= io_write_way_mask_1 & _GEN_15 | ~_GEN_15 & valids_1_1;
          valids_2_0 <= io_write_way_mask_0 & _GEN_16 | ~_GEN_16 & valids_2_0;
          valids_2_1 <= io_write_way_mask_1 & _GEN_16 | ~_GEN_16 & valids_2_1;
          valids_3_0 <= io_write_way_mask_0 & _GEN_17 | ~_GEN_17 & valids_3_0;
          valids_3_1 <= io_write_way_mask_1 & _GEN_17 | ~_GEN_17 & valids_3_1;
          valids_4_0 <= io_write_way_mask_0 & _GEN_18 | ~_GEN_18 & valids_4_0;
          valids_4_1 <= io_write_way_mask_1 & _GEN_18 | ~_GEN_18 & valids_4_1;
          valids_5_0 <= io_write_way_mask_0 & _GEN_19 | ~_GEN_19 & valids_5_0;
          valids_5_1 <= io_write_way_mask_1 & _GEN_19 | ~_GEN_19 & valids_5_1;
          valids_6_0 <= io_write_way_mask_0 & _GEN_20 | ~_GEN_20 & valids_6_0;
          valids_6_1 <= io_write_way_mask_1 & _GEN_20 | ~_GEN_20 & valids_6_1;
          valids_7_0 <= io_write_way_mask_0 & _GEN_21 | ~_GEN_21 & valids_7_0;
          valids_7_1 <= io_write_way_mask_1 & _GEN_21 | ~_GEN_21 & valids_7_1;
          valids_8_0 <= io_write_way_mask_0 & _GEN_22 | ~_GEN_22 & valids_8_0;
          valids_8_1 <= io_write_way_mask_1 & _GEN_22 | ~_GEN_22 & valids_8_1;
          valids_9_0 <= io_write_way_mask_0 & _GEN_23 | ~_GEN_23 & valids_9_0;
          valids_9_1 <= io_write_way_mask_1 & _GEN_23 | ~_GEN_23 & valids_9_1;
          valids_10_0 <= io_write_way_mask_0 & _GEN_24 | ~_GEN_24 & valids_10_0;
          valids_10_1 <= io_write_way_mask_1 & _GEN_24 | ~_GEN_24 & valids_10_1;
          valids_11_0 <= io_write_way_mask_0 & _GEN_25 | ~_GEN_25 & valids_11_0;
          valids_11_1 <= io_write_way_mask_1 & _GEN_25 | ~_GEN_25 & valids_11_1;
          valids_12_0 <= io_write_way_mask_0 & _GEN_26 | ~_GEN_26 & valids_12_0;
          valids_12_1 <= io_write_way_mask_1 & _GEN_26 | ~_GEN_26 & valids_12_1;
          valids_13_0 <= io_write_way_mask_0 & _GEN_27 | ~_GEN_27 & valids_13_0;
          valids_13_1 <= io_write_way_mask_1 & _GEN_27 | ~_GEN_27 & valids_13_1;
          valids_14_0 <= io_write_way_mask_0 & _GEN_28 | ~_GEN_28 & valids_14_0;
          valids_14_1 <= io_write_way_mask_1 & _GEN_28 | ~_GEN_28 & valids_14_1;
          valids_15_0 <= io_write_way_mask_0 & (&enq_idx) | ~(&enq_idx) & valids_15_0;
          valids_15_1 <= io_write_way_mask_1 & (&enq_idx) | ~(&enq_idx) & valids_15_1;
        end
        state_reg <=
          {~(state_reg_touch_way_sized[3]),
           state_reg_touch_way_sized[3]
             ? {~(state_reg_touch_way_sized[2]),
                state_reg_touch_way_sized[2]
                  ? {~(state_reg_touch_way_sized[1]),
                     state_reg_touch_way_sized[1]
                       ? ~(state_reg_touch_way_sized[0])
                       : state_reg[11],
                     state_reg_touch_way_sized[1]
                       ? state_reg[10]
                       : ~(state_reg_touch_way_sized[0])}
                  : state_reg[12:10],
                state_reg_touch_way_sized[2]
                  ? state_reg[9:7]
                  : {~(state_reg_touch_way_sized[1]),
                     state_reg_touch_way_sized[1]
                       ? ~(state_reg_touch_way_sized[0])
                       : state_reg[8],
                     state_reg_touch_way_sized[1]
                       ? state_reg[7]
                       : ~(state_reg_touch_way_sized[0])}}
             : state_reg[13:7],
           state_reg_touch_way_sized[3]
             ? state_reg[6:0]
             : {~(state_reg_touch_way_sized[2]),
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
                       : ~(state_reg_touch_way_sized[0])}}};
      end
      ever_written_0 <= io_wen & ~hit & (_GEN_14 | io_wen & _GEN_14) | ever_written_0;
      ever_written_1 <= io_wen & ~hit & (_GEN_15 | io_wen & _GEN_15) | ever_written_1;
      ever_written_2 <= io_wen & ~hit & (_GEN_16 | io_wen & _GEN_16) | ever_written_2;
      ever_written_3 <= io_wen & ~hit & (_GEN_17 | io_wen & _GEN_17) | ever_written_3;
      ever_written_4 <= io_wen & ~hit & (_GEN_18 | io_wen & _GEN_18) | ever_written_4;
      ever_written_5 <= io_wen & ~hit & (_GEN_19 | io_wen & _GEN_19) | ever_written_5;
      ever_written_6 <= io_wen & ~hit & (_GEN_20 | io_wen & _GEN_20) | ever_written_6;
      ever_written_7 <= io_wen & ~hit & (_GEN_21 | io_wen & _GEN_21) | ever_written_7;
      ever_written_8 <= io_wen & ~hit & (_GEN_22 | io_wen & _GEN_22) | ever_written_8;
      ever_written_9 <= io_wen & ~hit & (_GEN_23 | io_wen & _GEN_23) | ever_written_9;
      ever_written_10 <= io_wen & ~hit & (_GEN_24 | io_wen & _GEN_24) | ever_written_10;
      ever_written_11 <= io_wen & ~hit & (_GEN_25 | io_wen & _GEN_25) | ever_written_11;
      ever_written_12 <= io_wen & ~hit & (_GEN_26 | io_wen & _GEN_26) | ever_written_12;
      ever_written_13 <= io_wen & ~hit & (_GEN_27 | io_wen & _GEN_27) | ever_written_13;
      ever_written_14 <= io_wen & ~hit & (_GEN_28 | io_wen & _GEN_28) | ever_written_14;
      ever_written_15 <=
        io_wen & ~hit & ((&enq_idx) | io_wen & (&enq_idx)) | ever_written_15;
    end
  end // always @(posedge, posedge)
  `ifdef ENABLE_INITIAL_REG_
    `ifdef FIRRTL_BEFORE_INITIAL
      `FIRRTL_BEFORE_INITIAL
    `endif // FIRRTL_BEFORE_INITIAL
    logic [31:0] _RANDOM[0:1];
    initial begin
      `ifdef INIT_RANDOM_PROLOG_
        `INIT_RANDOM_PROLOG_
      `endif // INIT_RANDOM_PROLOG_
      `ifdef RANDOMIZE_REG_INIT
        for (logic [1:0] i = 2'h0; i < 2'h2; i += 2'h1) begin
          _RANDOM[i[0]] = `RANDOM;
        end
        valids_0_0 = _RANDOM[1'h0][0];
        valids_0_1 = _RANDOM[1'h0][1];
        valids_1_0 = _RANDOM[1'h0][2];
        valids_1_1 = _RANDOM[1'h0][3];
        valids_2_0 = _RANDOM[1'h0][4];
        valids_2_1 = _RANDOM[1'h0][5];
        valids_3_0 = _RANDOM[1'h0][6];
        valids_3_1 = _RANDOM[1'h0][7];
        valids_4_0 = _RANDOM[1'h0][8];
        valids_4_1 = _RANDOM[1'h0][9];
        valids_5_0 = _RANDOM[1'h0][10];
        valids_5_1 = _RANDOM[1'h0][11];
        valids_6_0 = _RANDOM[1'h0][12];
        valids_6_1 = _RANDOM[1'h0][13];
        valids_7_0 = _RANDOM[1'h0][14];
        valids_7_1 = _RANDOM[1'h0][15];
        valids_8_0 = _RANDOM[1'h0][16];
        valids_8_1 = _RANDOM[1'h0][17];
        valids_9_0 = _RANDOM[1'h0][18];
        valids_9_1 = _RANDOM[1'h0][19];
        valids_10_0 = _RANDOM[1'h0][20];
        valids_10_1 = _RANDOM[1'h0][21];
        valids_11_0 = _RANDOM[1'h0][22];
        valids_11_1 = _RANDOM[1'h0][23];
        valids_12_0 = _RANDOM[1'h0][24];
        valids_12_1 = _RANDOM[1'h0][25];
        valids_13_0 = _RANDOM[1'h0][26];
        valids_13_1 = _RANDOM[1'h0][27];
        valids_14_0 = _RANDOM[1'h0][28];
        valids_14_1 = _RANDOM[1'h0][29];
        valids_15_0 = _RANDOM[1'h0][30];
        valids_15_1 = _RANDOM[1'h0][31];
        ever_written_0 = _RANDOM[1'h1][0];
        ever_written_1 = _RANDOM[1'h1][1];
        ever_written_2 = _RANDOM[1'h1][2];
        ever_written_3 = _RANDOM[1'h1][3];
        ever_written_4 = _RANDOM[1'h1][4];
        ever_written_5 = _RANDOM[1'h1][5];
        ever_written_6 = _RANDOM[1'h1][6];
        ever_written_7 = _RANDOM[1'h1][7];
        ever_written_8 = _RANDOM[1'h1][8];
        ever_written_9 = _RANDOM[1'h1][9];
        ever_written_10 = _RANDOM[1'h1][10];
        ever_written_11 = _RANDOM[1'h1][11];
        ever_written_12 = _RANDOM[1'h1][12];
        ever_written_13 = _RANDOM[1'h1][13];
        ever_written_14 = _RANDOM[1'h1][14];
        ever_written_15 = _RANDOM[1'h1][15];
        state_reg = _RANDOM[1'h1][30:16];
      `endif // RANDOMIZE_REG_INIT
      if (reset) begin
        valids_0_0 = 1'h0;
        valids_0_1 = 1'h0;
        valids_1_0 = 1'h0;
        valids_1_1 = 1'h0;
        valids_2_0 = 1'h0;
        valids_2_1 = 1'h0;
        valids_3_0 = 1'h0;
        valids_3_1 = 1'h0;
        valids_4_0 = 1'h0;
        valids_4_1 = 1'h0;
        valids_5_0 = 1'h0;
        valids_5_1 = 1'h0;
        valids_6_0 = 1'h0;
        valids_6_1 = 1'h0;
        valids_7_0 = 1'h0;
        valids_7_1 = 1'h0;
        valids_8_0 = 1'h0;
        valids_8_1 = 1'h0;
        valids_9_0 = 1'h0;
        valids_9_1 = 1'h0;
        valids_10_0 = 1'h0;
        valids_10_1 = 1'h0;
        valids_11_0 = 1'h0;
        valids_11_1 = 1'h0;
        valids_12_0 = 1'h0;
        valids_12_1 = 1'h0;
        valids_13_0 = 1'h0;
        valids_13_1 = 1'h0;
        valids_14_0 = 1'h0;
        valids_14_1 = 1'h0;
        valids_15_0 = 1'h0;
        valids_15_1 = 1'h0;
        ever_written_0 = 1'h0;
        ever_written_1 = 1'h0;
        ever_written_2 = 1'h0;
        ever_written_3 = 1'h0;
        ever_written_4 = 1'h0;
        ever_written_5 = 1'h0;
        ever_written_6 = 1'h0;
        ever_written_7 = 1'h0;
        ever_written_8 = 1'h0;
        ever_written_9 = 1'h0;
        ever_written_10 = 1'h0;
        ever_written_11 = 1'h0;
        ever_written_12 = 1'h0;
        ever_written_13 = 1'h0;
        ever_written_14 = 1'h0;
        ever_written_15 = 1'h0;
        state_reg = 15'h0;
      end
    end // initial
    `ifdef FIRRTL_AFTER_INITIAL
      `FIRRTL_AFTER_INITIAL
    `endif // FIRRTL_AFTER_INITIAL
  `endif // ENABLE_INITIAL_REG_
  CAMTemplate_33 idx_tag_cam (
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
    .io_r_resp_0_8      (_idx_tag_cam_io_r_resp_0_8),
    .io_r_resp_0_9      (_idx_tag_cam_io_r_resp_0_9),
    .io_r_resp_0_10     (_idx_tag_cam_io_r_resp_0_10),
    .io_r_resp_0_11     (_idx_tag_cam_io_r_resp_0_11),
    .io_r_resp_0_12     (_idx_tag_cam_io_r_resp_0_12),
    .io_r_resp_0_13     (_idx_tag_cam_io_r_resp_0_13),
    .io_r_resp_0_14     (_idx_tag_cam_io_r_resp_0_14),
    .io_r_resp_0_15     (_idx_tag_cam_io_r_resp_0_15),
    .io_w_valid         (io_wen & ~hit),
    .io_w_bits_data_idx (io_write_idx),
    .io_w_bits_index    (enq_idx)
  );
  data_mem_16x12 data_mem_ext (
    .R0_addr (hit_idx),
    .R0_en   (1'h1),
    .R0_clk  (clock),
    .R0_data (_data_mem_ext_R0_data),
    .R1_addr (hit_idx),
    .R1_en   (1'h1),
    .R1_clk  (clock),
    .R1_data (_data_mem_ext_R1_data),
    .W0_addr (hit ? hit_idx : enq_idx),
    .W0_en   (io_wen),
    .W0_clk  (clock),
    .W0_data ({io_write_data_1, io_write_data_0}),
    .W0_mask ({io_write_way_mask_1, io_write_way_mask_0})
  );
  assign io_hit = hit;
  assign io_hit_data_0_valid =
    hits_oh_0 & valids_0_0 | hits_oh_1 & valids_1_0 | hits_oh_2 & valids_2_0 | hits_oh_3
    & valids_3_0 | hits_oh_4 & valids_4_0 | hits_oh_5 & valids_5_0 | hits_oh_6
    & valids_6_0 | hits_oh_7 & valids_7_0 | hits_oh_8 & valids_8_0 | hits_oh_9
    & valids_9_0 | hits_oh_10 & valids_10_0 | hits_oh_11 & valids_11_0 | hits_oh_12
    & valids_12_0 | hits_oh_13 & valids_13_0 | hits_oh_14 & valids_14_0 | hits_oh_15
    & valids_15_0;
  assign io_hit_data_0_bits = _data_mem_ext_R1_data[5:0];
  assign io_hit_data_1_valid =
    hits_oh_0 & valids_0_1 | hits_oh_1 & valids_1_1 | hits_oh_2 & valids_2_1 | hits_oh_3
    & valids_3_1 | hits_oh_4 & valids_4_1 | hits_oh_5 & valids_5_1 | hits_oh_6
    & valids_6_1 | hits_oh_7 & valids_7_1 | hits_oh_8 & valids_8_1 | hits_oh_9
    & valids_9_1 | hits_oh_10 & valids_10_1 | hits_oh_11 & valids_11_1 | hits_oh_12
    & valids_12_1 | hits_oh_13 & valids_13_1 | hits_oh_14 & valids_14_1 | hits_oh_15
    & valids_15_1;
  assign io_hit_data_1_bits = _data_mem_ext_R0_data[11:6];
endmodule
