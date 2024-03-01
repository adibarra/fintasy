// @ts-check
import antfu from '@antfu/eslint-config'

export default antfu({
  unocss: true,
  formatters: true,
  rules: {
    'if-newline': 'off',
  },
})
