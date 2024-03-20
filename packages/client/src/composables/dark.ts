/**
 * @author: adibarra (Alec Ibarra)
 * @description: Composable for handling dark mode state
 */

export const preferredDark = usePreferredDark()
export const isDark = useDark({
  initialValue: 'dark',
  storageKey: 'color-scheme',
})
export const toggleTheme = useToggle(isDark)
export const colorTheme = computed(() => (isDark.value ? 'dark' : 'light'))
