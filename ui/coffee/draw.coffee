console.log 'hello'


class Path
  constructor: (mode = 'draw') ->
    @mode = mode
    @data = []

  toDict: ->
    return {
      mode: @mode,
      data: @data
    }


class Main
  constructor: -> 
    @canvas = document.getElementById 'canvas'
    @context = @canvas.getContext('2d')

    @canvas.addEventListener 'mousedown', @mousedown.bind(this), false
    @canvas.addEventListener 'mouseup', @mouseup.bind(this), false
    @canvas.addEventListener 'mousemove', @mousemove.bind(this), false
    $(@canvas).on 'touchstart', @touchstart.bind(this)
    $(@canvas).on 'touchend', @touchend.bind(this)
    $(@canvas).on 'touchmove', @touchmove.bind(this)

    @isDrawing = false

    @paths = []
    @path = null

    @mode = 'draw'
    $('#buttons .draw').click =>
      @mode = 'draw'
    $('#buttons .erase').click =>
      @mode = 'erase'
    $('#buttons .send').click =>
      @send()

  mousedown: (e) ->
    console.log('mousedown')
    @isDrawing = true
    @path = new Path(@mode)
    @paths.push @path

  mouseup: (e) ->
    console.log('mouseup')
    @isDrawing = false
    @path = null

  mousemove: (e) ->
    pos = $(@canvas).position()
    x = e.clientX - pos.left
    y = e.clientY - pos.top
    if @isDrawing
      @path.data.push([x, y])
    @draw()

  touchstart: (e) ->
    console.log('touchstart')
    @isDrawing = true
    @path = new Path(@mode)
    @paths.push @path

  touchend: (e) ->
    console.log('touchend')
    @isDrawing = false
    @path = null

  touchmove: (e) ->
    touch = e.touches[0];
    pos = $(@canvas).position()
    x = touch.clientX - pos.left
    y = touch.clientY - pos.top
    if @isDrawing
      @path.data.push([x, y])
    @draw()

  draw: ->
    ctx = @context

    for path in @paths
      if path.mode == 'draw'
        ctx.lineWidth = 8
        ctx.lineCap = 'round'
        ctx.strokeStyle = 'black'
      else
        ctx.lineWidth = 32
        ctx.lineCap = 'round'
        ctx.strokeStyle = 'white'

      ctx.beginPath()
      [x, y] = path.data[0]
      ctx.moveTo x, y

      for point in path.data[1...path.data.length]
        [x, y] = point
        ctx.lineTo x, y

      ctx.stroke()

  send: ->
    paths = (path.toDict() for path in @paths)
    $.ajax
      type: 'POST'
      url: '/wave'
      data: 'data=' + JSON.stringify(paths)
      success: -> console.log 'success'
      error: (e) -> console.log(e)



$ ->
  window.main = new Main

