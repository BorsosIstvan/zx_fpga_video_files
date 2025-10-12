module pattern (
    input  wire       clk_pixel,
    input  wire       reset_n,
    input  wire [10:0] hcnt,
    input  wire [10:0] vcnt,
    output reg  [23:0] rgb
);

    // hcnt / 128  ==  hcnt[10:7]  (want 2^7 = 128)
    wire [2:0] stripe_index = hcnt[10:7];

always @(posedge clk_pixel or negedge reset_n) begin
    if (!reset_n) begin
        rgb <= 24'hFFFFFF;
    end else begin
        // binnen zichtbare resolutie (1024x768)
        if ((hcnt < 1024) && (vcnt < 768)) begin
            case (stripe_index)
                3'd0: rgb <= 24'hFF0000; // rood
                3'd1: rgb <= 24'h00FF00; // groen
                3'd2: rgb <= 24'h0000FF; // blauw
                3'd3: rgb <= 24'hFFFF00; // geel
                3'd4: rgb <= 24'hFF00FF; // magenta
                3'd5: rgb <= 24'h00FFFF; // cyaan
                3'd6: rgb <= 24'hFFFFFF; // wit
                3'd7: rgb <= 24'h000000; // zwart
                default: rgb <= 24'h000000; // veiligheidskleur
            endcase
        end else begin
            // buiten zichtbaar (blanking)
            rgb <= 24'h000000;
        end
    end
end

endmodule
