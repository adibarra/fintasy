const { width, height } = useWindowSize()

/**
 * A computed property that returns whether the window should be rendered as a mobile view.
 * @returns Whether the window should be rendered as a mobile view.
 */
export const isMobile = computed<boolean>(() => {
  return width.value < 640 || height.value < 640
})
