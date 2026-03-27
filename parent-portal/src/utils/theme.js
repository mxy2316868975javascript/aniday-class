const THEME_STORAGE_KEY = 'ddclass-theme'
const DEFAULT_THEME = 'light'

export function resolveTheme(theme) {
  if (theme === 'light' || theme === 'dark') {
    return theme
  }

  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY)
  if (storedTheme === 'light' || storedTheme === 'dark') {
    return storedTheme
  }

  return DEFAULT_THEME
}

export function applyTheme(theme) {
  const resolvedTheme = resolveTheme(theme)
  document.documentElement.dataset.theme = resolvedTheme
  document.documentElement.style.colorScheme = resolvedTheme
  localStorage.setItem(THEME_STORAGE_KEY, resolvedTheme)
  return resolvedTheme
}

export function initializeTheme() {
  return applyTheme(resolveTheme())
}
