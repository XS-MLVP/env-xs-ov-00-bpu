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

module TageTable_3(
  input         clock,
  input         reset,
  output        io_req_ready,
  input         io_req_valid,
  input  [40:0] io_req_bits_pc,
  input  [10:0] io_req_bits_folded_hist_hist_16_folded_hist,
  input  [7:0]  io_req_bits_folded_hist_hist_8_folded_hist,
  input  [6:0]  io_req_bits_folded_hist_hist_5_folded_hist,
  output        io_resps_0_valid,
  output [2:0]  io_resps_0_bits_ctr,
  output        io_resps_0_bits_u,
  output        io_resps_0_bits_unconf,
  output        io_resps_1_valid,
  output [2:0]  io_resps_1_bits_ctr,
  output        io_resps_1_bits_u,
  output        io_resps_1_bits_unconf,
  input  [40:0] io_update_pc,
  input  [10:0] io_update_folded_hist_hist_16_folded_hist,
  input  [7:0]  io_update_folded_hist_hist_8_folded_hist,
  input  [6:0]  io_update_folded_hist_hist_5_folded_hist,
  input         io_update_mask_0,
  input         io_update_mask_1,
  input         io_update_takens_0,
  input         io_update_takens_1,
  input         io_update_alloc_0,
  input         io_update_alloc_1,
  input  [2:0]  io_update_oldCtrs_0,
  input  [2:0]  io_update_oldCtrs_1,
  input         io_update_uMask_0,
  input         io_update_uMask_1,
  input         io_update_us_0,
  input         io_update_us_1,
  input         io_update_reset_u_0,
  input         io_update_reset_u_1
);

  wire        per_bank_not_silent_update_3_1;
  wire        per_bank_not_silent_update_3_0;
  wire        per_bank_not_silent_update_2_1;
  wire        per_bank_not_silent_update_2_0;
  wire        per_bank_not_silent_update_1_1;
  wire        per_bank_not_silent_update_1_0;
  wire        per_bank_not_silent_update_0_1;
  wire        per_bank_not_silent_update_0_0;
  reg         powerOnResetState;
  wire        _resp_invalid_by_write_T_6;
  wire        _bank_wrbypasses_3_1_io_hit;
  wire        _bank_wrbypasses_3_1_io_hit_data_0_valid;
  wire [2:0]  _bank_wrbypasses_3_1_io_hit_data_0_bits;
  wire        _bank_wrbypasses_3_0_io_hit;
  wire        _bank_wrbypasses_3_0_io_hit_data_0_valid;
  wire [2:0]  _bank_wrbypasses_3_0_io_hit_data_0_bits;
  wire        _bank_wrbypasses_2_1_io_hit;
  wire        _bank_wrbypasses_2_1_io_hit_data_0_valid;
  wire [2:0]  _bank_wrbypasses_2_1_io_hit_data_0_bits;
  wire        _bank_wrbypasses_2_0_io_hit;
  wire        _bank_wrbypasses_2_0_io_hit_data_0_valid;
  wire [2:0]  _bank_wrbypasses_2_0_io_hit_data_0_bits;
  wire        _bank_wrbypasses_1_1_io_hit;
  wire        _bank_wrbypasses_1_1_io_hit_data_0_valid;
  wire [2:0]  _bank_wrbypasses_1_1_io_hit_data_0_bits;
  wire        _bank_wrbypasses_1_0_io_hit;
  wire        _bank_wrbypasses_1_0_io_hit_data_0_valid;
  wire [2:0]  _bank_wrbypasses_1_0_io_hit_data_0_bits;
  wire        _bank_wrbypasses_0_1_io_hit;
  wire        _bank_wrbypasses_0_1_io_hit_data_0_valid;
  wire [2:0]  _bank_wrbypasses_0_1_io_hit_data_0_bits;
  wire        _bank_wrbypasses_0_0_io_hit;
  wire        _bank_wrbypasses_0_0_io_hit_data_0_valid;
  wire [2:0]  _bank_wrbypasses_0_0_io_hit_data_0_bits;
  wire        _table_banks_3_io_r_req_ready;
  wire        _table_banks_3_io_r_resp_data_0_valid;
  wire [7:0]  _table_banks_3_io_r_resp_data_0_tag;
  wire [2:0]  _table_banks_3_io_r_resp_data_0_ctr;
  wire        _table_banks_3_io_r_resp_data_1_valid;
  wire [7:0]  _table_banks_3_io_r_resp_data_1_tag;
  wire [2:0]  _table_banks_3_io_r_resp_data_1_ctr;
  wire        _table_banks_2_io_r_req_ready;
  wire        _table_banks_2_io_r_resp_data_0_valid;
  wire [7:0]  _table_banks_2_io_r_resp_data_0_tag;
  wire [2:0]  _table_banks_2_io_r_resp_data_0_ctr;
  wire        _table_banks_2_io_r_resp_data_1_valid;
  wire [7:0]  _table_banks_2_io_r_resp_data_1_tag;
  wire [2:0]  _table_banks_2_io_r_resp_data_1_ctr;
  wire        _table_banks_1_io_r_req_ready;
  wire        _table_banks_1_io_r_resp_data_0_valid;
  wire [7:0]  _table_banks_1_io_r_resp_data_0_tag;
  wire [2:0]  _table_banks_1_io_r_resp_data_0_ctr;
  wire        _table_banks_1_io_r_resp_data_1_valid;
  wire [7:0]  _table_banks_1_io_r_resp_data_1_tag;
  wire [2:0]  _table_banks_1_io_r_resp_data_1_ctr;
  wire        _table_banks_0_io_r_req_ready;
  wire        _table_banks_0_io_r_resp_data_0_valid;
  wire [7:0]  _table_banks_0_io_r_resp_data_0_tag;
  wire [2:0]  _table_banks_0_io_r_resp_data_0_ctr;
  wire        _table_banks_0_io_r_resp_data_1_valid;
  wire [7:0]  _table_banks_0_io_r_resp_data_1_tag;
  wire [2:0]  _table_banks_0_io_r_resp_data_1_ctr;
  wire        _us_io_r_req_ready;
  wire        _us_io_r_resp_data_0;
  wire        _us_io_r_resp_data_1;
  wire        _us_extra_reset_T_1 = io_update_mask_0 | io_update_mask_1;
  wire [10:0] s0_idx = io_req_bits_pc[11:1] ^ io_req_bits_folded_hist_hist_16_folded_hist;
  wire        s0_bank_req_1h_0 = s0_idx[1:0] == 2'h0;
  wire        s0_bank_req_1h_1 = s0_idx[1:0] == 2'h1;
  wire        s0_bank_req_1h_2 = s0_idx[1:0] == 2'h2;
  wire        _s1_bank_req_1h_T = ~powerOnResetState & io_req_valid;
  reg  [39:0] s1_unhashed_idx;
  reg  [7:0]  s1_tag;
  reg         s1_bank_req_1h_0;
  reg         s1_bank_req_1h_1;
  reg         s1_bank_req_1h_2;
  reg         s1_bank_req_1h_3;
  reg         s1_bank_has_write_on_this_req_0;
  reg         s1_bank_has_write_on_this_req_1;
  reg         s1_bank_has_write_on_this_req_2;
  reg         s1_bank_has_write_on_this_req_3;
  wire [2:0]  _resp_selected_T_6 =
    (s1_bank_req_1h_0 ? _table_banks_0_io_r_resp_data_0_ctr : 3'h0)
    | (s1_bank_req_1h_1 ? _table_banks_1_io_r_resp_data_0_ctr : 3'h0)
    | (s1_bank_req_1h_2 ? _table_banks_2_io_r_resp_data_0_ctr : 3'h0)
    | (s1_bank_req_1h_3 ? _table_banks_3_io_r_resp_data_0_ctr : 3'h0);
  wire [2:0]  _resp_selected_T_27 =
    (s1_bank_req_1h_0 ? _table_banks_0_io_r_resp_data_1_ctr : 3'h0)
    | (s1_bank_req_1h_1 ? _table_banks_1_io_r_resp_data_1_ctr : 3'h0)
    | (s1_bank_req_1h_2 ? _table_banks_2_io_r_resp_data_1_ctr : 3'h0)
    | (s1_bank_req_1h_3 ? _table_banks_3_io_r_resp_data_1_ctr : 3'h0);
  wire        _unconf_selected_T_6 =
    s1_bank_req_1h_0
    & (_table_banks_0_io_r_resp_data_0_ctr == 3'h4
       | _table_banks_0_io_r_resp_data_0_ctr == 3'h3) | s1_bank_req_1h_1
    & (_table_banks_1_io_r_resp_data_0_ctr == 3'h4
       | _table_banks_1_io_r_resp_data_0_ctr == 3'h3) | s1_bank_req_1h_2
    & (_table_banks_2_io_r_resp_data_0_ctr == 3'h4
       | _table_banks_2_io_r_resp_data_0_ctr == 3'h3) | s1_bank_req_1h_3
    & (_table_banks_3_io_r_resp_data_0_ctr == 3'h4
       | _table_banks_3_io_r_resp_data_0_ctr == 3'h3);
  wire        _unconf_selected_T_13 =
    s1_bank_req_1h_0
    & (_table_banks_0_io_r_resp_data_1_ctr == 3'h4
       | _table_banks_0_io_r_resp_data_1_ctr == 3'h3) | s1_bank_req_1h_1
    & (_table_banks_1_io_r_resp_data_1_ctr == 3'h4
       | _table_banks_1_io_r_resp_data_1_ctr == 3'h3) | s1_bank_req_1h_2
    & (_table_banks_2_io_r_resp_data_1_ctr == 3'h4
       | _table_banks_2_io_r_resp_data_1_ctr == 3'h3) | s1_bank_req_1h_3
    & (_table_banks_3_io_r_resp_data_1_ctr == 3'h4
       | _table_banks_3_io_r_resp_data_1_ctr == 3'h3);
  wire        _hit_selected_T_6 =
    s1_bank_req_1h_0 & _table_banks_0_io_r_resp_data_0_tag == s1_tag
    & _table_banks_0_io_r_resp_data_0_valid & ~_resp_invalid_by_write_T_6
    | s1_bank_req_1h_1 & _table_banks_1_io_r_resp_data_0_tag == s1_tag
    & _table_banks_1_io_r_resp_data_0_valid & ~_resp_invalid_by_write_T_6
    | s1_bank_req_1h_2 & _table_banks_2_io_r_resp_data_0_tag == s1_tag
    & _table_banks_2_io_r_resp_data_0_valid & ~_resp_invalid_by_write_T_6
    | s1_bank_req_1h_3 & _table_banks_3_io_r_resp_data_0_tag == s1_tag
    & _table_banks_3_io_r_resp_data_0_valid & ~_resp_invalid_by_write_T_6;
  wire        _hit_selected_T_13 =
    s1_bank_req_1h_0 & _table_banks_0_io_r_resp_data_1_tag == s1_tag
    & _table_banks_0_io_r_resp_data_1_valid & ~_resp_invalid_by_write_T_6
    | s1_bank_req_1h_1 & _table_banks_1_io_r_resp_data_1_tag == s1_tag
    & _table_banks_1_io_r_resp_data_1_valid & ~_resp_invalid_by_write_T_6
    | s1_bank_req_1h_2 & _table_banks_2_io_r_resp_data_1_tag == s1_tag
    & _table_banks_2_io_r_resp_data_1_valid & ~_resp_invalid_by_write_T_6
    | s1_bank_req_1h_3 & _table_banks_3_io_r_resp_data_1_tag == s1_tag
    & _table_banks_3_io_r_resp_data_1_valid & ~_resp_invalid_by_write_T_6;
  assign _resp_invalid_by_write_T_6 =
    s1_bank_req_1h_0 & s1_bank_has_write_on_this_req_0 | s1_bank_req_1h_1
    & s1_bank_has_write_on_this_req_1 | s1_bank_req_1h_2 & s1_bank_has_write_on_this_req_2
    | s1_bank_req_1h_3 & s1_bank_has_write_on_this_req_3;
  wire [10:0] update_idx = io_update_pc[11:1] ^ io_update_folded_hist_hist_16_folded_hist;
  wire [7:0]  update_tag =
    io_update_pc[8:1] ^ io_update_folded_hist_hist_8_folded_hist
    ^ {io_update_folded_hist_hist_5_folded_hist, 1'h0};
  wire        update_req_bank_1h_0 = update_idx[1:0] == 2'h0;
  wire        update_req_bank_1h_1 = update_idx[1:0] == 2'h1;
  wire        update_req_bank_1h_2 = update_idx[1:0] == 2'h2;
  wire [1:0]  per_bank_update_way_mask_0 =
    {(io_update_pc[1] & io_update_mask_0 | ~(io_update_pc[1]) & io_update_mask_1)
       & per_bank_not_silent_update_0_1,
     (~(io_update_pc[1]) & io_update_mask_0 | io_update_pc[1] & io_update_mask_1)
       & per_bank_not_silent_update_0_0};
  wire [1:0]  per_bank_update_way_mask_1 =
    {(io_update_pc[1] & io_update_mask_0 | ~(io_update_pc[1]) & io_update_mask_1)
       & per_bank_not_silent_update_1_1,
     (~(io_update_pc[1]) & io_update_mask_0 | io_update_pc[1] & io_update_mask_1)
       & per_bank_not_silent_update_1_0};
  wire [1:0]  per_bank_update_way_mask_2 =
    {(io_update_pc[1] & io_update_mask_0 | ~(io_update_pc[1]) & io_update_mask_1)
       & per_bank_not_silent_update_2_1,
     (~(io_update_pc[1]) & io_update_mask_0 | io_update_pc[1] & io_update_mask_1)
       & per_bank_not_silent_update_2_0};
  wire [1:0]  per_bank_update_way_mask_3 =
    {(io_update_pc[1] & io_update_mask_0 | ~(io_update_pc[1]) & io_update_mask_1)
       & per_bank_not_silent_update_3_1,
     (~(io_update_pc[1]) & io_update_mask_0 | io_update_pc[1] & io_update_mask_1)
       & per_bank_not_silent_update_3_0};
  wire        _s1_bank_has_write_on_this_req_WIRE_0 =
    (|per_bank_update_way_mask_0) & update_req_bank_1h_0;
  wire        _s1_bank_has_write_on_this_req_WIRE_1 =
    (|per_bank_update_way_mask_1) & update_req_bank_1h_1;
  wire        _s1_bank_has_write_on_this_req_WIRE_2 =
    (|per_bank_update_way_mask_2) & update_req_bank_1h_2;
  wire        _s1_bank_has_write_on_this_req_WIRE_3 =
    (|per_bank_update_way_mask_3) & (&(update_idx[1:0]));
  wire [2:0]  _wrbypass_io_T_6 =
    (io_update_pc[1] ? 3'h0 : _bank_wrbypasses_0_0_io_hit_data_0_bits)
    | (io_update_pc[1] ? _bank_wrbypasses_0_1_io_hit_data_0_bits : 3'h0);
  wire        wrbypass_data_valid =
    (~(io_update_pc[1]) & _bank_wrbypasses_0_0_io_hit | io_update_pc[1]
     & _bank_wrbypasses_0_1_io_hit)
    & (~(io_update_pc[1]) & _bank_wrbypasses_0_0_io_hit_data_0_valid | io_update_pc[1]
       & _bank_wrbypasses_0_1_io_hit_data_0_valid);
  wire        _GEN = io_update_pc[1] ? io_update_takens_1 : io_update_takens_0;
  wire [2:0]  _GEN_0 = io_update_pc[1] ? io_update_oldCtrs_1 : io_update_oldCtrs_0;
  wire        _GEN_1 = (|_GEN_0) | _GEN;
  wire        _GEN_2 = io_update_pc[1] ? io_update_alloc_1 : io_update_alloc_0;
  wire [2:0]  per_bank_update_wdata_0_0_ctr =
    _GEN_2
      ? (_GEN ? 3'h4 : 3'h3)
      : wrbypass_data_valid
          ? ((&_wrbypass_io_T_6) & _GEN
               ? 3'h7
               : _wrbypass_io_T_6 == 3'h0 & ~_GEN
                   ? 3'h0
                   : _GEN ? 3'(_wrbypass_io_T_6 + 3'h1) : 3'(_wrbypass_io_T_6 - 3'h1))
          : (&_GEN_0) & _GEN
              ? 3'h7
              : _GEN_1 ? (_GEN ? 3'(_GEN_0 + 3'h1) : 3'(_GEN_0 - 3'h1)) : 3'h0;
  assign per_bank_not_silent_update_0_0 =
    (wrbypass_data_valid
       ? ~((&_wrbypass_io_T_6) & _GEN | _wrbypass_io_T_6 == 3'h0 & ~_GEN)
       : ~((&_GEN_0) & _GEN | _GEN_0 == 3'h0 & ~_GEN)) | _GEN_2;
  wire [2:0]  _wrbypass_io_T_28 =
    (io_update_pc[1] ? _bank_wrbypasses_0_0_io_hit_data_0_bits : 3'h0)
    | (io_update_pc[1] ? 3'h0 : _bank_wrbypasses_0_1_io_hit_data_0_bits);
  wire        wrbypass_data_valid_1 =
    (io_update_pc[1] & _bank_wrbypasses_0_0_io_hit | ~(io_update_pc[1])
     & _bank_wrbypasses_0_1_io_hit)
    & (io_update_pc[1] & _bank_wrbypasses_0_0_io_hit_data_0_valid | ~(io_update_pc[1])
       & _bank_wrbypasses_0_1_io_hit_data_0_valid);
  wire        _GEN_3 = io_update_pc[1] ? io_update_takens_0 : io_update_takens_1;
  wire [2:0]  _GEN_4 = io_update_pc[1] ? io_update_oldCtrs_0 : io_update_oldCtrs_1;
  wire        _GEN_5 = io_update_pc[1] ? io_update_alloc_0 : io_update_alloc_1;
  wire [2:0]  per_bank_update_wdata_0_1_ctr =
    _GEN_5
      ? (_GEN_3 ? 3'h4 : 3'h3)
      : wrbypass_data_valid_1
          ? ((&_wrbypass_io_T_28) & _GEN_3
               ? 3'h7
               : _wrbypass_io_T_28 == 3'h0 & ~_GEN_3
                   ? 3'h0
                   : _GEN_3 ? 3'(_wrbypass_io_T_28 + 3'h1) : 3'(_wrbypass_io_T_28 - 3'h1))
          : (&_GEN_4) & _GEN_3
              ? 3'h7
              : _GEN_4 == 3'h0 & ~_GEN_3
                  ? 3'h0
                  : _GEN_3 ? 3'(_GEN_4 + 3'h1) : 3'(_GEN_4 - 3'h1);
  assign per_bank_not_silent_update_0_1 =
    (wrbypass_data_valid_1
       ? ~((&_wrbypass_io_T_28) & _GEN_3 | _wrbypass_io_T_28 == 3'h0 & ~_GEN_3)
       : ~((&_GEN_4) & _GEN_3 | _GEN_4 == 3'h0 & ~_GEN_3)) | _GEN_5;
  wire [2:0]  _wrbypass_io_T_50 =
    (io_update_pc[1] ? 3'h0 : _bank_wrbypasses_1_0_io_hit_data_0_bits)
    | (io_update_pc[1] ? _bank_wrbypasses_1_1_io_hit_data_0_bits : 3'h0);
  wire        wrbypass_data_valid_2 =
    (~(io_update_pc[1]) & _bank_wrbypasses_1_0_io_hit | io_update_pc[1]
     & _bank_wrbypasses_1_1_io_hit)
    & (~(io_update_pc[1]) & _bank_wrbypasses_1_0_io_hit_data_0_valid | io_update_pc[1]
       & _bank_wrbypasses_1_1_io_hit_data_0_valid);
  wire [2:0]  per_bank_update_wdata_1_0_ctr =
    _GEN_2
      ? (_GEN ? 3'h4 : 3'h3)
      : wrbypass_data_valid_2
          ? ((&_wrbypass_io_T_50) & _GEN
               ? 3'h7
               : _wrbypass_io_T_50 == 3'h0 & ~_GEN
                   ? 3'h0
                   : _GEN ? 3'(_wrbypass_io_T_50 + 3'h1) : 3'(_wrbypass_io_T_50 - 3'h1))
          : (&_GEN_0) & _GEN
              ? 3'h7
              : _GEN_1 ? (_GEN ? 3'(_GEN_0 + 3'h1) : 3'(_GEN_0 - 3'h1)) : 3'h0;
  assign per_bank_not_silent_update_1_0 =
    (wrbypass_data_valid_2
       ? ~((&_wrbypass_io_T_50) & _GEN | _wrbypass_io_T_50 == 3'h0 & ~_GEN)
       : ~((&_GEN_0) & _GEN | _GEN_0 == 3'h0 & ~_GEN)) | _GEN_2;
  wire [2:0]  _wrbypass_io_T_72 =
    (io_update_pc[1] ? _bank_wrbypasses_1_0_io_hit_data_0_bits : 3'h0)
    | (io_update_pc[1] ? 3'h0 : _bank_wrbypasses_1_1_io_hit_data_0_bits);
  wire        wrbypass_data_valid_3 =
    (io_update_pc[1] & _bank_wrbypasses_1_0_io_hit | ~(io_update_pc[1])
     & _bank_wrbypasses_1_1_io_hit)
    & (io_update_pc[1] & _bank_wrbypasses_1_0_io_hit_data_0_valid | ~(io_update_pc[1])
       & _bank_wrbypasses_1_1_io_hit_data_0_valid);
  wire [2:0]  per_bank_update_wdata_1_1_ctr =
    _GEN_5
      ? (_GEN_3 ? 3'h4 : 3'h3)
      : wrbypass_data_valid_3
          ? ((&_wrbypass_io_T_72) & _GEN_3
               ? 3'h7
               : _wrbypass_io_T_72 == 3'h0 & ~_GEN_3
                   ? 3'h0
                   : _GEN_3 ? 3'(_wrbypass_io_T_72 + 3'h1) : 3'(_wrbypass_io_T_72 - 3'h1))
          : (&_GEN_4) & _GEN_3
              ? 3'h7
              : _GEN_4 == 3'h0 & ~_GEN_3
                  ? 3'h0
                  : _GEN_3 ? 3'(_GEN_4 + 3'h1) : 3'(_GEN_4 - 3'h1);
  assign per_bank_not_silent_update_1_1 =
    (wrbypass_data_valid_3
       ? ~((&_wrbypass_io_T_72) & _GEN_3 | _wrbypass_io_T_72 == 3'h0 & ~_GEN_3)
       : ~((&_GEN_4) & _GEN_3 | _GEN_4 == 3'h0 & ~_GEN_3)) | _GEN_5;
  wire [2:0]  _wrbypass_io_T_94 =
    (io_update_pc[1] ? 3'h0 : _bank_wrbypasses_2_0_io_hit_data_0_bits)
    | (io_update_pc[1] ? _bank_wrbypasses_2_1_io_hit_data_0_bits : 3'h0);
  wire        wrbypass_data_valid_4 =
    (~(io_update_pc[1]) & _bank_wrbypasses_2_0_io_hit | io_update_pc[1]
     & _bank_wrbypasses_2_1_io_hit)
    & (~(io_update_pc[1]) & _bank_wrbypasses_2_0_io_hit_data_0_valid | io_update_pc[1]
       & _bank_wrbypasses_2_1_io_hit_data_0_valid);
  wire [2:0]  per_bank_update_wdata_2_0_ctr =
    _GEN_2
      ? (_GEN ? 3'h4 : 3'h3)
      : wrbypass_data_valid_4
          ? ((&_wrbypass_io_T_94) & _GEN
               ? 3'h7
               : _wrbypass_io_T_94 == 3'h0 & ~_GEN
                   ? 3'h0
                   : _GEN ? 3'(_wrbypass_io_T_94 + 3'h1) : 3'(_wrbypass_io_T_94 - 3'h1))
          : (&_GEN_0) & _GEN
              ? 3'h7
              : _GEN_1 ? (_GEN ? 3'(_GEN_0 + 3'h1) : 3'(_GEN_0 - 3'h1)) : 3'h0;
  assign per_bank_not_silent_update_2_0 =
    (wrbypass_data_valid_4
       ? ~((&_wrbypass_io_T_94) & _GEN | _wrbypass_io_T_94 == 3'h0 & ~_GEN)
       : ~((&_GEN_0) & _GEN | _GEN_0 == 3'h0 & ~_GEN)) | _GEN_2;
  wire [2:0]  _wrbypass_io_T_116 =
    (io_update_pc[1] ? _bank_wrbypasses_2_0_io_hit_data_0_bits : 3'h0)
    | (io_update_pc[1] ? 3'h0 : _bank_wrbypasses_2_1_io_hit_data_0_bits);
  wire        wrbypass_data_valid_5 =
    (io_update_pc[1] & _bank_wrbypasses_2_0_io_hit | ~(io_update_pc[1])
     & _bank_wrbypasses_2_1_io_hit)
    & (io_update_pc[1] & _bank_wrbypasses_2_0_io_hit_data_0_valid | ~(io_update_pc[1])
       & _bank_wrbypasses_2_1_io_hit_data_0_valid);
  wire [2:0]  per_bank_update_wdata_2_1_ctr =
    _GEN_5
      ? (_GEN_3 ? 3'h4 : 3'h3)
      : wrbypass_data_valid_5
          ? ((&_wrbypass_io_T_116) & _GEN_3
               ? 3'h7
               : _wrbypass_io_T_116 == 3'h0 & ~_GEN_3
                   ? 3'h0
                   : _GEN_3
                       ? 3'(_wrbypass_io_T_116 + 3'h1)
                       : 3'(_wrbypass_io_T_116 - 3'h1))
          : (&_GEN_4) & _GEN_3
              ? 3'h7
              : _GEN_4 == 3'h0 & ~_GEN_3
                  ? 3'h0
                  : _GEN_3 ? 3'(_GEN_4 + 3'h1) : 3'(_GEN_4 - 3'h1);
  assign per_bank_not_silent_update_2_1 =
    (wrbypass_data_valid_5
       ? ~((&_wrbypass_io_T_116) & _GEN_3 | _wrbypass_io_T_116 == 3'h0 & ~_GEN_3)
       : ~((&_GEN_4) & _GEN_3 | _GEN_4 == 3'h0 & ~_GEN_3)) | _GEN_5;
  wire [2:0]  _wrbypass_io_T_138 =
    (io_update_pc[1] ? 3'h0 : _bank_wrbypasses_3_0_io_hit_data_0_bits)
    | (io_update_pc[1] ? _bank_wrbypasses_3_1_io_hit_data_0_bits : 3'h0);
  wire        wrbypass_data_valid_6 =
    (~(io_update_pc[1]) & _bank_wrbypasses_3_0_io_hit | io_update_pc[1]
     & _bank_wrbypasses_3_1_io_hit)
    & (~(io_update_pc[1]) & _bank_wrbypasses_3_0_io_hit_data_0_valid | io_update_pc[1]
       & _bank_wrbypasses_3_1_io_hit_data_0_valid);
  wire [2:0]  per_bank_update_wdata_3_0_ctr =
    _GEN_2
      ? (_GEN ? 3'h4 : 3'h3)
      : wrbypass_data_valid_6
          ? ((&_wrbypass_io_T_138) & _GEN
               ? 3'h7
               : _wrbypass_io_T_138 == 3'h0 & ~_GEN
                   ? 3'h0
                   : _GEN ? 3'(_wrbypass_io_T_138 + 3'h1) : 3'(_wrbypass_io_T_138 - 3'h1))
          : (&_GEN_0) & _GEN
              ? 3'h7
              : _GEN_1 ? (_GEN ? 3'(_GEN_0 + 3'h1) : 3'(_GEN_0 - 3'h1)) : 3'h0;
  assign per_bank_not_silent_update_3_0 =
    (wrbypass_data_valid_6
       ? ~((&_wrbypass_io_T_138) & _GEN | _wrbypass_io_T_138 == 3'h0 & ~_GEN)
       : ~((&_GEN_0) & _GEN | _GEN_0 == 3'h0 & ~_GEN)) | _GEN_2;
  wire [2:0]  _wrbypass_io_T_160 =
    (io_update_pc[1] ? _bank_wrbypasses_3_0_io_hit_data_0_bits : 3'h0)
    | (io_update_pc[1] ? 3'h0 : _bank_wrbypasses_3_1_io_hit_data_0_bits);
  wire        wrbypass_data_valid_7 =
    (io_update_pc[1] & _bank_wrbypasses_3_0_io_hit | ~(io_update_pc[1])
     & _bank_wrbypasses_3_1_io_hit)
    & (io_update_pc[1] & _bank_wrbypasses_3_0_io_hit_data_0_valid | ~(io_update_pc[1])
       & _bank_wrbypasses_3_1_io_hit_data_0_valid);
  wire [2:0]  per_bank_update_wdata_3_1_ctr =
    _GEN_5
      ? (_GEN_3 ? 3'h4 : 3'h3)
      : wrbypass_data_valid_7
          ? ((&_wrbypass_io_T_160) & _GEN_3
               ? 3'h7
               : _wrbypass_io_T_160 == 3'h0 & ~_GEN_3
                   ? 3'h0
                   : _GEN_3
                       ? 3'(_wrbypass_io_T_160 + 3'h1)
                       : 3'(_wrbypass_io_T_160 - 3'h1))
          : (&_GEN_4) & _GEN_3
              ? 3'h7
              : _GEN_4 == 3'h0 & ~_GEN_3
                  ? 3'h0
                  : _GEN_3 ? 3'(_GEN_4 + 3'h1) : 3'(_GEN_4 - 3'h1);
  assign per_bank_not_silent_update_3_1 =
    (wrbypass_data_valid_7
       ? ~((&_wrbypass_io_T_160) & _GEN_3 | _wrbypass_io_T_160 == 3'h0 & ~_GEN_3)
       : ~((&_GEN_4) & _GEN_3 | _GEN_4 == 3'h0 & ~_GEN_3)) | _GEN_5;
  always @(posedge clock) begin
    if (_s1_bank_req_1h_T) begin
      s1_unhashed_idx <= io_req_bits_pc[40:1];
      s1_tag <=
        io_req_bits_pc[8:1] ^ io_req_bits_folded_hist_hist_8_folded_hist
        ^ {io_req_bits_folded_hist_hist_5_folded_hist, 1'h0};
      s1_bank_req_1h_0 <= s0_bank_req_1h_0;
      s1_bank_req_1h_1 <= s0_bank_req_1h_1;
      s1_bank_req_1h_2 <= s0_bank_req_1h_2;
      s1_bank_req_1h_3 <= &(s0_idx[1:0]);
    end
    if (io_req_valid) begin
      s1_bank_has_write_on_this_req_0 <= _s1_bank_has_write_on_this_req_WIRE_0;
      s1_bank_has_write_on_this_req_1 <= _s1_bank_has_write_on_this_req_WIRE_1;
      s1_bank_has_write_on_this_req_2 <= _s1_bank_has_write_on_this_req_WIRE_2;
      s1_bank_has_write_on_this_req_3 <= _s1_bank_has_write_on_this_req_WIRE_3;
    end
  end // always @(posedge)
  always @(posedge clock or posedge reset) begin
    if (reset)
      powerOnResetState <= 1'h1;
    else
      powerOnResetState <=
        ~(_us_io_r_req_ready & _table_banks_0_io_r_req_ready
          & _table_banks_1_io_r_req_ready & _table_banks_2_io_r_req_ready
          & _table_banks_3_io_r_req_ready) & powerOnResetState;
  end // always @(posedge, posedge)
  `ifdef ENABLE_INITIAL_REG_
    `ifdef FIRRTL_BEFORE_INITIAL
      `FIRRTL_BEFORE_INITIAL
    `endif // FIRRTL_BEFORE_INITIAL
    logic [31:0] _RANDOM[0:3];
    initial begin
      `ifdef INIT_RANDOM_PROLOG_
        `INIT_RANDOM_PROLOG_
      `endif // INIT_RANDOM_PROLOG_
      `ifdef RANDOMIZE_REG_INIT
        for (logic [2:0] i = 3'h0; i < 3'h4; i += 3'h1) begin
          _RANDOM[i[1:0]] = `RANDOM;
        end
        s1_unhashed_idx = {_RANDOM[2'h0], _RANDOM[2'h1][7:0]};
        s1_tag = _RANDOM[2'h1][26:19];
        s1_bank_req_1h_0 = _RANDOM[2'h3][4];
        s1_bank_req_1h_1 = _RANDOM[2'h3][5];
        s1_bank_req_1h_2 = _RANDOM[2'h3][6];
        s1_bank_req_1h_3 = _RANDOM[2'h3][7];
        s1_bank_has_write_on_this_req_0 = _RANDOM[2'h3][8];
        s1_bank_has_write_on_this_req_1 = _RANDOM[2'h3][9];
        s1_bank_has_write_on_this_req_2 = _RANDOM[2'h3][10];
        s1_bank_has_write_on_this_req_3 = _RANDOM[2'h3][11];
        powerOnResetState = _RANDOM[2'h3][12];
      `endif // RANDOMIZE_REG_INIT
      if (reset)
        powerOnResetState = 1'h1;
    end // initial
    `ifdef FIRRTL_AFTER_INITIAL
      `FIRRTL_AFTER_INITIAL
    `endif // FIRRTL_AFTER_INITIAL
  `endif // ENABLE_INITIAL_REG_
  FoldedSRAMTemplate us (
    .clock                 (clock),
    .reset                 (reset),
    .io_r_req_ready        (_us_io_r_req_ready),
    .io_r_req_valid        (_s1_bank_req_1h_T),
    .io_r_req_bits_setIdx  (s0_idx),
    .io_r_resp_data_0      (_us_io_r_resp_data_0),
    .io_r_resp_data_1      (_us_io_r_resp_data_1),
    .io_w_req_valid
      (_us_extra_reset_T_1 & (io_update_uMask_0 | io_update_uMask_1)),
    .io_w_req_bits_setIdx  (update_idx),
    .io_w_req_bits_data_0
      (~(io_update_pc[1]) & io_update_us_0 | io_update_pc[1] & io_update_us_1),
    .io_w_req_bits_data_1
      (io_update_pc[1] & io_update_us_0 | ~(io_update_pc[1]) & io_update_us_1),
    .io_w_req_bits_waymask
      ({io_update_pc[1] & io_update_uMask_0 | ~(io_update_pc[1]) & io_update_uMask_1,
        ~(io_update_pc[1]) & io_update_uMask_0 | io_update_pc[1] & io_update_uMask_1}),
    .extra_reset
      ((io_update_reset_u_0 | io_update_reset_u_1) & _us_extra_reset_T_1)
  );
  FoldedSRAMTemplate_1 table_banks_0 (
    .clock                    (clock),
    .reset                    (reset),
    .io_r_req_ready           (_table_banks_0_io_r_req_ready),
    .io_r_req_valid           (_s1_bank_req_1h_T & s0_bank_req_1h_0),
    .io_r_req_bits_setIdx     (s0_idx[10:2]),
    .io_r_resp_data_0_valid   (_table_banks_0_io_r_resp_data_0_valid),
    .io_r_resp_data_0_tag     (_table_banks_0_io_r_resp_data_0_tag),
    .io_r_resp_data_0_ctr     (_table_banks_0_io_r_resp_data_0_ctr),
    .io_r_resp_data_1_valid   (_table_banks_0_io_r_resp_data_1_valid),
    .io_r_resp_data_1_tag     (_table_banks_0_io_r_resp_data_1_tag),
    .io_r_resp_data_1_ctr     (_table_banks_0_io_r_resp_data_1_ctr),
    .io_w_req_valid           (_s1_bank_has_write_on_this_req_WIRE_0),
    .io_w_req_bits_setIdx     (update_idx[10:2]),
    .io_w_req_bits_data_0_tag (update_tag),
    .io_w_req_bits_data_0_ctr (per_bank_update_wdata_0_0_ctr),
    .io_w_req_bits_data_1_tag (update_tag),
    .io_w_req_bits_data_1_ctr (per_bank_update_wdata_0_1_ctr),
    .io_w_req_bits_waymask    (per_bank_update_way_mask_0)
  );
  FoldedSRAMTemplate_1 table_banks_1 (
    .clock                    (clock),
    .reset                    (reset),
    .io_r_req_ready           (_table_banks_1_io_r_req_ready),
    .io_r_req_valid           (_s1_bank_req_1h_T & s0_bank_req_1h_1),
    .io_r_req_bits_setIdx     (s0_idx[10:2]),
    .io_r_resp_data_0_valid   (_table_banks_1_io_r_resp_data_0_valid),
    .io_r_resp_data_0_tag     (_table_banks_1_io_r_resp_data_0_tag),
    .io_r_resp_data_0_ctr     (_table_banks_1_io_r_resp_data_0_ctr),
    .io_r_resp_data_1_valid   (_table_banks_1_io_r_resp_data_1_valid),
    .io_r_resp_data_1_tag     (_table_banks_1_io_r_resp_data_1_tag),
    .io_r_resp_data_1_ctr     (_table_banks_1_io_r_resp_data_1_ctr),
    .io_w_req_valid           (_s1_bank_has_write_on_this_req_WIRE_1),
    .io_w_req_bits_setIdx     (update_idx[10:2]),
    .io_w_req_bits_data_0_tag (update_tag),
    .io_w_req_bits_data_0_ctr (per_bank_update_wdata_1_0_ctr),
    .io_w_req_bits_data_1_tag (update_tag),
    .io_w_req_bits_data_1_ctr (per_bank_update_wdata_1_1_ctr),
    .io_w_req_bits_waymask    (per_bank_update_way_mask_1)
  );
  FoldedSRAMTemplate_1 table_banks_2 (
    .clock                    (clock),
    .reset                    (reset),
    .io_r_req_ready           (_table_banks_2_io_r_req_ready),
    .io_r_req_valid           (_s1_bank_req_1h_T & s0_bank_req_1h_2),
    .io_r_req_bits_setIdx     (s0_idx[10:2]),
    .io_r_resp_data_0_valid   (_table_banks_2_io_r_resp_data_0_valid),
    .io_r_resp_data_0_tag     (_table_banks_2_io_r_resp_data_0_tag),
    .io_r_resp_data_0_ctr     (_table_banks_2_io_r_resp_data_0_ctr),
    .io_r_resp_data_1_valid   (_table_banks_2_io_r_resp_data_1_valid),
    .io_r_resp_data_1_tag     (_table_banks_2_io_r_resp_data_1_tag),
    .io_r_resp_data_1_ctr     (_table_banks_2_io_r_resp_data_1_ctr),
    .io_w_req_valid           (_s1_bank_has_write_on_this_req_WIRE_2),
    .io_w_req_bits_setIdx     (update_idx[10:2]),
    .io_w_req_bits_data_0_tag (update_tag),
    .io_w_req_bits_data_0_ctr (per_bank_update_wdata_2_0_ctr),
    .io_w_req_bits_data_1_tag (update_tag),
    .io_w_req_bits_data_1_ctr (per_bank_update_wdata_2_1_ctr),
    .io_w_req_bits_waymask    (per_bank_update_way_mask_2)
  );
  FoldedSRAMTemplate_1 table_banks_3 (
    .clock                    (clock),
    .reset                    (reset),
    .io_r_req_ready           (_table_banks_3_io_r_req_ready),
    .io_r_req_valid           (_s1_bank_req_1h_T & (&(s0_idx[1:0]))),
    .io_r_req_bits_setIdx     (s0_idx[10:2]),
    .io_r_resp_data_0_valid   (_table_banks_3_io_r_resp_data_0_valid),
    .io_r_resp_data_0_tag     (_table_banks_3_io_r_resp_data_0_tag),
    .io_r_resp_data_0_ctr     (_table_banks_3_io_r_resp_data_0_ctr),
    .io_r_resp_data_1_valid   (_table_banks_3_io_r_resp_data_1_valid),
    .io_r_resp_data_1_tag     (_table_banks_3_io_r_resp_data_1_tag),
    .io_r_resp_data_1_ctr     (_table_banks_3_io_r_resp_data_1_ctr),
    .io_w_req_valid           (_s1_bank_has_write_on_this_req_WIRE_3),
    .io_w_req_bits_setIdx     (update_idx[10:2]),
    .io_w_req_bits_data_0_tag (update_tag),
    .io_w_req_bits_data_0_ctr (per_bank_update_wdata_3_0_ctr),
    .io_w_req_bits_data_1_tag (update_tag),
    .io_w_req_bits_data_1_ctr (per_bank_update_wdata_3_1_ctr),
    .io_w_req_bits_waymask    (per_bank_update_way_mask_3)
  );
  WrBypass bank_wrbypasses_0_0 (
    .clock               (clock),
    .reset               (reset),
    .io_wen              (io_update_mask_0 & update_req_bank_1h_0),
    .io_write_idx        (update_idx[10:2]),
    .io_write_data_0
      ((io_update_pc[1] ? 3'h0 : per_bank_update_wdata_0_0_ctr)
       | (io_update_pc[1] ? per_bank_update_wdata_0_1_ctr : 3'h0)),
    .io_hit              (_bank_wrbypasses_0_0_io_hit),
    .io_hit_data_0_valid (_bank_wrbypasses_0_0_io_hit_data_0_valid),
    .io_hit_data_0_bits  (_bank_wrbypasses_0_0_io_hit_data_0_bits)
  );
  WrBypass bank_wrbypasses_0_1 (
    .clock               (clock),
    .reset               (reset),
    .io_wen              (io_update_mask_1 & update_req_bank_1h_0),
    .io_write_idx        (update_idx[10:2]),
    .io_write_data_0
      ((io_update_pc[1] ? per_bank_update_wdata_0_0_ctr : 3'h0)
       | (io_update_pc[1] ? 3'h0 : per_bank_update_wdata_0_1_ctr)),
    .io_hit              (_bank_wrbypasses_0_1_io_hit),
    .io_hit_data_0_valid (_bank_wrbypasses_0_1_io_hit_data_0_valid),
    .io_hit_data_0_bits  (_bank_wrbypasses_0_1_io_hit_data_0_bits)
  );
  WrBypass bank_wrbypasses_1_0 (
    .clock               (clock),
    .reset               (reset),
    .io_wen              (io_update_mask_0 & update_req_bank_1h_1),
    .io_write_idx        (update_idx[10:2]),
    .io_write_data_0
      ((io_update_pc[1] ? 3'h0 : per_bank_update_wdata_1_0_ctr)
       | (io_update_pc[1] ? per_bank_update_wdata_1_1_ctr : 3'h0)),
    .io_hit              (_bank_wrbypasses_1_0_io_hit),
    .io_hit_data_0_valid (_bank_wrbypasses_1_0_io_hit_data_0_valid),
    .io_hit_data_0_bits  (_bank_wrbypasses_1_0_io_hit_data_0_bits)
  );
  WrBypass bank_wrbypasses_1_1 (
    .clock               (clock),
    .reset               (reset),
    .io_wen              (io_update_mask_1 & update_req_bank_1h_1),
    .io_write_idx        (update_idx[10:2]),
    .io_write_data_0
      ((io_update_pc[1] ? per_bank_update_wdata_1_0_ctr : 3'h0)
       | (io_update_pc[1] ? 3'h0 : per_bank_update_wdata_1_1_ctr)),
    .io_hit              (_bank_wrbypasses_1_1_io_hit),
    .io_hit_data_0_valid (_bank_wrbypasses_1_1_io_hit_data_0_valid),
    .io_hit_data_0_bits  (_bank_wrbypasses_1_1_io_hit_data_0_bits)
  );
  WrBypass bank_wrbypasses_2_0 (
    .clock               (clock),
    .reset               (reset),
    .io_wen              (io_update_mask_0 & update_req_bank_1h_2),
    .io_write_idx        (update_idx[10:2]),
    .io_write_data_0
      ((io_update_pc[1] ? 3'h0 : per_bank_update_wdata_2_0_ctr)
       | (io_update_pc[1] ? per_bank_update_wdata_2_1_ctr : 3'h0)),
    .io_hit              (_bank_wrbypasses_2_0_io_hit),
    .io_hit_data_0_valid (_bank_wrbypasses_2_0_io_hit_data_0_valid),
    .io_hit_data_0_bits  (_bank_wrbypasses_2_0_io_hit_data_0_bits)
  );
  WrBypass bank_wrbypasses_2_1 (
    .clock               (clock),
    .reset               (reset),
    .io_wen              (io_update_mask_1 & update_req_bank_1h_2),
    .io_write_idx        (update_idx[10:2]),
    .io_write_data_0
      ((io_update_pc[1] ? per_bank_update_wdata_2_0_ctr : 3'h0)
       | (io_update_pc[1] ? 3'h0 : per_bank_update_wdata_2_1_ctr)),
    .io_hit              (_bank_wrbypasses_2_1_io_hit),
    .io_hit_data_0_valid (_bank_wrbypasses_2_1_io_hit_data_0_valid),
    .io_hit_data_0_bits  (_bank_wrbypasses_2_1_io_hit_data_0_bits)
  );
  WrBypass bank_wrbypasses_3_0 (
    .clock               (clock),
    .reset               (reset),
    .io_wen              (io_update_mask_0 & (&(update_idx[1:0]))),
    .io_write_idx        (update_idx[10:2]),
    .io_write_data_0
      ((io_update_pc[1] ? 3'h0 : per_bank_update_wdata_3_0_ctr)
       | (io_update_pc[1] ? per_bank_update_wdata_3_1_ctr : 3'h0)),
    .io_hit              (_bank_wrbypasses_3_0_io_hit),
    .io_hit_data_0_valid (_bank_wrbypasses_3_0_io_hit_data_0_valid),
    .io_hit_data_0_bits  (_bank_wrbypasses_3_0_io_hit_data_0_bits)
  );
  WrBypass bank_wrbypasses_3_1 (
    .clock               (clock),
    .reset               (reset),
    .io_wen              (io_update_mask_1 & (&(update_idx[1:0]))),
    .io_write_idx        (update_idx[10:2]),
    .io_write_data_0
      ((io_update_pc[1] ? per_bank_update_wdata_3_0_ctr : 3'h0)
       | (io_update_pc[1] ? 3'h0 : per_bank_update_wdata_3_1_ctr)),
    .io_hit              (_bank_wrbypasses_3_1_io_hit),
    .io_hit_data_0_valid (_bank_wrbypasses_3_1_io_hit_data_0_valid),
    .io_hit_data_0_bits  (_bank_wrbypasses_3_1_io_hit_data_0_bits)
  );
  assign io_req_ready = ~powerOnResetState;
  assign io_resps_0_valid =
    ~(s1_unhashed_idx[0]) & _hit_selected_T_6 | s1_unhashed_idx[0] & _hit_selected_T_13;
  assign io_resps_0_bits_ctr =
    (s1_unhashed_idx[0] ? 3'h0 : _resp_selected_T_6)
    | (s1_unhashed_idx[0] ? _resp_selected_T_27 : 3'h0);
  assign io_resps_0_bits_u =
    ~(s1_unhashed_idx[0]) & _us_io_r_resp_data_0 | s1_unhashed_idx[0]
    & _us_io_r_resp_data_1;
  assign io_resps_0_bits_unconf =
    ~(s1_unhashed_idx[0]) & _unconf_selected_T_6 | s1_unhashed_idx[0]
    & _unconf_selected_T_13;
  assign io_resps_1_valid =
    s1_unhashed_idx[0] & _hit_selected_T_6 | ~(s1_unhashed_idx[0]) & _hit_selected_T_13;
  assign io_resps_1_bits_ctr =
    (s1_unhashed_idx[0] ? _resp_selected_T_6 : 3'h0)
    | (s1_unhashed_idx[0] ? 3'h0 : _resp_selected_T_27);
  assign io_resps_1_bits_u =
    s1_unhashed_idx[0] & _us_io_r_resp_data_0 | ~(s1_unhashed_idx[0])
    & _us_io_r_resp_data_1;
  assign io_resps_1_bits_unconf =
    s1_unhashed_idx[0] & _unconf_selected_T_6 | ~(s1_unhashed_idx[0])
    & _unconf_selected_T_13;
endmodule

