/*global $, WebSocket, console, window, document*/
"use strict";
//This is the Java file that connects the GUI to the Pi
function toogleDpadButtons(){
	var dpad_buttons = document.getElementsByClassName("d-button")
	// This gets informatnion about the buttons forom the HTML page
	for (var x=0; x<dpad_buttons.lenght; x++){
		dpad_buttons[x].disabled = !dpad_buttons[x].disabled
		//This deactivates the buttons
	}
}
function LoadTitle(){
	    $.getJSON( "static/Config/configuration.json", function(json) {
            $('#title').text(json.title)
        //this loads up a defult config file
    })
}
function BindDPadButtons(_client){
	$(' #MoveLeftButton').on({
		"touchstart": function(){_client.move('LEFT')},
		"mousedown": function(){_client.move('LEFT')},
		"touchend": function(){_client.move('LEFT')},
		"mouseup": function(){_client.move('LEFT')}
	})
	$(' #MoveRightButton ').on({
		"touchstart": function(){_client.move('RIGHT')},
		"mousedown": function(){_client.move('RIGHT')},
		"touchend": function(){_client.move('RIGHT')},
		"mouseup": function(){_client.move('RIGHT')}
	})
	$(' #MoveBackButton').on({
		"touchstart": function(){_client.move('BACKWARDS')},
		"mousedown": function(){_client.move('BACKWARDS')},
		"touchend": function(){_client.move('BACKWARDS')},
		"mouseup": function(){_client.move('BACKWARDS')}
	})
	$(' #MoveForwardButton').on({
		"touchstart": function(){_client.move('FORWARD')},
		"mousedown": function(){_client.move('FORWARD')},
		"touchend": function(){_client.move('FORWARD')},
		"mouseup": function(){_client.move('FORWARD')}
	})
}
// The above is what sends the users button presses to the main script, there are diffrent methods as the user 
//can interact with the code on diffrent platforms
var client = {
	//connects the users device to the open socket on the pi
	connect: function (port,callback) {
		var self = this, video = document.getElementById("video");
        this.socket = new WebSocket("ws://" + window.location.hostname + ":" + port + "/websocket");
		//The below askes for the stream once the contorler and PI are connected
		this.socket.onopen = function(){
			console.log("Connected!");
			self.CameraFeed();
			BindDPadButtons(self)
		};
		// to prevent oddness with a video stream on the users device, the video feed is converted too images, and this ensures
		// that there is not issues with this
		this.socket.onmessage = function(messsageEvent){
			video.scr = "data:image/jpeg;base64," + messageEvent.data;
		};
	},
	move: function(_direction){
		console.log('Move '+_direction)
		this.socket.send(_direction);
		//This adds the momvent to a cosole, when the user makes it move plus the difrection
	},
	stop: function(_direction){
		console.log("Stop "+ _direction)
		this.socket.send('STOP '+_direction)
		//This puts when the user trys to stop the duck and a direction into a console
	},
	self_drive: function(){
		console.log("Self_Driving funcion called")
		var selfDriveButton = document.getElementById("action-button");
		if (selfDriveButton.innerText == "Start Self-Drive"){
			selfDriveButton.innterText = "Quack!"
			toggleDpadButtons()
			this.socket.send("manual");
		}
		else{
			selfDriveButton.innterText = "Start Self-Drive"
			toggleDpadButtons()
			this.socket.send("manual");
		// This changes the text in the button for self driving, it also notifys the pi
		}
	},
	save_frames: function(){
		console.log("Save Frames")
		this.socket.send("save_frames");
		//saves the video stream to help the traning process
	},
	readCamera: function() {
		this.socket.send("read_camera")
		//reads the camerea input from the pi
	},
	setMode: function(_mode){
		if (_mode =='True'){
			$('#action-button')
				.text('Train')
				.click(function(){
					client.save_frames()
				})
		}
		else{
			$('#action-button')
				.text('Self Drive')
				.click(function(){
					client.self_drive()
			})
		}
	}
};