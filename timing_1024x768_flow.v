module timing_1024x768_flow(
    input  clk_pixel,       // 25 MHz pixel klok
    input  resetn,
    output reg hsync,
    output reg vsync,
    output reg de,          // data enable
    output reg [11:0] hcount,
    output reg [11:0] vcount
);

    // 1024x768@70Hz timing (VESA)
    localparam H_ACTIVE    = 1024;
    localparam H_FRONT     = 24;
    localparam H_SYNC      = 136;
    localparam H_BACK      = 160;
    localparam H_TOTAL     = H_ACTIVE + H_FRONT + H_SYNC + H_BACK; // 1344

    localparam V_ACTIVE    = 768;
    localparam V_FRONT     = 3;
    localparam V_SYNC      = 6;
    localparam V_BACK      = 29;
    localparam V_TOTAL     = V_ACTIVE + V_FRONT + V_SYNC + V_BACK; // 806

    // horizontale en verticale counters
    always @(posedge clk_pixel or negedge resetn) begin
        if(!resetn) begin
            hcount <= 0;
            vcount <= 0;
        end else begin
            if(hcount == H_TOTAL-1) begin
                hcount <= 0;
                if(vcount == V_TOTAL-1)
                    vcount <= 0;
                else
                    vcount <= vcount + 1;
            end else begin
                hcount <= hcount + 1;
            end
        end
    end

    // sync en data enable genereren
    always @(posedge clk_pixel) begin
        hsync <= (hcount >= (H_ACTIVE + H_FRONT)) &&
                 (hcount <  (H_ACTIVE + H_FRONT + H_SYNC));
        vsync <= (vcount >= (V_ACTIVE + V_FRONT)) &&
                 (vcount <  (V_ACTIVE + V_FRONT + V_SYNC));

        de    <= (hcount < H_ACTIVE) && (vcount < V_ACTIVE);
    end
endmodule

