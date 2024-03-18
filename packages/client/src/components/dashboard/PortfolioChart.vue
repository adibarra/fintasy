<script setup lang="ts">
import * as am5 from '@amcharts/amcharts5'
import * as am5xy from '@amcharts/amcharts5/xy'
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated'
import am5themes_Dark from '@amcharts/amcharts5/themes/Dark'

const props = defineProps({
  data: {
    type: Array as PropType<
      {
        date: number
        value: number
      }[]
    >,
    required: true,
  },
})

const chartdiv = ref<HTMLElement>()

onMounted(() => {
  const root = am5.Root.new(chartdiv.value!)

  watch(isDark, (isDark) => {
    root.setThemes(isDark
      ? [
          am5themes_Animated.new(root),
          am5themes_Dark.new(root),
        ]
      : [
          am5themes_Animated.new(root),
        ])
  }, { immediate: true })

  const chart = root.container.children.push(am5xy.XYChart.new(root, {
    paddingLeft: 0,
  }))

  // Add cursor
  // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
  const cursor = chart.set('cursor', am5xy.XYCursor.new(root, {
    behavior: 'none',
  }))
  cursor.lineY.set('visible', false)

  // Create axes
  // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
  const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
    maxDeviation: 0.1,
    baseInterval: {
      timeUnit: 'day',
      count: 1,
    },
    renderer: am5xy.AxisRendererX.new(root, {
      minorGridEnabled: true,
    }),
    tooltip: am5.Tooltip.new(root, {}),
  }))

  const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
    renderer: am5xy.AxisRendererY.new(root, { }),
  }))

  // Add series
  // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
  const series = chart.series.push(am5xy.LineSeries.new(root, {
    name: 'Series',
    xAxis,
    yAxis,
    valueYField: 'value',
    valueXField: 'date',
    tooltip: am5.Tooltip.new(root, {
      // eslint-disable-next-line no-template-curly-in-string
      labelText: '${valueY}',
    }),
  }))

  // Set data
  series.data.setAll(props.data)

  // Make stuff animate on load
  // https://www.amcharts.com/docs/v5/concepts/animations/
  series.appear(2500, 100)
  chart.appear(2500, 100)

  onBeforeUnmount(() => {
    if (root)
      root.dispose()
  })
})
</script>

<template>
  <div flex>
    <span ml-1 text-xl>Portfolio Value</span>
    <div grow />
    <span
      :class="data[data.length - 1].value >= 0 ? 'color-green' : 'color-red'"
      mx-2 text-xl
    >
      $
      <n-number-animation
        :from="0"
        :to="data[data.length - 1].value"
        :duration="4000"
        :active="true"
        show-separator
      />
    </span>
  </div>
  <div
    ref="chartdiv"
    mt-2 h-full min-h-50 w-full color--c-text
  />
</template>
