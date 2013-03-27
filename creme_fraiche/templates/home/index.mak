
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>${project}, from Linux</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="${request.static_url('creme_fraiche:static/css/bootstrap.css')}" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="${request.static_url('creme_fraiche:static/css/bootstrap-responsive.css')}" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="${request.static_url('creme_fraiche:static/js/html5shiv.js')}"></script>
    <![endif]-->

  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="brand" href="#">${project}</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li class="active"><a href="#">Home</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">

      <h1>${project}</h1>
      <p>Use this document as a way to quick start any new project.<br> All you get is this message and a barebones HTML document.</p>

    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="${request.static_url('creme_fraiche:static/js/jquery.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-transition.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-alert.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-modal.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-dropdown.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-scrollspy.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-tab.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-tooltip.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-popover.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-button.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-collapse.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-carousel.js')}"></script>
    <script src="${request.static_url('creme_fraiche:static/js/bootstrap-typeahead.js')}"></script>

  </body>
</html>
