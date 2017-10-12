network = require 'browser/node-network'
heatmap = require 'browser/heatmap'
sankey = require 'browser/sankey'


nodes = [
  { name: 'networkNode', component: network }
  { name: 'heatmapNode', component: heatmap }
  { name: 'sankeyNode', component: sankey }
]

module.exports = ->
  for node in nodes
    el = document.getElementById node.name
    if el
      node.component el
      break
