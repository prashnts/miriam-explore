$ = require 'jquery'
echarts = require 'echarts'
require 'echarts/dist/extension/dataTool'

class NodeNetwork
  constructor: (id) ->
    @el = document.getElementById id
    @chart = echarts.init @el, 'roma'

  drawGraph: (xml) =>
    @chart.hideLoading()

    graph = echarts.dataTool.gexf.parse xml

    categories = (name: c for c in ['mirna', 'gene'])

    graph.nodes.forEach (node) ->
      node.category = node.attributes['0']
      node.value = node.attributes['1']
      node.symbolSize = node.attributes['1'] / 10
      node.label = normal: show: node.symbolSize > 10

    graph.links.forEach (link) ->
      thickness = link.lineStyle.normal.width
      link.lineStyle =
        normal:
          width: thickness / 70
          opacity: 0.03
          color: '#000'
        emphasis:
          opacity: 1
          color: '#000'

    options = {
      legend: [
        {
          data: categories.map (a) -> a.name
        }
      ]
      tooltip: {}
      series: [
        {
          type: 'graph'
          layout: 'circular'
          force: edgeLength: 1000
          circular: rotateLabel: yes
          focusNodeAdjacency: yes
          hoverAnimation: yes
          data: graph.nodes
          links: graph.links
          #edgeSymbol: ['none', 'arrow']
          categories: categories
          roam: yes
          label: normal: { position: 'right', formatter: '{b}' }
          lineStyle:
            normal:
              curveness: 0.3
            emphasis:
              curveness: 0
              opacity: 1
        }
      ]
      animationDuration: 1000
      animationEasingUpdate: 'quinticInOut'
    }

    @chart.setOption options

  draw: ->
    @chart.showLoading()
    $.get '/static/aorta.gexf', @drawGraph, 'xml'


module.exports = ->
  nn = new NodeNetwork 'browserEntry'
  nn.draw()
