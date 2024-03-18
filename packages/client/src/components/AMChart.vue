<script setup lang="ts">
import * as am5 from '@amcharts/amcharts5'
import * as am5xy from '@amcharts/amcharts5/xy'
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated'
import am5themes_Dark from '@amcharts/amcharts5/themes/Dark'

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
    panX: true,
    panY: true,
    wheelX: 'panX',
    wheelY: 'zoomX',
    pinchZoomX: true,
    paddingLeft: 0,
  }))

  // Add cursor
  // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
  const cursor = chart.set('cursor', am5xy.XYCursor.new(root, {
    behavior: 'none',
  }))
  cursor.lineY.set('visible', false)

  // Generate random data
  function generateData(count: number) {
    const data = []
    const date = new Date()
    let value = 100

    date.setHours(0, 0, 0, 0)
    for (let i = 0; i < count; ++i) {
      value = Math.round((Math.random() * 10 - 5) + value)
      am5.time.add(date, 'day', 1)
      data.push({
        date: date.getTime(),
        value,
      })
    }

    return data
  }

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
    renderer: am5xy.AxisRendererY.new(root, {
      pan: 'zoom',
    }),
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
  series.data.setAll(generateData(1200))

  // Make stuff animate on load
  // https://www.amcharts.com/docs/v5/concepts/animations/
  series.appear(1000)
  chart.appear(1000, 100)

  onBeforeUnmount(() => {
    if (root)
      root.dispose()
  })
})
</script>

<template>
  <div
    ref="chartdiv"
    h-full w-full color--c-text
  />
</template>
