# shaders.py

vertex_shader = """
#version 120
attribute vec3 a_position;
void main() {
    gl_Position = vec4(a_position, 1.0);
}
"""

fragment_shader = """
#version 120
uniform vec4 u_color;
void main() {
    gl_FragColor = u_color;
}
"""
