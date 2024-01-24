import antfu from '@antfu/eslint-config'

export default await antfu({
  typescript: true,
  vue: true,
  rules: {
    'antfu/if-newline': 'off',
  },
})
