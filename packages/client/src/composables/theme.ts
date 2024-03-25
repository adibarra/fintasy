/**
 * @author: adibarra (Alec Ibarra)
 * @description: Composable for handling color theme state
 */

export const preferredDark = usePreferredDark()
export const isDark = useDark({
  initialValue: 'dark',
  storageKey: 'color-theme',
})
export const toggleTheme = useToggle(isDark)
export const colorTheme = computed(() => (isDark.value ? 'dark' : 'light'))
