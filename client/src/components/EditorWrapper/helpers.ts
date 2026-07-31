export function removeEscapeChars(value: string) {
    return value.replace(/\n/g, "").replace(/\t/g, "")
}