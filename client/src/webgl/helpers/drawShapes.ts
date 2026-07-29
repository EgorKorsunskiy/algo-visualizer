import { COLORS } from "./constants"
import { drawScene } from "./drawScene"

function getTextMetrics(text: string, fontSize: number = 24) {
    const offscreenCanvas = document.createElement('canvas')
    const ctx = offscreenCanvas.getContext('2d')
    if (ctx === null) return null;
    ctx.font = `${fontSize}px Arial`
    const padding = 2

    const metrics = ctx.measureText(text)
    const textWidth = metrics.width
    const textHeight = fontSize - padding

    return { textWidth, textHeight }
}

export function drawRectangle(gl: WebGLRenderingContext, x: number, y: number, width: number, height: number, color: Array<number>, text: string = "") {
    const positionData = new Float32Array([
        x, y,
        x + width, y,
        x, y + height,
        x, y + height,
        x + width, y + height,
        x + width, y
    ])
    const vertexCount = positionData.length / 2
    const colorData = new Float32Array(vertexCount * 4)
    for (let i = 0; i < vertexCount; i++) {
        colorData.set(color, i * 4)
    }
    drawScene(gl, positionData, colorData)
    if (text) {
        const metrics = getTextMetrics(text)
        if (metrics === null) return null
        const textX = x + (width / 2) - (metrics.textWidth / 2)
        const textY = y + (height / 2) - (metrics.textHeight / 2)
        drawText(gl, text, textX, textY)
    }
}

export function drawOutlinedRectangle(gl: WebGLRenderingContext, x: number, y: number, width: number, height: number, color: Array<number>, borderWidth: number, text: string = "") {
    drawRectangle(gl, x, y, width, height, color)
    drawRectangle(gl, x + borderWidth, y + borderWidth, width - (2 * borderWidth), height - (2 * borderWidth), COLORS.WHITE, text)
}

export function drawText(gl: WebGLRenderingContext, text: string, x: number, y: number, fontSize: number = 24, fontColor: string = "black") {
    const metrics = getTextMetrics(text, fontSize)
    if (metrics === null) return null
    const { textWidth, textHeight } = metrics

    const offscreenCanvas = document.createElement('canvas')
    const ctx = offscreenCanvas.getContext('2d')
    if (ctx === null) return null;

    offscreenCanvas.width = textWidth
    offscreenCanvas.height = textHeight

    ctx.clearRect(0, 0, textWidth, textHeight);
    ctx.font = `${fontSize}px Arial`
    ctx.fillStyle = fontColor
    ctx.fillText(text, 0, textHeight)

    const positionData = new Float32Array([
        x, y,
        x + textWidth, y,
        x, y + textHeight,
        x, y + textHeight,
        x + textWidth, y,
        x + textWidth, y + textHeight,
    ])
    const colorData = new Float32Array(positionData.length * 4)
    drawScene(gl, positionData, colorData, offscreenCanvas)
}