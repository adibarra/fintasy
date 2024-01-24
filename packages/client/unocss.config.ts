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
    ['custom-bg', 'bg-[var(--c-primary)]'],
    ['custom-text', 'text-[var(--c-text)]'],
    ['custom-accent', 'text-[var(--c-accent)]'],
    ['custom-link', 'custom-accent outline-none underline-1 hover:underline focus:underline'],
    ['custom-outline', 'border-[var(--c-inverse)] outline-none rd-1 b-1'],
    ['custom-outline-hover', 'hover:bg-[var(--c-secondary)] focus:bg-[var(--c-secondary)] focus:b-[var(--c-accent)] focus-within:b-[var(--c-accent)]'],
    ['custom-icon-btn', 'outline-none inline-block cursor-pointer select-none opacity-75 transition duration-200 ease-in-out hover:opacity-100 hover:text-[var(--c-accent)] focus:opacity-100 focus:text-[var(--c-accent)]'],
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
