import {
  defineConfig,
  presetAttributify,
  presetIcons,
  presetTypography,
  presetUno,
  presetWebFonts,
  transformerDirectives,
  transformerVariantGroup,
} from 'unocss'

export default defineConfig({
  shortcuts: [
    [/^(.*)--c-(.*)$/, ([, prefix, c]) => `${prefix}-[var(--c-${c})]`], // bg--c-bg-primary -> bg-[var(--c-bg-primary)], etc.
    ['fn-link', 'text--c-accent outline-none underline-1 hover:underline focus:underline'],
    ['fn-icon-btn', 'outline-none inline-block cursor-pointer select-none opacity-75 transition duration-200 ease-in-out hover:opacity-100 hover:text--c-accent focus:opacity-100 focus:text--c-accent'],
    ['fn-outline', 'border--c-inverse outline-none rd-1 b-1'],
    ['fn-outline-hover', 'hover:bg--c-bg-secondary focus:bg--c-bg-secondary focus:border--c-accent focus-within:border--c-accent'],
    ['text-xs', 'text-[0.75rem] line-height-[1rem]'],
    ['markdown-body', 'text-left m-auto prose'],
  ],
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2,
      warn: true,
    }),
    presetTypography(),
    presetWebFonts({
      fonts: {
        sans: 'DM Sans',
        serif: 'DM Serif Display',
        mono: 'DM Mono',
      },
    }),
  ],
  transformers: [
    transformerDirectives(),
    transformerVariantGroup(),
  ],
  safelist: ''.split(' '),
})
