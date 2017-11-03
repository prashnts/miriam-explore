_ = require 'lodash'
bourbon = require 'node-bourbon'
fs = require 'fs'
fse = require 'fs-extra'
glob = require 'glob'

global.DEBUG = '-p' not in global.process.argv
global._COPIED = no

copy_map = [
  ['node_modules/@blueprintjs/core/resources', 'public/resources']
]

PROD = process.env.STAGING? or process.env.PRODUCTION?
STATIC_ROOT =
  if PROD
    "//#{process.env.AWS_BUCKET_NAME}.s3.amazonaws.com"
  else '/static'
# [@prashnts] This bit here is used to generate the watched folders
MODULE_PATH = '**/frontend/**/@(index|main).@(coffee|cjsx|jsx|js|styl|sass)'
watched = _
  .chain(glob.sync MODULE_PATH)
  .map (filename) ->
    [__, dirname] = /^(.+)\/(index|main).\w+$/.exec filename
    dirname
  .uniq()
  .value()

bundles = do ->
  bndls =
    js: 'js/vendors.js': /^node_modules/
    css: 'css/vendors.css': /^node_modules/
  for path in watched
    cpath = path.replace /\/?frontend/, ''
    app = if /^frontend/.test path then 'common' else cpath.replace /\//, '_'
    bndls.js["js/#{app}.js"]    = new RegExp "^#{path}\/[\\-_\\d\\w]+\\.\\w+$"
    bndls.css["css/#{app}.css"] = new RegExp "^#{path}\/[\\-_\\d\\w]+\\.\\w+$"
  bndls

console.log "==> #{unless PROD then 'Dev' else 'Production'} build"
console.log " --> Static root set to: #{STATIC_ROOT}"
console.log "==> Discovered #{watched.length} components"
for k, v of bundles.js
  console.log " --> #{/js\/(.+)\.js/.exec(k)[1]}"


module.exports = config:
  paths:
    watched: watched

  conventions:
    ignored: [
      /tests\//
      /^frontend\/.+\.styl$/
    ]

  plugins:
    autoReload:
      enabled: yes
    postcss:
      processors: [
        require('autoprefixer')(['last 8 versions'])
      ]
    sass:
      options:
        mode: 'ruby'
        debug: 'debug'
        allowCache: true
        includePaths: [
          './node_modules/@blueprintjs/core/dist/'
          './node_modules/tachyons-sass/'
          bourbon.includePaths...
        ]
    babel:
      presets: ['es2015', 'react', 'stage-2']
      ignore: [
        /^(node_modules)/
      ]
      pattern: /\.jsx?$/

  npm:
    enabled: yes
    styles:
      '@blueprintjs/core': [
        'dist/blueprint.css'
      ]
    globals:
      jQuery: 'jquery'
      $: 'jquery'

  modules:
    nameCleaner: (path) ->
      path
        .replace /\.cjsx/, ''
        .replace /\.coffee/, ''
        .replace /\.js/, ''
        .replace /\.jsx/, ''
        .replace /\.sass/, ''
        .replace /frontend\//, ''
        .replace /\/index/, ''

  files:
    javascripts:
      joinTo: bundles.js
    stylesheets:
      joinTo: bundles.css

  hooks:
    preCompile: (end) ->
      unless global._COPIED
        for [src, dest] in copy_map
          fse.copySync src, dest
          console.log 'Copied', src, 'to', dest
        global._COPIED = yes
      end()
