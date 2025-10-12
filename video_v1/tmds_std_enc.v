// Minimal standard-conform TMDS encoder (10-bit output)
// de = 1 : encode pixel data (din[7:0])
// de = 0 : output control symbol according to {c1,c0}
module tmds_std_enc (
    input  wire       clk,     // pixel clock
    input  wire       resetn,  // active low (synchronous reset in this code)
    input  wire       de,      // data enable (1 = video)
    input  wire       c0,      // HSync
    input  wire       c1,      // VSync
    input  wire [7:0] din,     // input byte
    output reg  [9:0] dout     // 10-bit TMDS output
);

    // helper functions: count ones / zeros in 8-bit vector
    function [3:0] N1;
        input [7:0] bits;
        integer i;
        begin
            N1 = 0;
            for (i = 0; i < 8; i = i + 1)
                N1 = N1 + bits[i];
        end
    endfunction

    function [3:0] N0;
        input [7:0] bits;
        integer i;
        begin
            N0 = 0;
            for (i = 0; i < 8; i = i + 1)
                N0 = N0 + !bits[i];
        end
    endfunction

    // internal regs
    reg [8:0] q_m;                // intermediate 9-bit (8 data + mode bit)
    reg [9:0] q_out, q_out_next;  // next encoded 10-bit (unbuffered)
    reg signed [7:0] rd, rd_next; // running disparity (signed)
    reg [3:0] ones_qm, zeros_qm;  // counts for q_m[7:0]

    // pipeline buffer to help timing (two FF stages)
    reg [9:0] dout_buf1, dout_buf2;

    // combinational part: compute q_m and q_out_next and rd_next
    // We'll do everything in a clocked block for simplicity and to avoid
    // combinational complexity in some tools. This is standard practice.
    always @(posedge clk) begin
        if (!resetn) begin
            q_out <= 10'b0;
            q_out_next <= 10'b0;
            rd <= 0;
            q_m <= 9'd0;
            ones_qm <= 4'd0;
            zeros_qm <= 4'd0;
            dout_buf1 <= 10'd0;
            dout_buf2 <= 10'd0;
            dout <= 10'd0;
        end else begin
            if (!de) begin
                // Control period: send one of four control symbols, reset disparity
                case ({c1,c0})
                    2'b00: q_out <= 10'b1101010100;
                    2'b01: q_out <= 10'b0010101011;
                    2'b10: q_out <= 10'b0101010100;
                    2'b11: q_out <= 10'b1010101011;
                endcase
                rd <= 0;
            end else begin
                // --- Step 1: transition minimization to produce q_m[7:0]
                // mode = 1 means use XNOR chain; mode=0 means XOR chain
                // standard rule: mode = (N1(din) > 4) || (N1(din) == 4 && din[0] == 0)
                if ((N1(din) > 4) || ((N1(din) == 4) && (din[0] == 0))) begin
                    // XNOR chain (implementation using bitwise ops)
                    q_m[0] = din[0];
                    q_m[1] = ~(q_m[0] ^ din[1]); // q_m[0] XNOR din[1]
                    q_m[2] = ~(q_m[1] ^ din[2]);
                    q_m[3] = ~(q_m[2] ^ din[3]);
                    q_m[4] = ~(q_m[3] ^ din[4]);
                    q_m[5] = ~(q_m[4] ^ din[5]);
                    q_m[6] = ~(q_m[5] ^ din[6]);
                    q_m[7] = ~(q_m[6] ^ din[7]);
                    q_m[8] = 1'b0; // note: some formulations set bit8 = 0 for XNOR-mode (spec uses opposite convention in places; this matches SVO approach)
                end else begin
                    // XOR chain
                    q_m[0] = din[0];
                    q_m[1] = q_m[0] ^ din[1];
                    q_m[2] = q_m[1] ^ din[2];
                    q_m[3] = q_m[2] ^ din[3];
                    q_m[4] = q_m[3] ^ din[4];
                    q_m[5] = q_m[4] ^ din[5];
                    q_m[6] = q_m[5] ^ din[6];
                    q_m[7] = q_m[6] ^ din[7];
                    q_m[8] = 1'b1;
                end

                // count ones/zeros in q_m[7:0]
                ones_qm = N1(q_m[7:0]);
                zeros_qm = N0(q_m[7:0]);

                // --- Step 2: running disparity decision
                // This follows the reference encoder logic:
                if ((rd == 0) || (ones_qm == zeros_qm)) begin
                    // case: equal or zero disparity -> use simple code
                    q_out[9] <= ~q_m[8];
                    q_out[8] <=  q_m[8];
                    if (q_m[8])
                        q_out[7:0] <= q_m[7:0];
                    else
                        q_out[7:0] <= ~q_m[7:0];

                    if (q_m[8])
                        rd <= rd + (ones_qm - zeros_qm);
                    else
                        rd <= rd + (zeros_qm - ones_qm);

                end else if ( (rd > 0 && ones_qm > zeros_qm) ||
                              (rd < 0 && zeros_qm > ones_qm) ) begin
                    // invert and set leading bit to '1'
                    q_out[9] <= 1'b1;
                    q_out[8] <= q_m[8];
                    q_out[7:0] <= ~q_m[7:0];

                    // update disparity
                    // cnt_tmp = rd + (zeros_qm - ones_qm)
                    if (q_m[8])
                        rd <= rd + (zeros_qm - ones_qm) + 2; // the +2 correction when q_m[8]==1
                    else
                        rd <= rd + (zeros_qm - ones_qm);
                end else begin
                    // keep polarity and set leading bit to '0'
                    q_out[9] <= 1'b0;
                    q_out[8] <= q_m[8];
                    q_out[7:0] <= q_m[7:0];

                    // update disparity
                    if (q_m[8])
                        rd <= rd + (ones_qm - zeros_qm);
                    else
                        rd <= rd + (ones_qm - zeros_qm) - 2; // -2 correction when q_m[8]==0
                end
            end // de
            // pipeline output through two registers (helps timing)
            dout_buf1 <= q_out;
            dout_buf2 <= dout_buf1;
            dout <= dout_buf2;
        end // resetn
    end // always

endmodule
