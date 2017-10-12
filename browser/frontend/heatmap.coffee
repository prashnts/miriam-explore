$ = require 'jquery'
echarts = require 'echarts'

PROCESSES = [
  'apopticProcess', 'biogenesis', 'biologicalAdhesion',
  'biologicalRegulation', 'cellKilling', 'cellularProcess',
  'developmentalProcess', 'growth', 'immuneSystemProcess',
  'localization', 'locomotion', 'metabolicProcess',
  'multicellularOrganismalProcess', 'reproduction', 'responsetoStimulus',
  'rhythmicProcess', 'transcriptionFactors'
]

class HeatmapChart
  constructor: (el) ->
    @el = el
    @chart = echarts.init @el, 'roma'

  drawGraph: (data) =>
    @chart.hideLoading()

    options = {
      tooltip: {}
      grid:
        height: 400
        width: 400
        y: 20
      xAxis:
        name: 'Target Genes'
        type: 'category'
        data: PROCESSES
        splitArea: show: yes
        splitLine: show: no
        interval: 1
        axisLabel:
          show: yes
          interval: 0
          rotate: 45
      yAxis:
        name: 'Host Genes'
        type: 'category'
        data: PROCESSES
        splitArea: show: yes
      series: [
        {
          type: 'heatmap'
          data: data
          label: normal: { show: no }
        }
      ]
      visualMap:
        calculable: yes
        max: 15
        min: 0
      animationDuration: 1000
      animationEasingUpdate: 'quinticInOut'
    }

    @chart.setOption options

  draw: ->
    @chart.showLoading()
    $.get '/static/leuk.json', @drawGraph

module.exports = (el) ->
  nn = new HeatmapChart el
  nn.draw()
