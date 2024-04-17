/* eslint-disable */
/* prettier-ignore */
// @ts-nocheck
// Generated by unplugin-vue-router. ‼️ DO NOT MODIFY THIS FILE ‼️
// It's recommended to commit this file.
// Make sure to add this file to your tsconfig.json file as an "includes" or "files" entry.

declare module 'vue-router/auto-routes' {
  import type {
    RouteRecordInfo,
    ParamValue,
    ParamValueOneOrMore,
    ParamValueZeroOrMore,
    ParamValueZeroOrOne,
  } from 'unplugin-vue-router/types'

  /**
   * Route name map generated by unplugin-vue-router
   */
  export interface RouteNamedMap {
    '/': RouteRecordInfo<'/', '/', Record<never, never>, Record<never, never>>,
    '/[...all]': RouteRecordInfo<'/[...all]', '/:all(.*)', { all: ParamValue<true> }, { all: ParamValue<false> }>,
    '/dashboard/': RouteRecordInfo<'/dashboard/', '/dashboard', Record<never, never>, Record<never, never>>,
    '/dashboard/[...all]': RouteRecordInfo<'/dashboard/[...all]', '/dashboard/:all(.*)', { all: ParamValue<true> }, { all: ParamValue<false> }>,
    '/dashboard/help/': RouteRecordInfo<'/dashboard/help/', '/dashboard/help', Record<never, never>, Record<never, never>>,
    '/dashboard/help/faq': RouteRecordInfo<'/dashboard/help/faq', '/dashboard/help/faq', Record<never, never>, Record<never, never>>,
    '/dashboard/settings': RouteRecordInfo<'/dashboard/settings', '/dashboard/settings', Record<never, never>, Record<never, never>>,
    '/dashboard/tournaments': RouteRecordInfo<'/dashboard/tournaments', '/dashboard/tournaments', Record<never, never>, Record<never, never>>,
    '/dashboard/trade': RouteRecordInfo<'/dashboard/trade', '/dashboard/trade', Record<never, never>, Record<never, never>>,
    '/login': RouteRecordInfo<'/login', '/login', Record<never, never>, Record<never, never>>,
  }
}
