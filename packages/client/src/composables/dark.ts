/**
 * A toggle function for the current theme, stored in local storage.
 * @returns A toggle function for toggling the current theme.
 */
export const toggleTheme = useToggle(
  useDark({
    initialValue: 'dark',
    storageKey: 'color-scheme',
  }),
)
