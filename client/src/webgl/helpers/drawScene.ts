import { initAndBindLocations, initBuffers, initTexture } from "./initBuffersAndLocations"
import { initProgram } from "./initProgram"

let program: WebGLProgram | null = null

export async function drawScene(gl: WebGLRenderingContext, positionData: Float32Array, colorData: Float32Array, texture: TexImageSource | null = null, count: number = -1) {
    if (program === null) {
        program = await initProgram(gl)
        gl.useProgram(program)
    }
    if (program === null) {
        throw new Error("Failed to initialise ")
    }
    const { positionBuffer, colorBuffer } = initBuffers(gl, positionData, colorData)
    initAndBindLocations(gl, program, positionBuffer, colorBuffer)
    if (texture) {
        initTexture(gl, program, texture)
    }

    const primitiveType = gl.TRIANGLES
    const offset = 0

    if (count === -1) {
        count = positionData.length / 2
    }

    gl.drawArrays(primitiveType, offset, count)
}