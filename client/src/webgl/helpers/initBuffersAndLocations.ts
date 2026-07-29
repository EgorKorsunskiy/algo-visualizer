export function initBuffers(gl: WebGLRenderingContext, positionData: Float32Array, colorData: Float32Array) {
    const positionBuffer = gl.createBuffer()
    const colorBuffer = gl.createBuffer()

    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer)
    gl.bufferData(gl.ARRAY_BUFFER, positionData, gl.DYNAMIC_DRAW)

    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer)
    gl.bufferData(gl.ARRAY_BUFFER, colorData, gl.DYNAMIC_DRAW)

    return { positionBuffer, colorBuffer }
}

export function initAndBindLocations(gl: WebGLRenderingContext, program: WebGLProgram, positionBuffer: WebGLBuffer, colorBuffer: WebGLBuffer) {
    const positionLocation = gl.getAttribLocation(program, "a_position")
    const colorLocation = gl.getAttribLocation(program, "a_color")
    const resolutionLocation = gl.getUniformLocation(program, "u_resolution")
    const useTextureLocation = gl.getUniformLocation(program, "u_useTexture")

    const posSize = 2
    const colSize = 4

    const type = gl.FLOAT
    const normalize = false
    const stride = 0 // default to selected data type -> size*sizeof(type)
    const offset = 0

    gl.enableVertexAttribArray(positionLocation)
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer)
    gl.vertexAttribPointer(positionLocation, posSize, type, normalize, stride, offset)

    gl.enableVertexAttribArray(colorLocation)
    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer)
    gl.vertexAttribPointer(colorLocation, colSize, type, normalize, stride, offset)

    gl.uniform2f(resolutionLocation, gl.canvas.width, gl.canvas.height)
    gl.uniform1f(useTextureLocation, 0.0)

    return { positionLocation, colorLocation, resolutionLocation }
}

export function initTexture(gl: WebGLRenderingContext, program: WebGLProgram, image: TexImageSource) {
    const texPosLocation = gl.getAttribLocation(program, "a_texPos")
    const useTextureLocation = gl.getUniformLocation(program, "u_useTexture")
    gl.uniform1f(useTextureLocation, 1.0)

    const texPosData = new Float32Array([
        0, 0,
        1, 0,
        0, 1,
        0, 1,
        1, 0,
        1, 1,
    ])
    const texPosBuffer = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, texPosBuffer)
    gl.bufferData(gl.ARRAY_BUFFER, texPosData, gl.DYNAMIC_DRAW)

    const size = 2
    const type = gl.FLOAT
    const normalize = false
    const stride = 0 // default to selected data type -> size*sizeof(type)
    const offset = 0

    gl.enableVertexAttribArray(texPosLocation)
    gl.vertexAttribPointer(texPosLocation, size, type, normalize, stride, offset)

    const texture = gl.createTexture()
    gl.bindTexture(gl.TEXTURE_2D, texture)

    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);

    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image)
}