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

module FTBEntryGen(	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7]
  input  [40:0] io_start_addr,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_valid,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [3:0]  io_old_entry_brSlots_0_offset,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [11:0] io_old_entry_brSlots_0_lower,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [1:0]  io_old_entry_brSlots_0_tarStat,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_brSlots_0_sharing,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_brSlots_0_valid,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [3:0]  io_old_entry_tailSlot_offset,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [19:0] io_old_entry_tailSlot_lower,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [1:0]  io_old_entry_tailSlot_tarStat,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_tailSlot_sharing,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_tailSlot_valid,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [3:0]  io_old_entry_pftAddr,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_carry,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_isCall,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_isRet,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_isJalr,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_last_may_be_rvi_call,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_always_taken_0,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_old_entry_always_taken_1,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_0,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_1,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_2,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_3,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_4,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_5,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_6,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_7,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_8,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_9,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_10,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_11,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_12,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_13,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_14,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_brMask_15,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_jmpInfo_valid,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_jmpInfo_bits_0,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_jmpInfo_bits_1,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_jmpInfo_bits_2,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [3:0]  io_pd_jmpOffset,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [40:0] io_pd_jalTarget,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_0,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_1,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_2,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_3,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_4,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_5,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_6,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_7,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_8,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_9,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_10,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_11,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_12,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_13,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_14,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_pd_rvcMask_15,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_cfiIndex_valid,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [3:0]  io_cfiIndex_bits,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input  [40:0] io_target,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_hit,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_0,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_1,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_2,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_3,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_4,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_5,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_6,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_7,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_8,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_9,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_10,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_11,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_12,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_13,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_14,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  input         io_mispredict_vec_15,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_valid,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output [3:0]  io_new_entry_brSlots_0_offset,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output [11:0] io_new_entry_brSlots_0_lower,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output [1:0]  io_new_entry_brSlots_0_tarStat,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_brSlots_0_sharing,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_brSlots_0_valid,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output [3:0]  io_new_entry_tailSlot_offset,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output [19:0] io_new_entry_tailSlot_lower,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output [1:0]  io_new_entry_tailSlot_tarStat,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_tailSlot_sharing,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_tailSlot_valid,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output [3:0]  io_new_entry_pftAddr,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_carry,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_isCall,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_isRet,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_isJalr,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_last_may_be_rvi_call,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_always_taken_0,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_new_entry_always_taken_1,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_taken_mask_0,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_taken_mask_1,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_jmp_taken,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_mispred_mask_0,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_mispred_mask_1,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_mispred_mask_2,	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
  output        io_is_old_entry	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14]
);

  wire [15:0] _GEN =
    {{io_pd_brMask_15},
     {io_pd_brMask_14},
     {io_pd_brMask_13},
     {io_pd_brMask_12},
     {io_pd_brMask_11},
     {io_pd_brMask_10},
     {io_pd_brMask_9},
     {io_pd_brMask_8},
     {io_pd_brMask_7},
     {io_pd_brMask_6},
     {io_pd_brMask_5},
     {io_pd_brMask_4},
     {io_pd_brMask_3},
     {io_pd_brMask_2},
     {io_pd_brMask_1},
     {io_pd_brMask_0}};	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:256:47]
  wire        cfi_is_br = _GEN[io_cfiIndex_bits] & io_cfiIndex_valid;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:256:47]
  wire        init_entry_isJalr =
    io_pd_jmpInfo_valid & io_pd_jmpInfo_bits_0 & io_cfiIndex_valid;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:259:62]
  wire        last_jmp_rvi = io_pd_jmpInfo_valid & (&io_pd_jmpOffset) & ~io_pd_rvcMask_15;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:262:{52,75,78}]
  wire        cfi_is_jalr = io_cfiIndex_bits == io_pd_jmpOffset & init_entry_isJalr;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:259:62, :265:37, :266:55]
  wire [39:0] _GEN_0 = cfi_is_jalr ? io_target[40:1] : io_pd_jalTarget[40:1];	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:225:14, :266:55, :287:64]
  wire [4:0]  _GEN_1 = {1'h0, io_start_addr[4:1]};	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:253:41, :269:30, :290:40]
  wire [15:0] _GEN_2 =
    {{io_pd_rvcMask_15},
     {io_pd_rvcMask_14},
     {io_pd_rvcMask_13},
     {io_pd_rvcMask_12},
     {io_pd_rvcMask_11},
     {io_pd_rvcMask_10},
     {io_pd_rvcMask_9},
     {io_pd_rvcMask_8},
     {io_pd_rvcMask_7},
     {io_pd_rvcMask_6},
     {io_pd_rvcMask_5},
     {io_pd_rvcMask_4},
     {io_pd_rvcMask_3},
     {io_pd_rvcMask_2},
     {io_pd_rvcMask_1},
     {io_pd_rvcMask_0}};	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:290:62]
  wire [4:0]  jmpPft =
    5'(_GEN_1
       + 5'({1'h0, io_pd_jmpOffset} + {3'h0, _GEN_2[io_pd_jmpOffset] ? 2'h1 : 2'h2}));	// @[src/main/scala/xiangshan/frontend/FTB.scala:60:10, :61:12, src/main/scala/xiangshan/frontend/NewFtq.scala:253:41, :290:{40,56,62}]
  wire        is_new_br =
    cfi_is_br
    & {io_old_entry_tailSlot_valid & io_old_entry_tailSlot_offset == io_cfiIndex_bits
         & io_old_entry_tailSlot_sharing,
       io_old_entry_brSlots_0_valid
         & io_old_entry_brSlots_0_offset == io_cfiIndex_bits} == 2'h0;	// @[src/main/scala/xiangshan/frontend/FTB.scala:194:{32,44}, :195:{42,53}, src/main/scala/xiangshan/frontend/NewFtq.scala:253:41, :256:47, :302:{37,44}, :303:29]
  wire        new_br_insert_onehot_0 =
    ~io_old_entry_brSlots_0_valid | io_cfiIndex_bits < io_old_entry_brSlots_0_offset;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:310:{9,33,50}]
  wire        _new_br_insert_onehot_T_3 =
    io_cfiIndex_bits > io_old_entry_brSlots_0_offset;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:312:53]
  wire        new_br_insert_onehot_1 =
    io_old_entry_brSlots_0_valid & _new_br_insert_onehot_T_3
    & (~io_old_entry_tailSlot_valid | io_cfiIndex_bits < io_old_entry_tailSlot_offset);	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:312:{53,83}, :313:{10,36,53}]
  wire        _GEN_3 = io_cfiIndex_bits > io_old_entry_tailSlot_offset;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:325:31]
  wire        _GEN_4 = _GEN_3 | ~io_old_entry_brSlots_0_valid;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:317:36, :325:{31,61}, :332:44]
  wire        pft_need_to_change =
    is_new_br & io_old_entry_brSlots_0_valid & io_old_entry_tailSlot_valid;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:303:29, :345:38]
  wire [3:0]  new_pft_offset =
    {new_br_insert_onehot_1, new_br_insert_onehot_0} == 2'h0
      ? io_cfiIndex_bits
      : io_old_entry_tailSlot_offset;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:253:41, :310:33, :312:83, :349:{10,33,40}]
  wire [4:0]  _old_entry_modified_carry_T_1 = 5'(_GEN_1 + {1'h0, new_pft_offset});	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:253:41, :290:40, :349:10, :353:59, :354:58]
  wire        _old_target_target_T_9 = io_old_entry_tailSlot_tarStat == 2'h1;	// @[src/main/scala/xiangshan/frontend/FTB.scala:60:10, :98:19]
  wire        _old_target_target_T_10 = io_old_entry_tailSlot_tarStat == 2'h2;	// @[src/main/scala/xiangshan/frontend/FTB.scala:61:12, :99:19]
  wire        _old_target_target_T_11 = io_old_entry_tailSlot_tarStat == 2'h0;	// @[src/main/scala/xiangshan/frontend/FTB.scala:100:19, src/main/scala/xiangshan/frontend/NewFtq.scala:253:41]
  wire        jalr_target_modified =
    cfi_is_jalr
    & {io_old_entry_tailSlot_sharing
         ? {(_old_target_target_T_9 ? 28'(io_start_addr[40:13] + 28'h1) : 28'h0)
              | (_old_target_target_T_10 ? 28'(io_start_addr[40:13] - 28'h1) : 28'h0)
              | (_old_target_target_T_11 ? io_start_addr[40:13] : 28'h0),
            io_old_entry_tailSlot_lower[11:0]}
         : {(_old_target_target_T_9 ? 20'(io_start_addr[40:21] + 20'h1) : 20'h0)
              | (_old_target_target_T_10 ? 20'(io_start_addr[40:21] - 20'h1) : 20'h0)
              | (_old_target_target_T_11 ? io_start_addr[40:21] : 20'h0),
            io_old_entry_tailSlot_lower},
       1'h0} != io_target & ~io_old_entry_tailSlot_sharing;	// @[src/main/scala/chisel3/util/Mux.scala:30:73, src/main/scala/xiangshan/frontend/FTB.scala:76:32, :92:30, :93:31, :96:12, :98:19, :99:19, :100:19, :102:16, :109:10, src/main/scala/xiangshan/frontend/NewFtq.scala:253:41, :266:55, :363:25, :364:{57,72}]
  wire        old_entry_always_taken_always_taken_0 =
    io_old_entry_always_taken_0 & io_cfiIndex_valid & io_old_entry_brSlots_0_valid
    & io_cfiIndex_bits == io_old_entry_brSlots_0_offset;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:374:{65,85}]
  wire        old_entry_always_taken_always_taken_1 =
    io_old_entry_always_taken_1 & io_cfiIndex_valid & io_old_entry_tailSlot_valid
    & io_old_entry_tailSlot_sharing & io_cfiIndex_bits == io_old_entry_tailSlot_offset;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:374:{65,85}]
  wire        _GEN_5 = is_new_br & new_br_insert_onehot_0;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:303:29, :310:33, :382:8]
  wire        _GEN_6 = is_new_br & pft_need_to_change;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:303:29, :345:38, :382:8]
  wire        _GEN_7 = ~is_new_br | ~pft_need_to_change;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:303:29, :317:36, :345:38, :347:29, :355:45, :382:8]
  wire [3:0]  io_new_entry_brSlots_0_offset_0 =
    io_hit
      ? (_GEN_5 ? io_cfiIndex_bits : io_old_entry_brSlots_0_offset)
      : cfi_is_br ? io_cfiIndex_bits : 4'h0;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:253:{28,41}, :256:47, :276:20, :278:25, :382:8, :386:22]
  wire        io_new_entry_brSlots_0_valid_0 =
    io_hit ? _GEN_5 | io_old_entry_brSlots_0_valid : cfi_is_br;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:256:47, :382:8, :386:22]
  wire [3:0]  io_new_entry_tailSlot_offset_0 =
    io_hit
      ? (is_new_br
           ? (new_br_insert_onehot_1
                ? io_cfiIndex_bits
                : _GEN_4 ? io_old_entry_tailSlot_offset : io_old_entry_brSlots_0_offset)
           : io_old_entry_tailSlot_offset)
      : io_pd_jmpInfo_valid ? io_pd_jmpOffset : 4'h0;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:253:{28,41}, :284:24, :285:32, :303:29, :312:83, :317:36, :320:36, :322:19, :325:61, :332:44, :382:8, :386:22]
  wire        io_new_entry_tailSlot_sharing_0 =
    io_hit
    & (is_new_br
         ? new_br_insert_onehot_1 | ~_GEN_3 & io_old_entry_brSlots_0_valid
           | io_old_entry_tailSlot_sharing
         : ~jalr_target_modified & io_old_entry_tailSlot_sharing);	// @[src/main/scala/xiangshan/frontend/FTB.scala:70:18, src/main/scala/xiangshan/frontend/NewFtq.scala:303:29, :312:83, :317:36, :320:36, :325:{31,61}, :332:44, :361:47, :364:72, :365:31, :382:8, :383:10, :386:22]
  wire        io_new_entry_tailSlot_valid_0 =
    io_hit
      ? (is_new_br
           ? new_br_insert_onehot_1
             | (_GEN_4 ? io_old_entry_tailSlot_valid : io_old_entry_brSlots_0_valid)
           : io_old_entry_tailSlot_valid)
      : io_pd_jmpInfo_valid
        & (io_pd_jmpInfo_valid & ~io_pd_jmpInfo_bits_0 & io_cfiIndex_valid
           | init_entry_isJalr);	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:253:28, :258:{42,62}, :259:62, :284:24, :286:{31,49}, :303:29, :312:83, :317:36, :320:36, :321:18, :325:61, :332:44, :382:8, :386:22]
  wire        _io_mispred_mask_1_T =
    io_new_entry_tailSlot_valid_0 & io_new_entry_tailSlot_sharing_0;	// @[src/main/scala/xiangshan/frontend/FTB.scala:203:47, src/main/scala/xiangshan/frontend/NewFtq.scala:386:22]
  wire [15:0] _GEN_8 =
    {{io_mispredict_vec_15},
     {io_mispredict_vec_14},
     {io_mispredict_vec_13},
     {io_mispredict_vec_12},
     {io_mispredict_vec_11},
     {io_mispredict_vec_10},
     {io_mispredict_vec_9},
     {io_mispredict_vec_8},
     {io_mispredict_vec_7},
     {io_mispredict_vec_6},
     {io_mispredict_vec_5},
     {io_mispredict_vec_4},
     {io_mispredict_vec_3},
     {io_mispredict_vec_2},
     {io_mispredict_vec_1},
     {io_mispredict_vec_0}};	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:394:52]
  assign io_new_entry_valid = ~io_hit | io_old_entry_valid;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:{22,23}]
  assign io_new_entry_brSlots_0_offset = io_new_entry_brSlots_0_offset_0;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22]
  assign io_new_entry_brSlots_0_lower =
    io_hit
      ? (_GEN_5 ? io_target[12:1] : io_old_entry_brSlots_0_lower)
      : cfi_is_br ? io_target[12:1] : 12'h0;	// @[src/main/scala/xiangshan/frontend/FTB.scala:62:64, :68:16, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :253:{28,41}, :256:47, :276:20, :382:8, :386:22]
  assign io_new_entry_brSlots_0_tarStat =
    io_hit
      ? (_GEN_5
           ? (io_target[40:13] > io_start_addr[40:13]
                ? 2'h1
                : {io_target[40:13] < io_start_addr[40:13], 1'h0})
           : io_old_entry_brSlots_0_tarStat)
      : cfi_is_br
          ? (io_target[40:13] > io_start_addr[40:13]
               ? 2'h1
               : {io_target[40:13] < io_start_addr[40:13], 1'h0})
          : 2'h0;	// @[src/main/scala/xiangshan/frontend/FTB.scala:60:{10,25}, :61:{12,27}, :64:23, :65:31, :69:18, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :253:{28,41}, :256:47, :276:20, :382:8, :386:22]
  assign io_new_entry_brSlots_0_sharing =
    io_hit & (~is_new_br | ~new_br_insert_onehot_0) & io_old_entry_brSlots_0_sharing;	// @[src/main/scala/xiangshan/frontend/FTB.scala:70:18, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :303:29, :310:33, :317:36, :320:36, :382:8, :386:22]
  assign io_new_entry_brSlots_0_valid = io_new_entry_brSlots_0_valid_0;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22]
  assign io_new_entry_tailSlot_offset = io_new_entry_tailSlot_offset_0;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22]
  assign io_new_entry_tailSlot_lower =
    io_hit
      ? (is_new_br
           ? (new_br_insert_onehot_1
                ? {8'h0, io_target[12:1]}
                : _GEN_4
                    ? io_old_entry_tailSlot_lower
                    : {8'h0, io_old_entry_brSlots_0_lower})
           : jalr_target_modified ? io_target[20:1] : io_old_entry_tailSlot_lower)
      : io_pd_jmpInfo_valid ? _GEN_0[19:0] : 20'h0;	// @[src/main/scala/xiangshan/frontend/FTB.scala:62:64, :68:16, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :253:{28,41}, :284:24, :287:64, :303:29, :312:83, :317:36, :320:36, :325:61, :332:44, :364:72, :382:8, :383:10, :386:22, utility/src/main/scala/utility/BitUtils.scala:88:41]
  assign io_new_entry_tailSlot_tarStat =
    io_hit
      ? (is_new_br
           ? (new_br_insert_onehot_1
                ? (io_target[40:13] > io_start_addr[40:13]
                     ? 2'h1
                     : {io_target[40:13] < io_start_addr[40:13], 1'h0})
                : _GEN_4 ? io_old_entry_tailSlot_tarStat : io_old_entry_brSlots_0_tarStat)
           : jalr_target_modified
               ? (io_target[40:21] > io_start_addr[40:21]
                    ? 2'h1
                    : {io_target[40:21] < io_start_addr[40:21], 1'h0})
               : io_old_entry_tailSlot_tarStat)
      : io_pd_jmpInfo_valid
          ? (_GEN_0[39:20] > io_start_addr[40:21]
               ? 2'h1
               : {_GEN_0[39:20] < io_start_addr[40:21], 1'h0})
          : 2'h0;	// @[src/main/scala/xiangshan/frontend/FTB.scala:60:{10,25}, :61:{12,27}, :64:23, :65:31, :69:18, :76:32, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :253:{28,41}, :284:24, :287:64, :303:29, :312:83, :317:36, :320:36, :325:61, :332:44, :364:72, :382:8, :383:10, :386:22]
  assign io_new_entry_tailSlot_sharing = io_new_entry_tailSlot_sharing_0;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22]
  assign io_new_entry_tailSlot_valid = io_new_entry_tailSlot_valid_0;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22]
  assign io_new_entry_pftAddr =
    io_hit
      ? (_GEN_6 ? 4'(io_start_addr[4:1] + new_pft_offset) : io_old_entry_pftAddr)
      : io_pd_jmpInfo_valid & ~last_jmp_rvi ? jmpPft[3:0] : io_start_addr[4:1];	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :262:75, :269:30, :290:56, :291:{28,43,46}, :349:10, :353:59, :382:8, :386:22]
  assign io_new_entry_carry =
    io_hit
      ? (_GEN_6 ? _old_entry_modified_carry_T_1[4] : io_old_entry_carry)
      : ~(io_pd_jmpInfo_valid & ~last_jmp_rvi) | jmpPft[4];	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :262:75, :290:56, :291:46, :292:{28,43,67}, :354:{58,81}, :382:8, :386:22]
  assign io_new_entry_isCall =
    io_hit
      ? _GEN_7 & io_old_entry_isCall
      : io_pd_jmpInfo_valid & io_pd_jmpInfo_bits_1 & io_cfiIndex_valid;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :260:62, :382:8, :386:22]
  assign io_new_entry_isRet =
    io_hit
      ? _GEN_7 & io_old_entry_isRet
      : io_pd_jmpInfo_valid & io_pd_jmpInfo_bits_2 & io_cfiIndex_valid;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :261:62, :382:8, :386:22]
  assign io_new_entry_isJalr = io_hit ? _GEN_7 & io_old_entry_isJalr : init_entry_isJalr;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :259:62, :382:8, :386:22]
  assign io_new_entry_last_may_be_rvi_call =
    io_hit
      ? _GEN_7 & io_old_entry_last_may_be_rvi_call
      : (&io_pd_jmpOffset) & ~_GEN_2[io_pd_jmpOffset];	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :262:52, :290:62, :297:{74,77}, :382:8, :386:22]
  assign io_new_entry_always_taken_0 =
    io_hit
      ? (is_new_br
           ? new_br_insert_onehot_0 | ~_new_br_insert_onehot_T_3
             & io_old_entry_always_taken_0
           : jalr_target_modified
               ? ~jalr_target_modified & io_old_entry_always_taken_0
               : old_entry_always_taken_always_taken_0)
      : cfi_is_br;	// @[src/main/scala/xiangshan/frontend/FTB.scala:70:18, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :256:47, :303:29, :310:33, :312:53, :317:36, :320:36, :324:42, :325:61, :326:42, :361:47, :364:72, :365:31, :367:48, :374:65, :382:8, :383:10, :386:22]
  assign io_new_entry_always_taken_1 =
    io_hit
    & (is_new_br
         ? new_br_insert_onehot_1 | ~_GEN_3 & io_old_entry_always_taken_1
         : jalr_target_modified
             ? ~jalr_target_modified & io_old_entry_always_taken_1
             : old_entry_always_taken_always_taken_1);	// @[src/main/scala/xiangshan/frontend/FTB.scala:70:18, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :303:29, :312:83, :317:36, :320:36, :324:42, :325:{31,61}, :326:42, :332:44, :361:47, :364:72, :365:31, :367:48, :374:65, :382:8, :383:10, :386:22]
  assign io_taken_mask_0 =
    io_cfiIndex_bits == io_new_entry_brSlots_0_offset_0 & io_cfiIndex_valid
    & io_new_entry_brSlots_0_valid_0;	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22, :390:{39,68}]
  assign io_taken_mask_1 =
    io_cfiIndex_bits == io_new_entry_tailSlot_offset_0 & io_cfiIndex_valid
    & _io_mispred_mask_1_T;	// @[src/main/scala/xiangshan/frontend/FTB.scala:203:47, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22, :390:{39,68}]
  assign io_jmp_taken =
    io_new_entry_tailSlot_valid_0 & ~io_new_entry_tailSlot_sharing_0
    & io_new_entry_tailSlot_offset_0 == io_cfiIndex_bits;	// @[src/main/scala/xiangshan/frontend/FTB.scala:217:23, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22, :392:{41,73}]
  assign io_mispred_mask_0 =
    io_new_entry_brSlots_0_valid_0 & _GEN_8[io_new_entry_brSlots_0_offset_0];	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22, :394:52]
  assign io_mispred_mask_1 =
    _io_mispred_mask_1_T & _GEN_8[io_new_entry_tailSlot_offset_0];	// @[src/main/scala/xiangshan/frontend/FTB.scala:203:47, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22, :394:52]
  assign io_mispred_mask_2 =
    io_new_entry_tailSlot_valid_0 & ~io_new_entry_tailSlot_sharing_0
    & _GEN_8[io_pd_jmpOffset];	// @[src/main/scala/xiangshan/frontend/FTB.scala:217:23, src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :386:22, :394:52, :396:49]
  assign io_is_old_entry =
    io_hit & ~is_new_br & ~jalr_target_modified
    & ~(io_old_entry_always_taken_0 & ~old_entry_always_taken_always_taken_0
        | io_old_entry_always_taken_1 & ~old_entry_always_taken_always_taken_1);	// @[src/main/scala/xiangshan/frontend/NewFtq.scala:224:7, :303:29, :364:72, :374:65, :375:{56,59}, :377:65, :400:{29,43,65,68}]
endmodule

