module ula_my (
    input  clk,
    input  resetn,
    output reg busy,           // actief als ULA video-RAM leest
    output reg [7:0] h_count,  // 0..255 tijdens actief venster
    output reg [7:0] v_count   // 0..191 tijdens actief venster
);

    // Horizontale parameters
    parameter H_TOTAL   = 448;   // totaal clocks per lijn
    parameter H_SYNC    = 84;    // sync breedte
    parameter H_BORDER  = 108;   // border (links+rechts samen)
    parameter H_VIDEO   = 256;   // actief video breedte

    // Verticale parameters
    parameter V_TOTAL   = 312;   // totaal lijnen per frame
    parameter V_SYNC    = 4;
    parameter V_BORDER  = 56;
    parameter V_VIDEO   = 192;

    // Tellers
    reg [8:0] h_cnt = 0;
    reg [8:0] v_cnt = 0;

    // horizontale teller
    always @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            h_cnt <= 0;
            v_cnt <= 0;
        end else if (h_cnt == H_TOTAL-1) begin
            h_cnt <= 0;
            v_cnt <= (v_cnt == V_TOTAL-1) ? 0 : v_cnt + 1;
        end else begin
            h_cnt <= h_cnt + 1;
        end
    end

    // start van actief venster (links)
    localparam H_START = H_SYNC + (H_BORDER/2);
    localparam H_END   = H_START + H_VIDEO;

    localparam V_START = V_SYNC + (V_BORDER/2);
    localparam V_END   = V_START + V_VIDEO;

    // video actief detectie
    wire video_active_h = (h_cnt >= H_START) && (h_cnt < H_END);
    wire video_active_v = (v_cnt >= V_START) && (v_cnt < V_END);

    // afgeleide tellers
    always @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            h_count <= 0;
            v_count <= 0;
            busy    <= 0;
        end else begin
            if (video_active_h) begin
                h_count <= h_cnt - H_START;   // loopt 0..255
            end else if (h_cnt == 0) begin
                h_count <= 0; // reset aan begin van lijn
            end

            if (video_active_v) begin
                v_count <= v_cnt - V_START;   // loopt 0..191
            end else if (v_cnt == 0) begin
                v_count <= 0;
            end

            busy <= video_active_h && video_active_v;
        end
    end

endmodule