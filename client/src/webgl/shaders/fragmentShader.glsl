precision mediump float;

uniform sampler2D u_image;

varying vec4 v_color;
varying vec2 v_texPos;

void main() {
    if(v_texPos[0] == -1.0) {
        gl_FragColor = v_color;
    }
    else {
        gl_FragColor = texture2D(u_image, v_texPos);
    }
}