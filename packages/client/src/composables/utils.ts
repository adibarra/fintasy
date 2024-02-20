/**
 * Clamps a number between a minimum and maximum value.
 * @param num - The number to clamp.
 * @param min - The minimum value to clamp the number to.
 * @param max - The maximum value to clamp the number to.
 * @returns The clamped number.
 */
export function clamp(num: number, min: number, max: number): number {
  return Math.min(Math.max(num, min), max)
}
