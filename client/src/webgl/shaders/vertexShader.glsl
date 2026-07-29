attribute vec2 a_position;
attribute vec2 a_texPos;
attribute vec4 a_color;

uniform vec2 u_resolution;
uniform bool u_useTexture;

varying vec4 v_color;
varying vec2 v_texPos;

void main() {
    if(u_useTexture) {
        v_texPos = a_texPos;
    }
    else {
        v_color = a_color;
        v_texPos = vec2(-1,-1);
    }
    vec2 zeroToTwoPos = (a_position / u_resolution) * 2.0;
    vec2 clipSpace = zeroToTwoPos - vec2(1.0);

    gl_Position = vec4(clipSpace*vec2(1,-1), 0, 1);
}