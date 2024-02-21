export const preferredDark = usePreferredDark()
export const isDark = useDark({
  initialValue: 'dark',
  storageKey: 'color-scheme',
})
export const toggleTheme = useToggle(isDark)
