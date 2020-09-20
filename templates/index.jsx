<!--<meta http-equiv="refresh" content="5"> -->
{% extends "bootstrap/base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block title %}djs_woz{% endblock %}

{% block styles %}
{{super()}}
<link rel="stylesheet" href="{{url_for('.static', filename='css/style.css')}}"></link>
<link rel="stylesheet" href="{{url_for('.static', filename='css/bootstrap-theme.min.css')}}"></link>
<link rel="stylesheet" href="{{url_for('.static', filename='css/fontAwesome.css')}}"></link>
<link rel="stylesheet" href="{{url_for('.static', filename='css/light-box.css')}}"></link>
<link rel="stylesheet" href="{{url_for('.static', filename='css/owl-carousel.css')}}"></link>
<link rel="stylesheet" href="{{url_for('.static', filename='css/templatemo-style.css')}}"></link>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700,800"></link>
{% endblock %}

{% block scripts %}
<script type="module" src="{{url_for('.static', filename='node_modules/react-tree-graph/src/components/tree.js')}}"></script>
<script type="module" src="{{url_for('.static', filename='static/dist/bundle.js')}}"></script>
{{super()}}
{% endblock %}

{% block navbar %}
<div class="navbar navbar-inverse" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle"
            data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">DJS_WOZ</a>
        </div>
    <div class="navbar-collapse collapse">
        <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
        </ul>
    </div>
    </div>
</div>
{% endblock %}



{% block content %}
<div class="container">
    <div class="page-header">
        <div id="place_for_query" float="left"></div>
            <!-- {% raw %}
            <button type="submit" class="btn btn-primary" ng-disabled="loading">{{ submitButtonText }}</button>
            {% endraw %} -->
        <div id="quickMenu" float="right"></div>
    </div>
    
    <section id="video" class="content-section">
        <div class="row">
            <div class="col-md-4" style="width:40%; margin-top:-12px; margin-left:2px; float:left;">
                <div class="panel panel-info">
                <div class="panel-heading">
                            Realtime Chat
                        </div>
					  
					<div class="panel-body">
                    <div class="h-100 justify-content-center">
                    <div class="chat-container" style="overflow: auto; max-height: 80vh; height:400px;">
                        <!-- chat messages -->
                        <div class="chat-message col-md-5 offset-md-7 bot-message" style="align:right;">
                          Listening...
                        </div>
                    </div>
                        <form id="responseForm">
                            <input class="controls form-control" type="text" placeholder="Enter Response..." id="input_message" style="width:100%; font-size:20px;"/>
                            <input type="submit" hidden>
                        </form>
                        </div>
					</div>   
			    </div>
            </div>
            </div>
            <div class="col-md-4" style="width:40%;">
            <div class="panel panel-info"style="margin-bottom:5px;">
                        <div class="panel-heading">
                            Name of Current Chat Person
                        </div>
                        <div class="panel-body chat-widget-main" style="max-height:400px;">
                            <div class="chat-widget-left">
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                           Lorem ipsum dolor.
                            </div>
                            <div class="chat-widget-name-left">
                                <img class="media-object img-circle img-left-chat" src="assets/img/user2.png" />
                                <h4>  Amanna Seiar</h4>
                                <h5>Time 2:00 pm at 25th july</h5>
                            </div>
                            <div class="chat-widget-name-right">
                               <img class="media-object img-circle img-right-chat" src="assets/img/user2.png" />
                                <h4>  Amanna Seiar</h4>
                                <h5>Time 2:00 pm at 25th july</h5>
                            </div>
                            <hr />
							<div class="chat-widget-left">
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                           Lorem ipsum dolor sit amet.
                            </div>
                            <hr />
                        </div>

                    </div>                             
            </div>
            </div>
    </section>
     



<script src="https://fb.me/react-0.14.3.js"></script>
<script src="https://fb.me/react-dom-0.14.3.js"></script>
<script src=" https://cdnjs.cloudflare.com/ajax/libs/babel-core/5.8.24/browser.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script>
    $("#document").ready(function(){
    var text = $(this).val();
    var myajax = function(){
        $.ajax({
            url: "/webhook",
            type: "get",
            data: {text},
            success: function(response) {
                $("#place_for_query").html(response);
                myajax();
            },
            error: function(xhr) {
                //Do Something to handle error
                $("#place_for_query").val("No Query Found!!");
            }
        });
    };
    myajax();
});

function submit_response(response) {
    $.post( "/send_response", {response: response});
}

$('#responseForm').on('submit', function(){
    
    const input_message = $('#input_message').val()
    // return if the user does not enter any text
    if (!input_message) {
      return;
    }

    $('.chat-container').append(`
            <div class="chat-message col-md-5 human-message">
                ${input_message}
            </div>
        `)

    // send the message
    submit_response(input_message)
});


</script>

<script type="text/babel">
    
    var QuickMenu = React.createClass({

        repeatLastResponse : function(){
            alert('Sending previous response');
        },
        askUserToRepeat : function(){
            alert('Asking user to repeat last utterance.');
        },
        render: function() {
            return(
                <div>
                    <button className="accent-button button" onClick={this.askUserToRepeat}>Ask user to repeat</button>
                    <button className="accent-button button" onClick={this.repeatLastResponse}>Repeat last response</button>
                </div> 
            );
        }
    });

    var CollapsibleTree = React.createClass({
        data: {
            name:'Parent',
            children:[{
                name: 'Child One'
            }, {
                name: 'Child Two'
            }]
        },
        render: function(){
            return(
                <Tree data={data}
                height={400}
                width={400}/>
            );
        }
    });
    


    ReactDOM.render(<div>
            <QuickMenu></QuickMenu><CollapsibleTree></CollapsibleTree>
        </div>, document.getElementById('quickMenu'))
</script>

{% endblock %}