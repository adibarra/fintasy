<!--
  @author: adibarra (Alec Ibarra)
  @description: This component is used to display the user's portfolio value over time.
-->

<script setup lang="ts">
import * as am5 from '@amcharts/amcharts5'
import * as am5xy from '@amcharts/amcharts5/xy'
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated'
import am5themes_Dark from '@amcharts/amcharts5/themes/Dark'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  data: {
    type: Array as PropType<{
      date: number
      value: number
    }[]>,
    required: true,
  },
})

const chartdiv = ref<HTMLElement>()
const lastValue = computed(() => {
  if (props.data.length === 0)
    return 0
  return props.data[props.data.length - 1].value
})

onMounted(() => {
  // bind to chartdiv
  const root = am5.Root.new(chartdiv.value!)

  // add responsive theme
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

  // create chart
  const chart = root.container.children.push(am5xy.XYChart.new(root, {
    paddingLeft: 0,
  }))

  // add cursor
  const cursor = chart.set('cursor', am5xy.XYCursor.new(root, {
    behavior: 'none',
  }))
  cursor.lineY.set('visible', false)

  // create axes
  const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
    maxDeviation: 0.1,
    baseInterval: {
      timeUnit: 'second',
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

  // add series
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

  // set data
  series.data.setAll(props.data)

  // make stuff animate on load
  series.appear(2500, 100)
  chart.appear(2500, 100)

  // make data reactive
  watch(() => props.data, (data) => {
    series.data.setAll(data)
  })

  // handle cleanup
  onBeforeUnmount(() => {
    if (root)
      root.dispose()
  })
})
</script>

<template>
  <div flex>
    <span ml-1 text-xl font-600>
      {{ props.name }}
    </span>
    <div grow />
    <span
      :class="lastValue >= 0 ? 'color-lime-600 dark:color-lime-500' : 'color-red-500'"
      mx-2 text-xl font-600
    >
      $
      <n-number-animation
        :from="0"
        :to="lastValue"
        :duration="4000"
        :active="true"
        show-separator
      />
    </span>
    <span mr-2 mt-auto op-75>
      USD
    </span>
  </div>
  <div
    ref="chartdiv"
    mt-2 h-full min-h-50 w-full color--c-text
  />
</template>
