$ = require 'jquery'
d3Scale = require 'd3-scale'
echarts = require 'echarts'
_startCase = require 'lodash/startCase'
_snakeCase = require 'lodash/snakeCase'
download = require 'downloadjs'

CELLPROC = 'Cellular Functions'
MOLFN = 'Molecular Activities'


class SankeyChart
  constructor: (el) ->
    @el = el
    @chart = echarts.init @el
    window.chart = @

  drawGraph: (data, tissue) =>
    schemeScale = d3Scale.scaleOrdinal(d3Scale.schemeCategory20c)
    @getProcess = (id) -> _startCase data.labels[+id[2..]]

    tissueName = _startCase tissue.split('-')[1]
    tissueProc = if tissue.indexOf('func') >= 0 then CELLPROC else MOLFN

    data.nodes.forEach (node) =>
      node.itemStyle =
        normal:
          color: schemeScale @getProcess node.name

      node.label =
        normal:
          position: if node.name.indexOf('x_') >= 0 then 'left' else 'right'

    data.links.forEach (edge) ->
      edge.lineStyle =
        normal:
          opacity: if edge.value > 0 then 0.5 else 0

    options = {
      title:
        text: tissueName
        left: 'center'
        subtext: tissueProc
      tooltip: {}
      toolbox:
        feature:
          saveAsImage:
            type: 'png'
            title: 'Save'
            pixelRatio: 3
      series: [
        {
          type: 'sankey'
          data: data.nodes
          links: data.links
          nodeGap: 10
          left: 'center'
          width: '40%'
          top: 60
          label:
            normal:
              formatter: (params) => @getProcess params.name
          itemStyle:
            normal:
              borderColor: '#000'
              borderType: 'solid'
          lineStyle:
            normal:
              color: 'source'
              curveness: 0.5
              opacity: 0.4
          tooltip:
            padding: [2, 5]
            borderWidth: 1
            backgroundColor: '#192B35'
            extraCssText: 'border-radius: 2;'
            formatter: (params) =>
              if params.dataType is 'edge'
                source = @getProcess params.data.source
                target = @getProcess params.data.target
                "#{source} → #{target} (#{Math.floor params.value})"
              else
                @getProcess params.name
        }
      ]
      animation: no
    }

    @chart.hideLoading()
    @chart.setOption options

    fileName = _snakeCase "#{tissueProc}--#{tissueName}"

    # setTimeout (=> @save(fileName)), 1000

  draw: (tissue) ->
    url = "/static/#{tissue}.json"
    loading_opts =
      text: 'Loading'
      maskColor: 'rgba(0, 0, 0, 0)'
      zlevel: 10

    @chart.showLoading('default', loading_opts)
    $.get url, (data) => @drawGraph(data, tissue)

  save: (fileName) ->
    blob = @chart.getDataURL {
      type: 'png'
      pixelRatio: 3
      backgroundColor: '#fff'
    }
    download blob, "#{fileName}.png", 'image/png'

module.exports = (el) ->
  chart = new SankeyChart el

  update_chart = () ->
    tissue = $('input[name="sankey-args.tissue"]:checked').val()
    kind = $('input[name="sankey-args.kind"]:checked').val()
    chart.draw "sankey.#{kind}.#{tissue}"

  update_chart()

  $('input[name^="sankey-args"]').on 'change', () -> update_chart()
