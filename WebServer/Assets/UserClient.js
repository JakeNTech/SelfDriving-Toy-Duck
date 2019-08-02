/*global $, WebSocket, console, window, document*/
"use strict";
//This is the Java file that connects the GUI to the Pi
//When the buttons are pressed they will trigger the movement and will then stop that movement, adapted for a computer or
//touch screen
function BindDPadButtons(_client){
	$(' #MoveLeftButton').on({
		"touchstart": function(){_client.move('LEFT')},
		"mousedown": function(){_client.move('LEFT')},
		"touchend": function(){_client.stop('LEFT')},
		"mouseup": function(){_client.stop('LEFT')}
	})
	$(' #MoveRightButton ').on({
		"touchstart": function(){_client.move('RIGHT')},
		"mousedown": function(){_client.move('RIGHT')},
		"touchend": function(){_client.stop('RIGHT')},
		"mouseup": function(){_client.stop('RIGHT')}
	})
	$(' #MoveBackwardsButton').on({
		"touchstart": function(){_client.move('BACKWARDS')},
		"mousedown": function(){_client.move('BACKWARDS')},
		"touchend": function(){_client.stop('BACKWARDS')},
		"mouseup": function(){_client.stop('BACKWARDS')}
	})
	$(' #MoveForwardButton').on({
		"touchstart": function(){_client.move('FORWARD')},
		"mousedown": function(){_client.move('FORWARD')},
		"touchend": function(){_client.stop('FORWARD')},
		"mouseup": function(){_client.stop('FORWARD')}
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
			self.readCamera();
			BindDPadButtons(self)
		};
		// to prevent oddness with a video stream on the users device, the video feed is converted too images, and this ensures
		// that there is not issues with this
        this.socket.onmessage = function (messageEvent) {
            video.src = "data:image/jpeg;base64," + messageEvent.data;
        };
	},
	//function adds movement to the console for debugging
	move: function(_directions){
		console.log('Move '+_directions)
		this.socket.send(_directions);
		//This adds the momvent to a cosole, when the user makes it move plus the difrection
	},
	//addes stops message to the console
	stop: function(_directions){
		console.log("Stop "+ _directions)
		this.socket.send('STOP '+_directions)
		//This puts when the user trys to stop the duck and a direction into a console
	},
	//When the Self-Driving button is pressed..self driving gets started
	self_drive: function(){
		var selfDriveButton = document.getElementById("action-button");
		if (selfDriveButton.innerText == "Start Self-Drive!"){
			var PleaseConfirm = false
			PleaseConfirm = confirm("Are you sure you wish to start self-driving?")
			if (PleaseConfirm == true){
				console.log("Self-Driving Started!")
				alert("Starting Self-Driving")
				console.log("Starting Self-Driving")
				selfDriveButton.innerText = "Quack!"
				toggleDpadButtons()
				this.socket.send("SelfDrive");
			}
			else if (PleaseConfirm == false){
				alert("Aborting!")
				console.log("Stopping")
			}
		}
		else{
			selfDriveButton.innerText = "Start Self-Drive!"
			this.socket.send("Manual");
		// This changes the text in the button for self driving, it also notifys the pi
		}
	},
	//Function for telling the webserver script that the user wants the about page
	shutdown: function(){
		var shutdownButton = document.getElementById("shutdown-button")
		if (shutdownButton.innnerText == "Shutdown"){
			console.log("shutdown")
			this.socket.send("shutdown");
		}
	},
	//Shows the camera output
	readCamera: function(){
		this.socket.send("readCamera")
		console.log("readCamera")
	},
	setMode: function(){
		$('#action-button')
			.text('Start SelfDrive')
			.click(function(){
				client.self_drive()
			})
		}
	};